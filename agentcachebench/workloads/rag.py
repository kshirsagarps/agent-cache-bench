import random
from typing import List, Dict, Any

def generate_rag_trajectory(
    num_steps: int = 6,
    doc_chunk_tokens: int = 1024,
    mutation_pattern: str = "reorder", # "append", "replace", "reorder"
    seed: int = 42
) -> List[Dict[str, Any]]:
    """
    Generates W3 RAG/Research workload trajectory:
    Retrieved document added, document replaced, evidence reordered, updated evidence.
    """
    random.seed(seed)
    system_prompt = [500 + i for i in range(256)]
    doc1 = [2000 + i for i in range(doc_chunk_tokens)]
    doc2 = [3000 + i for i in range(doc_chunk_tokens)]
    doc3 = [4000 + i for i in range(doc_chunk_tokens)]

    trajectory = []
    
    # Step 0: Query with Doc1
    c0 = system_prompt + doc1
    trajectory.append({
        "step_id": 0,
        "prompt_tokens": c0,
        "pause_ms": 500.0,
        "event_type": "retrieved_doc_added",
        "metadata": {"docs": ["doc1"]}
    })

    # Step 1: Query with Doc1 + Doc2
    c1 = system_prompt + doc1 + doc2
    trajectory.append({
        "step_id": 1,
        "prompt_tokens": c1,
        "pause_ms": 1000.0,
        "event_type": "additional_evidence_retrieved",
        "metadata": {"docs": ["doc1", "doc2"]}
    })

    # Step 2: Document mutation / reordering / replacement
    if mutation_pattern == "replace":
        # Replace doc1 with doc3 at beginning (context mutation)
        c2 = system_prompt + doc3 + doc2
        event = "document_replaced"
    elif mutation_pattern == "reorder":
        # Reorder doc2 before doc1
        c2 = system_prompt + doc2 + doc1
        event = "evidence_reordered"
    else:
        # Append doc3
        c2 = system_prompt + doc1 + doc2 + doc3
        event = "updated_evidence"

    trajectory.append({
        "step_id": 2,
        "prompt_tokens": c2,
        "pause_ms": 2000.0,
        "event_type": event,
        "metadata": {"pattern": mutation_pattern}
    })

    # Step 3: Synthesis & Follow-up
    c3 = c2 + [999 + i for i in range(128)]
    trajectory.append({
        "step_id": 3,
        "prompt_tokens": c3,
        "pause_ms": 3000.0,
        "event_type": "synthesis_step",
        "metadata": {}
    })

    return trajectory
