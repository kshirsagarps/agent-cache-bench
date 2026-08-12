from typing import Dict, Any

def compute_latency_metrics(
    ttft_ms: float,
    total_latency_ms: float,
    output_tokens: int,
    pause_duration_ms: float = 0.0
) -> Dict[str, Any]:
    """
    Computes TTFT (Time To First Token), inter-token latency, generation throughput, and end-to-end latency.
    """
    gen_time_ms = max(0.0, total_latency_ms - ttft_ms)
    tokens_per_sec = (
        (output_tokens / (total_latency_ms / 1000.0))
        if total_latency_ms > 0
        else 0.0
    )
    inter_token_latency_ms = (
        (gen_time_ms / output_tokens)
        if output_tokens > 0
        else 0.0
    )
    return {
        "ttft_ms": round(ttft_ms, 3),
        "total_latency_ms": round(total_latency_ms, 3),
        "gen_time_ms": round(gen_time_ms, 3),
        "pause_duration_ms": round(pause_duration_ms, 3),
        "tokens_per_sec": round(tokens_per_sec, 2),
        "inter_token_latency_ms": round(inter_token_latency_ms, 3)
    }
