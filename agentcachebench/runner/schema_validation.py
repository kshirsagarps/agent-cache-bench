import jsonschema
from typing import Dict, Any, Tuple, List

RAW_RESULT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "AgentCacheBenchRawExperimentResult",
    "type": "object",
    "required": [
        "experiment_id",
        "provenance",
        "workload",
        "scenario",
        "baseline",
        "steps",
        "metrics_summary"
    ],
    "properties": {
        "experiment_id": {"type": "string"},
        "provenance": {
            "type": "object",
            "required": [
                "experiment_id",
                "git_commit",
                "hardware",
                "gpu_name",
                "gpu_memory_gb",
                "cuda_version",
                "python_version",
                "pytorch_version",
                "runtime",
                "runtime_version",
                "backend",
                "model",
                "model_revision",
                "configuration_hash",
                "seed"
            ]
        },
        "workload": {"type": "string"},
        "scenario": {"type": "string"},
        "baseline": {"type": "string"},
        "steps": {
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "step_id",
                    "n_total",
                    "n_shared",
                    "n_eligible",
                    "logical_overlap",
                    "realized_reuse",
                    "ttft_ms",
                    "total_latency_ms",
                    "actual_compute_avoided"
                ]
            }
        },
        "metrics_summary": {
            "type": "object",
            "required": [
                "mean_logical_overlap",
                "mean_realized_reuse",
                "mean_actual_compute_avoided",
                "mean_ttft_ms",
                "mean_total_latency_ms",
                "spearman_rho_overlap_vs_avoided"
            ]
        }
    }
}

def validate_raw_result_schema(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validates a raw experiment result dictionary against the authoritative schema.
    Returns (is_valid, list_of_errors).
    """
    validator = jsonschema.Draft7Validator(RAW_RESULT_SCHEMA)
    errors = [e.message for e in validator.iter_errors(data)]
    return len(errors) == 0, errors
