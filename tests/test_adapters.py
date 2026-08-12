import pytest
from agentcachebench.adapters.simulated_engine import SimulatedKVEngine
from agentcachebench.adapters.base import StepRequest

def test_simulated_engine_prefix_cache_hit():
    engine = SimulatedKVEngine()
    engine.initialize({"block_size": 16, "max_cache_blocks": 100})
    engine.start_session("s1")

    # Step 1: 32 tokens
    prompt1 = [10] * 32
    req1 = StepRequest(session_id="s1", step_id=0, prompt_tokens=prompt1)
    resp1 = engine.run_step(req1)
    assert resp1.actually_reused_kv_tokens == 0

    # Step 2: 32 matching prefix tokens + 16 new tokens
    prompt2 = prompt1 + [20] * 16
    req2 = StepRequest(session_id="s1", step_id=1, prompt_tokens=prompt2)
    resp2 = engine.run_step(req2)
    assert resp2.actually_reused_kv_tokens == 32
    assert resp2.ttft_ms < resp1.ttft_ms + 10.0  # Prefill saved time
