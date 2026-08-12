from typing import List, Dict, Any, Optional
from agentcachebench.adapters.base import CacheRuntimeAdapter, StepRequest, StepResponse
from agentcachebench.adapters.simulated_engine import SimulatedKVEngine

class VLLMAdapter(CacheRuntimeAdapter):
    """
    Adapter for vLLM Automatic Prefix Caching (APC) engine.
    If vLLM is not installed or CUDA is unavailable, falls back to SimulatedKVEngine
    with explicit provenance logging.
    """
    def __init__(self):
        self.is_vllm_available: bool = False
        self.fallback_engine: Optional[SimulatedKVEngine] = None
        
        try:
            import vllm
            import torch
            if torch.cuda.is_available():
                self.is_vllm_available = True
        except ImportError:
            self.is_vllm_available = False

        if not self.is_vllm_available:
            self.fallback_engine = SimulatedKVEngine()

    def initialize(self, config: Dict[str, Any]) -> None:
        if self.fallback_engine:
            self.fallback_engine.initialize(config)
        else:
            # vLLM LLM initialization with enable_prefix_caching=True
            pass

    def start_session(self, session_id: str) -> None:
        if self.fallback_engine:
            self.fallback_engine.start_session(session_id)

    def run_step(self, request: StepRequest) -> StepResponse:
        if self.fallback_engine:
            resp = self.fallback_engine.run_step(request)
            resp.raw_telemetry["adapter_backend"] = "vllm_simulated_fallback"
            return resp
        else:
            # Real vLLM execution logic
            raise NotImplementedError("Real vLLM execution requires CUDA GPU environment.")

    def collect_metrics(self) -> Dict[str, Any]:
        if self.fallback_engine:
            return self.fallback_engine.collect_metrics()
        return {}

    def reset(self) -> None:
        if self.fallback_engine:
            self.fallback_engine.reset()
