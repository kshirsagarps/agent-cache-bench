from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class StepRequest:
    session_id: str
    step_id: int
    prompt_tokens: List[int]
    max_new_tokens: int = 32
    pause_before_step_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StepResponse:
    session_id: str
    step_id: int
    output_tokens: List[int]
    ttft_ms: float
    total_latency_ms: float
    logical_overlap_tokens: int
    eligible_reusable_tokens: int
    actually_reused_kv_tokens: Optional[int]  # None if NOT_OBSERVABLE
    eviction_events: int
    peak_memory_mb: float
    raw_telemetry: Dict[str, Any] = field(default_factory=dict)

class CacheRuntimeAdapter(ABC):
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize engine parameters, cache limits, policies."""
        pass

    @abstractmethod
    def start_session(self, session_id: str) -> None:
        """Initialize session state."""
        pass

    @abstractmethod
    def run_step(self, request: StepRequest) -> StepResponse:
        """Execute a single agent trajectory step."""
        pass

    @abstractmethod
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect aggregated engine metrics."""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset cache state."""
        pass
