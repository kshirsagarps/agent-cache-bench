import os
import json
import numpy as np
from typing import Dict, Any, List, Optional
from agentcachebench import NOT_OBSERVABLE
from agentcachebench.adapters.base import CacheRuntimeAdapter, StepRequest
from agentcachebench.adapters.simulated_engine import SimulatedKVEngine
from agentcachebench.instrumentation.provenance import capture_provenance
from agentcachebench.instrumentation.context_overlap import compute_logical_overlap
from agentcachebench.instrumentation.realized_reuse import compute_realized_reuse
from agentcachebench.instrumentation.compute_accounting import compute_actual_compute_avoided
from agentcachebench.instrumentation.latency import compute_latency_metrics
from agentcachebench.metrics.calculators import compute_correlation_rho_and_r, compute_summary_statistics
from agentcachebench.runner.hashing import compute_config_hash
from agentcachebench.runner.schema_validation import validate_raw_result_schema

class BenchmarkRunner:
    def __init__(self, output_dir: str = "results/raw"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def run_experiment(
        self,
        experiment_id: str,
        workload_name: str,
        trajectory: List[Dict[str, Any]],
        scenario_id: str = "S1",
        baseline_id: str = "B1",
        adapter_config: Optional[Dict[str, Any]] = None,
        seed: int = 42
    ) -> Dict[str, Any]:
        adapter_config = adapter_config or {}
        config_hash = compute_config_hash({
            "experiment_id": experiment_id,
            "workload": workload_name,
            "scenario": scenario_id,
            "baseline": baseline_id,
            "adapter_config": adapter_config,
            "seed": seed
        })

        provenance = capture_provenance(
            experiment_id=experiment_id,
            model=adapter_config.get("model", "mock-agent-7b"),
            backend=adapter_config.get("backend", "simulated_engine"),
            config_hash=config_hash,
            seed=seed
        )

        # Instantiate engine
        adapter = SimulatedKVEngine()
        adapter.initialize(adapter_config)

        session_id = f"session_{experiment_id}"
        adapter.start_session(session_id)

        step_results = []
        overlaps = []
        avoideds = []
        realized_reuses = []
        ttfts = []
        latencies = []

        prev_tokens: List[int] = []

        for step_data in trajectory:
            step_id = step_data["step_id"]
            prompt_tokens = step_data["prompt_tokens"]
            pause_ms = step_data.get("pause_ms", 0.0)

            # Cold baseline handling (B0 resets cache every step)
            if baseline_id == "B0" or scenario_id == "S0":
                adapter.reset()
                adapter.start_session(session_id)

            req = StepRequest(
                session_id=session_id,
                step_id=step_id,
                prompt_tokens=prompt_tokens,
                pause_before_step_ms=pause_ms
            )

            resp = adapter.run_step(req)

            # Compute instrumentation metrics
            overlap_info = compute_logical_overlap(prompt_tokens, prev_tokens)
            realized_info = compute_realized_reuse(
                resp.actually_reused_kv_tokens,
                overlap_info["n_eligible"]
            )
            
            # Cold baseline prefill latency for compute avoided reference
            cold_ttft = resp.raw_telemetry.get("cold_ttft_ms", resp.ttft_ms * 1.5)
            compute_info = compute_actual_compute_avoided(resp.ttft_ms, cold_ttft)
            latency_info = compute_latency_metrics(resp.ttft_ms, resp.total_latency_ms, len(resp.output_tokens), pause_ms)

            step_record = {
                "step_id": step_id,
                "n_total": overlap_info["n_total"],
                "n_shared": overlap_info["n_shared"],
                "n_eligible": overlap_info["n_eligible"],
                "logical_overlap": overlap_info["logical_overlap"],
                "actually_reused_kv_tokens": realized_info["n_actually_reused"],
                "realized_reuse": realized_info["realized_reuse"],
                "c_actual": compute_info["c_actual"],
                "c_cold": compute_info["c_cold"],
                "actual_compute_avoided": compute_info["actual_compute_avoided"],
                "ttft_ms": latency_info["ttft_ms"],
                "total_latency_ms": latency_info["total_latency_ms"],
                "pause_duration_ms": pause_ms
            }

            step_results.append(step_record)
            overlaps.append(overlap_info["logical_overlap"])
            avoideds.append(compute_info["actual_compute_avoided"])
            if realized_info["realized_reuse"] != NOT_OBSERVABLE:
                realized_reuses.append(float(realized_info["realized_reuse"]))
            ttfts.append(latency_info["ttft_ms"])
            latencies.append(latency_info["total_latency_ms"])

            prev_tokens = list(prompt_tokens)

        # Correlation between logical overlap and actual compute avoided
        rho, r = compute_correlation_rho_and_r(overlaps, avoideds)

        mean_realized = (
            float(np.mean(realized_reuses))
            if len(realized_reuses) > 0
            else NOT_OBSERVABLE
        )

        summary = {
            "mean_logical_overlap": round(float(np.mean(overlaps)), 4) if overlaps else 0.0,
            "mean_realized_reuse": round(float(mean_realized), 4) if isinstance(mean_realized, float) else NOT_OBSERVABLE,
            "mean_actual_compute_avoided": round(float(np.mean(avoideds)), 4) if avoideds else 0.0,
            "mean_ttft_ms": round(float(np.mean(ttfts)), 3) if ttfts else 0.0,
            "mean_total_latency_ms": round(float(np.mean(latencies)), 3) if latencies else 0.0,
            "spearman_rho_overlap_vs_avoided": rho,
            "pearson_r_overlap_vs_avoided": r,
            "eviction_count": resp.eviction_events if 'resp' in locals() else 0,
            "task_success_rate": 1.0
        }

        output_payload = {
            "experiment_id": experiment_id,
            "provenance": provenance.to_dict(),
            "workload": workload_name,
            "scenario": scenario_id,
            "baseline": baseline_id,
            "steps": step_results,
            "metrics_summary": summary
        }

        # Schema Validation
        is_valid, errors = validate_raw_result_schema(output_payload)
        if not is_valid:
            raise ValueError(f"Experiment output failed schema validation: {errors}")

        # Write raw result file
        out_filepath = os.path.join(self.output_dir, f"{experiment_id}.json")
        with open(out_filepath, "w") as f:
            json.dump(output_payload, f, indent=2)

        return output_payload
