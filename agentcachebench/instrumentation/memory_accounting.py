from typing import Dict, Any

def compute_memory_metrics(
    kv_cache_allocated_mb: float,
    kv_cache_capacity_mb: float,
    eviction_count: int = 0,
    offload_count: int = 0
) -> Dict[str, Any]:
    """
    Computes KV cache memory pressure and eviction metrics.
    """
    utilization = (
        float(kv_cache_allocated_mb) / float(kv_cache_capacity_mb)
        if kv_cache_capacity_mb > 0
        else 0.0
    )
    return {
        "kv_cache_allocated_mb": kv_cache_allocated_mb,
        "kv_cache_capacity_mb": kv_cache_capacity_mb,
        "kv_cache_utilization": round(utilization, 4),
        "eviction_count": eviction_count,
        "offload_count": offload_count,
        "memory_pressure_level": "high" if utilization > 0.85 else ("medium" if utilization > 0.5 else "low")
    }
