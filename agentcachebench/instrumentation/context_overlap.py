from typing import List, Sequence, Any, Dict

def compute_longest_common_prefix_length(seq1: Sequence[Any], seq2: Sequence[Any]) -> int:
    """Computes the length of the longest common prefix between two token sequences."""
    l = 0
    min_len = min(len(seq1), len(seq2))
    while l < min_len and seq1[l] == seq2[l]:
        l += 1
    return l

def compute_logical_overlap(current_tokens: Sequence[Any], previous_tokens: Sequence[Any]) -> Dict[str, Any]:
    """
    Computes logical context overlap metrics:
    1. Conventional Request-Level Textual / Token-Set Overlap (O_logical = N_shared_set / N_total)
    2. Longest Common Prefix Overlap (O_lcp = N_lcp / N_total)
    """
    n_total = len(current_tokens)
    if n_total == 0 or not previous_tokens:
        return {
            "n_total": n_total,
            "n_shared": 0,
            "n_eligible": 0,
            "logical_overlap": 0.0,
            "lcp_overlap": 0.0
        }
    
    n_lcp = compute_longest_common_prefix_length(current_tokens, previous_tokens)
    n_eligible = min(len(current_tokens), len(previous_tokens))

    # Conventional request-level logical overlap: shared tokens in context / total tokens
    # Counts tokens that exist in previous context (textual reuse capability)
    s_prev = set(previous_tokens)
    n_shared_set = sum(1 for t in current_tokens if t in s_prev)
    
    logical_overlap = float(n_shared_set) / float(n_total)
    lcp_overlap = float(n_lcp) / float(n_total)
    
    return {
        "n_total": n_total,
        "n_shared": n_shared_set,
        "n_eligible": n_eligible,
        "logical_overlap": round(logical_overlap, 4),
        "lcp_overlap": round(lcp_overlap, 4)
    }
