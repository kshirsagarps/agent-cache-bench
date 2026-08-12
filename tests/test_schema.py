import pytest
from agentcachebench.runner.schema_validation import validate_raw_result_schema
from agentcachebench.instrumentation.provenance import capture_provenance

def test_raw_result_schema_valid():
    prov = capture_provenance("E001")
    sample_data = {
        "experiment_id": "E001",
        "provenance": prov.to_dict(),
        "workload": "tool_use",
        "scenario": "S1",
        "baseline": "B1",
        "steps": [
            {
                "step_id": 0,
                "n_total": 1024,
                "n_shared": 0,
                "n_eligible": 0,
                "logical_overlap": 0.0,
                "actually_reused_kv_tokens": 0,
                "realized_reuse": 0.0,
                "c_actual": 12.0,
                "c_cold": 12.0,
                "actual_compute_avoided": 0.0,
                "ttft_ms": 12.0,
                "total_latency_ms": 200.0,
                "pause_duration_ms": 0.0
            }
        ],
        "metrics_summary": {
            "mean_logical_overlap": 0.0,
            "mean_realized_reuse": 0.0,
            "mean_actual_compute_avoided": 0.0,
            "mean_ttft_ms": 12.0,
            "mean_total_latency_ms": 200.0,
            "spearman_rho_overlap_vs_avoided": 0.0
        }
    }
    is_valid, errors = validate_raw_result_schema(sample_data)
    assert is_valid, f"Schema validation failed: {errors}"
