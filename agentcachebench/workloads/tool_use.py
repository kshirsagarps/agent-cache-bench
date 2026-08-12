import random
from typing import List, Dict, Any

def generate_tool_use_trajectory(
    num_steps: int = 6,
    base_context_tokens: int = 1024,
    tool_result_size: str = "medium",  # "small", "medium", "large"
    pause_ms: float = 1000.0,
    seed: int = 42
) -> List[Dict[str, Any]]:
    """
    Generates W1 Tool-Use trajectory steps:
    LLM -> Tool -> LLM -> Tool -> LLM
    """
    random.seed(seed)
    size_map = {"small": 128, "medium": 512, "large": 2048}
    tool_tokens_n = size_map.get(tool_result_size, 512)

    prefix_base = [random.randint(100, 10000) for _ in range(base_context_tokens)]
    trajectory = []
    accumulated_context = list(prefix_base)

    for step in range(num_steps):
        # Generate user prompt or tool result
        if step == 0:
            prompt = list(accumulated_context)
        else:
            # Append tool result to context
            tool_res = [random.randint(100, 10000) for _ in range(tool_tokens_n)]
            accumulated_context.extend(tool_res)
            prompt = list(accumulated_context)

        trajectory.append({
            "step_id": step,
            "prompt_tokens": prompt,
            "pause_ms": pause_ms if step > 0 else 0.0,
            "event_type": "initial_query" if step == 0 else "tool_result_appended",
            "metadata": {"tool_result_size": tool_result_size}
        })

    return trajectory
