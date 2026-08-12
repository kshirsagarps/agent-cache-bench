import random
from typing import List, Dict, Any

def generate_coding_trajectory(
    num_steps: int = 6,
    base_file_tokens: int = 2048,
    mutation_type: str = "diff",  # "diff", "middle_edit", "file_replace"
    seed: int = 42
) -> List[Dict[str, Any]]:
    """
    Generates W2 Coding workload trajectory with realistic context events:
    source files, diffs, compiler errors, test execution logs, context edits.
    """
    random.seed(seed)
    base_file = [1000 + (i % 500) for i in range(base_file_tokens)]
    trajectory = []
    current_context = list(base_file)

    for step in range(num_steps):
        if step == 0:
            prompt = list(current_context)
            event = "read_source_files"
        elif step == 1:
            # Add compiler output / error trace to end
            compiler_err = [8000 + i for i in range(256)]
            current_context.extend(compiler_err)
            prompt = list(current_context)
            event = "compiler_error_log"
        elif step == 2:
            # Edit in the middle (context mutation)
            if mutation_type == "middle_edit":
                mid = len(current_context) // 2
                current_context[mid:mid+100] = [9000 + i for i in range(120)]
            else:
                diff_tokens = [7000 + i for i in range(150)]
                current_context.extend(diff_tokens)
            prompt = list(current_context)
            event = "apply_diff_or_edit"
        elif step == 3:
            # Run unit tests -> test results appended
            test_results = [6000 + i for i in range(300)]
            current_context.extend(test_results)
            prompt = list(current_context)
            event = "test_results"
        else:
            # Further code edit / replacement
            if mutation_type == "file_replace":
                # Large replacement in context prefix
                current_context[:500] = [5000 + i for i in range(500)]
            else:
                current_context.extend([3000 + i for i in range(200)])
            prompt = list(current_context)
            event = "refactor_edit"

        trajectory.append({
            "step_id": step,
            "prompt_tokens": prompt,
            "pause_ms": 1500.0,
            "event_type": event,
            "metadata": {"mutation_type": mutation_type}
        })

    return trajectory
