from dataclasses import dataclass
from typing import Union, List, Dict, Any, Optional
from agentcachebench import NOT_OBSERVABLE

@dataclass
class StepMetricResult:
    step_id: int
    n_total: int
    n_shared: int
    n_eligible: int
    logical_overlap: float
    actually_reused_kv_tokens: Union[int, str]
    realized_reuse: Union[float, str]
    c_actual: float
    c_cold: float
    actual_compute_avoided: float
    ttft_ms: float
    total_latency_ms: float
    pause_duration_ms: float

@dataclass
class ExperimentMetricsSummary:
    mean_logical_overlap: float
    mean_realized_reuse: Union[float, str]
    mean_actual_compute_avoided: float
    mean_ttft_ms: float
    mean_total_latency_ms: float
    spearman_rho_overlap_vs_avoided: float
    pearson_r_overlap_vs_avoided: float
    eviction_count: int
    task_success_rate: float
