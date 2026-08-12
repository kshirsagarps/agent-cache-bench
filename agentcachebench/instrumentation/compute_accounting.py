from typing import Dict, Any, Union
from agentcachebench import NOT_OBSERVABLE

def compute_actual_compute_avoided(
    c_actual: float,
    c_cold: float
) -> Dict[str, Any]:
    """
    Computes Actual Compute Avoided:
    A = 1 - (C_actual / C_cold)
    Where C can be prefill FLOPs, TTFT, or recomputed prefill token processing time.
    """
    if c_cold <= 0:
        return {
            "c_actual": c_actual,
            "c_cold": c_cold,
            "actual_compute_avoided": 0.0
        }
    
    avoided = 1.0 - (float(c_actual) / float(c_cold))
    # Bound avoided ratio between 0.0 and 1.0
    avoided = max(0.0, min(1.0, avoided))

    return {
        "c_actual": c_actual,
        "c_cold": c_cold,
        "actual_compute_avoided": avoided
    }


def estimate_prefill_flops(
    n_tokens: int,
    num_layers: int = 32,
    hidden_size: int = 4096,
    num_attention_heads: int = 32
) -> float:
    """
    Estimates theoretical transformer prefill FLOPs:
    FLOPs approx 2 * n_tokens * (6 * num_layers * hidden_size^2 + 2 * num_layers * n_tokens * hidden_size)
    """
    if n_tokens <= 0:
        return 0.0
    linear_flops = 12.0 * num_layers * (hidden_size ** 2) * n_tokens
    attn_flops = 4.0 * num_layers * hidden_size * (n_tokens ** 2)
    return linear_flops + attn_flops
