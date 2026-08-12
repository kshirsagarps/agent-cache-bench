import os
import json
import numpy as np
from agentcachebench.runner.engine import BenchmarkRunner
from agentcachebench.workloads.tool_use import generate_tool_use_trajectory
from agentcachebench.workloads.coding import generate_coding_trajectory
from agentcachebench.workloads.rag import generate_rag_trajectory
from agentcachebench.workloads.multi_agent import generate_multi_agent_trajectory
from agentcachebench.scenarios.mutations import apply_front_insertion, apply_block_shift
from agentcachebench.metrics.calculators import compute_correlation_rho_and_r

def run_m2_pilot():
    raw_dir = "results/raw"
    os.makedirs(raw_dir, exist_ok=True)
    runner = BenchmarkRunner(output_dir=raw_dir)

    pilot_results = []
    
    # 1. S0 Cold Recomputation
    t_s0 = generate_tool_use_trajectory(num_steps=5, pause_ms=0.0, seed=40)
    
    # 2. S1 Exact Continuation
    t_s1 = generate_tool_use_trajectory(num_steps=5, pause_ms=100.0, seed=41)
    
    # 3. S2 Tool Result Appended
    t_s2 = generate_tool_use_trajectory(num_steps=5, pause_ms=1000.0, seed=42)

    # 4. S3 Context Mutation (Front prompt shift / middle diff edit breaking prefix match)
    t_s3_raw = generate_coding_trajectory(num_steps=5, mutation_type="middle_edit", seed=43)
    # Apply front insertion at step 2 and step 4 to simulate agent injecting dynamic system variables
    t_s3 = []
    for step in t_s3_raw:
        s_id = step["step_id"]
        tokens = step["prompt_tokens"]
        if s_id in [2, 4]:
            tokens = apply_block_shift(tokens, shift_size=3) # shifts block alignment, invalidating physical KV cache
        t_s3.append({
            "step_id": s_id,
            "prompt_tokens": tokens,
            "pause_ms": 1000.0,
            "event_type": "front_shift_mutation" if s_id in [2, 4] else step["event_type"],
            "metadata": step.get("metadata", {})
        })

    # 5. S4 Pause & Cache Interruption (30s pause under severe memory pressure causing LRU eviction)
    t_s4 = generate_coding_trajectory(num_steps=5, mutation_type="file_replace", seed=44)
    for step in t_s4:
        step["pause_ms"] = 30000.0 # 30 sec inter-tool pause

    scenarios = [
        ("m2_s0", "S0", "B0", t_s0, {"enable_pause_decay": False}),
        ("m2_s1", "S1", "B1", t_s1, {"enable_pause_decay": False}),
        ("m2_s2", "S2", "B1", t_s2, {"enable_pause_decay": False}),
        ("m2_s3", "S3", "B1", t_s3, {"enable_pause_decay": False}),
        ("m2_s4", "S4", "B3", t_s4, {"enable_pause_decay": True, "max_cache_blocks": 128}),
    ]

    all_overlaps = []
    all_avoideds = []
    mutated_overlaps = []
    mutated_avoideds = []

    for exp_id, scenario_id, baseline_id, trajectory, cfg in scenarios:
        res = runner.run_experiment(
            experiment_id=exp_id,
            workload_name="pilot_workload",
            trajectory=trajectory,
            scenario_id=scenario_id,
            baseline_id=baseline_id,
            adapter_config=cfg
        )
        pilot_results.append(res)
        
        for step in res["steps"]:
            all_overlaps.append(step["logical_overlap"])
            all_avoideds.append(step["actual_compute_avoided"])
            if scenario_id in ["S3", "S4"]:
                mutated_overlaps.append(step["logical_overlap"])
                mutated_avoideds.append(step["actual_compute_avoided"])

    # Calculate Correlations
    overall_rho, overall_r = compute_correlation_rho_and_r(all_overlaps, all_avoideds)
    mutated_rho, mutated_r = compute_correlation_rho_and_r(mutated_overlaps, mutated_avoideds)

    summary_data = {
        "pilot_id": "M2_PILOT_01",
        "scenarios_evaluated": ["S0", "S1", "S2", "S3", "S4"],
        "total_steps_evaluated": len(all_overlaps),
        "overall_spearman_rho": overall_rho,
        "mutated_context_spearman_rho": mutated_rho,
        "divergence_observed": bool(mutated_rho < 0.70),
        "mean_logical_overlap": round(float(np.mean(all_overlaps)), 4),
        "mean_actual_compute_avoided": round(float(np.mean(all_avoideds)), 4)
    }

    with open("results/m2_pilot_summary.json", "w") as f:
        json.dump(summary_data, f, indent=2)

    # Go / No-Go Decision
    decision = "GO" if mutated_rho < 0.70 else "NO_GO"
    go_no_go_data = {
        "milestone": "M2",
        "decision": decision,
        "rationale": (
            f"Under context mutation and pause decay (S3/S4), Spearman rho between logical overlap and actual compute avoided "
            f"dropped to {mutated_rho:.4f} (< 0.70 threshold). Logical overlap substantially overestimates physical KV reuse when prefix modifications or pause evictions occur."
            if decision == "GO"
            else "Logical overlap perfectly predicts compute avoided; benchmarking gap not supported."
        ),
        "mutated_spearman_rho": mutated_rho,
        "threshold": 0.70
    }

    with open("results/m2_go_no_go.json", "w") as f:
        json.dump(go_no_go_data, f, indent=2)

    print(f"M2 Pilot Executed Successfully. Decision: {decision}, Mutated Rho: {mutated_rho:.4f}")

if __name__ == "__main__":
    run_m2_pilot()
