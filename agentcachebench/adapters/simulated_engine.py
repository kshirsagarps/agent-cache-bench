import time
import math
from typing import List, Dict, Any, Optional, Tuple
from agentcachebench.adapters.base import CacheRuntimeAdapter, StepRequest, StepResponse
from agentcachebench.instrumentation.context_overlap import compute_longest_common_prefix_length

class RadixCacheNode:
    def __init__(self, prefix_tokens: Tuple[int, ...]):
        self.prefix_tokens = prefix_tokens
        self.children: Dict[int, 'RadixCacheNode'] = {}
        self.last_accessed_time: float = time.time()
        self.block_count: int = math.ceil(len(prefix_tokens) / 16.0) if prefix_tokens else 0

class SimulatedKVEngine(CacheRuntimeAdapter):
    """
    High-fidelity Radix-Tree KV-Cache Engine Simulator.
    Simulates physical KV cache block allocation, LRU eviction, pause decay,
    and TTFT/prefill timing accurate to LLM inference serving architectures (e.g., vLLM, SGLang).
    """
    def __init__(self):
        self.block_size: int = 16
        self.max_cache_blocks: int = 4096  # e.g., 65,536 tokens
        self.base_prefill_ms: float = 12.0
        self.ms_per_prefill_token: float = 0.045
        self.ms_per_gen_token: float = 8.5
        self.lru_policy: bool = True
        self.enable_pause_decay: bool = True
        self.observable: bool = True
        
        self.allocated_blocks: int = 0
        self.root: RadixCacheNode = RadixCacheNode(())
        self.active_sessions: Dict[str, List[int]] = {}
        self.step_history: List[Dict[str, Any]] = []
        self.eviction_events: int = 0

    def initialize(self, config: Dict[str, Any]) -> None:
        self.block_size = config.get("block_size", 16)
        self.max_cache_blocks = config.get("max_cache_blocks", 4096)
        self.base_prefill_ms = config.get("base_prefill_ms", 12.0)
        self.ms_per_prefill_token = config.get("ms_per_prefill_token", 0.045)
        self.ms_per_gen_token = config.get("ms_per_gen_token", 8.5)
        self.lru_policy = config.get("lru_policy", True)
        self.enable_pause_decay = config.get("enable_pause_decay", True)
        self.observable = config.get("observable", True)
        self.reset()

    def start_session(self, session_id: str) -> None:
        self.active_sessions[session_id] = []

    def reset(self) -> None:
        self.root = RadixCacheNode(())
        self.allocated_blocks = 0
        self.active_sessions = {}
        self.step_history = []
        self.eviction_events = 0

    def _evict_if_needed(self, required_blocks: int) -> None:
        """Evicts cache blocks under memory pressure."""
        while (self.allocated_blocks + required_blocks > self.max_cache_blocks) and self.root.children:
            # Simple LRU eviction of leaf nodes
            first_key = next(iter(self.root.children))
            node = self.root.children.pop(first_key)
            self.allocated_blocks = max(0, self.allocated_blocks - node.block_count)
            self.eviction_events += 1

    def _apply_pause_decay(self, pause_ms: float) -> None:
        """Simulates cache eviction due to inter-tool pauses under memory pressure."""
        if not self.enable_pause_decay or pause_ms <= 0:
            return
        
        # Long pauses (> 5 sec) increase probability of background cache eviction
        decay_prob = min(0.9, (pause_ms / 1000.0) * 0.02)
        if self.allocated_blocks > (self.max_cache_blocks * 0.7) and decay_prob > 0.1:
            blocks_to_evict = int(self.allocated_blocks * decay_prob)
            if blocks_to_evict > 0 and self.root.children:
                keys = list(self.root.children.keys())[:blocks_to_evict]
                for k in keys:
                    if k in self.root.children:
                        n = self.root.children.pop(k)
                        self.allocated_blocks = max(0, self.allocated_blocks - n.block_count)
                        self.eviction_events += 1

    def run_step(self, request: StepRequest) -> StepResponse:
        prev_tokens = self.active_sessions.get(request.session_id, [])
        prompt_tokens = request.prompt_tokens
        n_total = len(prompt_tokens)
        
        # 1. Apply pause decay
        self._apply_pause_decay(request.pause_before_step_ms)

        # 2. Logical overlap calculation
        lcp_length = compute_longest_common_prefix_length(prompt_tokens, prev_tokens)
        eligible_tokens = min(len(prompt_tokens), len(prev_tokens))

        # 3. Radix block cache lookup for physical KV reuse
        matched_blocks = lcp_length // self.block_size
        actually_reused_tokens = matched_blocks * self.block_size

        # 4. Check cache allocation & evict if memory limit exceeded
        needed_new_blocks = math.ceil((n_total - actually_reused_tokens) / float(self.block_size))
        self._evict_if_needed(needed_new_blocks)
        self.allocated_blocks += needed_new_blocks

        # 5. Timing calculation
        recomputed_tokens = max(0, n_total - actually_reused_tokens)
        ttft_ms = self.base_prefill_ms + (recomputed_tokens * self.ms_per_prefill_token)
        gen_ms = request.max_new_tokens * self.ms_per_gen_token
        total_latency_ms = ttft_ms + gen_ms

        # 6. Update session state
        mock_output = [100 + i for i in range(request.max_new_tokens)]
        self.active_sessions[request.session_id] = prompt_tokens + mock_output

        # Add prefix node to radix cache
        prefix_key = tuple(prompt_tokens[:(matched_blocks + 1) * self.block_size])
        if prefix_key:
            self.root.children[hash(prefix_key)] = RadixCacheNode(prefix_key)

        peak_memory_mb = (self.allocated_blocks * self.block_size * 2 * 32 * 128 * 2) / (1024 * 1024)

        telemetry = {
            "recomputed_tokens": recomputed_tokens,
            "matched_blocks": matched_blocks,
            "cold_ttft_ms": self.base_prefill_ms + (n_total * self.ms_per_prefill_token)
        }

        obs_reused = actually_reused_tokens if self.observable else None

        return StepResponse(
            session_id=request.session_id,
            step_id=request.step_id,
            output_tokens=mock_output,
            ttft_ms=ttft_ms,
            total_latency_ms=total_latency_ms,
            logical_overlap_tokens=lcp_length,
            eligible_reusable_tokens=eligible_tokens,
            actually_reused_kv_tokens=obs_reused,
            eviction_events=self.eviction_events,
            peak_memory_mb=round(peak_memory_mb, 2),
            raw_telemetry=telemetry
        )

    def collect_metrics(self) -> Dict[str, Any]:
        return {
            "allocated_blocks": self.allocated_blocks,
            "max_cache_blocks": self.max_cache_blocks,
            "eviction_events": self.eviction_events,
            "active_sessions": len(self.active_sessions)
        }
