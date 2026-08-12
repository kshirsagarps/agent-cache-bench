import random
from typing import List, Dict, Any

def generate_multi_agent_trajectory(
    base_shared_tokens: int = 1536,
    agent_output_tokens: int = 512,
    seed: int = 42
) -> List[Dict[str, Any]]:
    """
    Generates W4 Multi-Agent workload trajectory:
    Planner -> Researcher -> Coder -> Reviewer handoff chain.
    """
    random.seed(seed)
    system_ctx = [1000 + i for i in range(base_shared_tokens)]
    trajectory = []
    current_context = list(system_ctx)

    agents = ["Planner", "Researcher", "Coder", "Reviewer"]

    for step, agent in enumerate(agents):
        if step > 0:
            output_from_prev = [2000 + (step * 1000) + i for i in range(agent_output_tokens)]
            current_context.extend(output_from_prev)

        trajectory.append({
            "step_id": step,
            "prompt_tokens": list(current_context),
            "pause_ms": 2000.0 if step > 0 else 0.0,
            "event_type": f"agent_handoff_{agent.lower()}",
            "metadata": {"agent_role": agent}
        })

    return trajectory
