import random
from typing import List, Tuple, Dict, Any

def apply_front_insertion(tokens: List[int], insert_tokens: List[int]) -> List[int]:
    """Inserts tokens at the very front of the context (index 0). Breaks 100% of LCP prefix cache."""
    return insert_tokens + tokens

def apply_block_shift(tokens: List[int], shift_size: int = 1) -> List[int]:
    """Inserts shift_size tokens at index 0, shifting all block boundaries by shift_size."""
    shift_padding = [999990 + i for i in range(shift_size)]
    return shift_padding + tokens

def apply_mid_context_replacement(tokens: List[int], replace_ratio: float = 0.1) -> List[int]:
    """Replaces a slice in the middle of context with new tokens."""
    n = len(tokens)
    if n == 0:
        return tokens
    start_idx = n // 4
    num_replace = int(n * replace_ratio)
    new_slice = [888880 + i for i in range(num_replace)]
    res = list(tokens)
    res[start_idx : start_idx + num_replace] = new_slice
    return res

def compute_jaccard_overlap(tokens1: List[int], tokens2: List[int]) -> float:
    """Conventional bag-of-tokens Jaccard / set overlap metric."""
    if not tokens1 or not tokens2:
        return 0.0
    s1, s2 = set(tokens1), set(tokens2)
    intersection = len(s1.intersection(s2))
    union = len(s1.union(s2))
    return float(intersection) / float(union) if union > 0 else 0.0
