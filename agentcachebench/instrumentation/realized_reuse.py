from typing import Union, Dict, Any, Optional
from agentcachebench import NOT_OBSERVABLE

def compute_realized_reuse(
    actually_reused_kv_tokens: Optional[int],
    eligible_tokens: int
) -> Dict[str, Any]:
    """
    Computes Realized Reuse R = N_actually_reused / N_eligible.
    If physical KV telemetry is not available, returns NOT_OBSERVABLE.
    """
    if actually_reused_kv_tokens is None or actually_reused_kv_tokens < 0:
        return {
            "n_actually_reused": NOT_OBSERVABLE,
            "n_eligible": eligible_tokens,
            "realized_reuse": NOT_OBSERVABLE,
            "is_observable": False
        }
    
    if eligible_tokens <= 0:
        realized = 0.0
    else:
        realized = min(1.0, float(actually_reused_kv_tokens) / float(eligible_tokens))
        
    return {
        "n_actually_reused": actually_reused_kv_tokens,
        "n_eligible": eligible_tokens,
        "realized_reuse": realized,
        "is_observable": True
    }
