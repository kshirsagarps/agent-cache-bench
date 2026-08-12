import numpy as np
from scipy import stats
from typing import List, Dict, Any, Union, Tuple
from agentcachebench import NOT_OBSERVABLE

def compute_correlation_rho_and_r(
    overlaps: List[float],
    avoided_computes: List[float]
) -> Tuple[float, float]:
    """
    Computes Spearman's rank correlation (rho) and Pearson's linear correlation (r)
    between logical overlap O and actual compute avoided A.
    """
    if len(overlaps) < 2:
        return 0.0, 0.0
    
    # Avoid zero variance warnings
    if np.all(np.array(overlaps) == overlaps[0]) or np.all(np.array(avoided_computes) == avoided_computes[0]):
        return 0.0, 0.0

    rho, _ = stats.spearmanr(overlaps, avoided_computes)
    r, _ = stats.pearsonr(overlaps, avoided_computes)

    rho_val = float(rho) if not np.isnan(rho) else 0.0
    r_val = float(r) if not np.isnan(r) else 0.0

    return round(rho_val, 4), round(r_val, 4)


def compute_summary_statistics(values: List[float]) -> Dict[str, float]:
    """Computes sample size, mean, median, std dev, 95% CI."""
    if not values:
        return {"n": 0, "mean": 0.0, "median": 0.0, "std": 0.0, "ci_95_low": 0.0, "ci_95_high": 0.0}
    
    arr = np.array(values, dtype=float)
    n = len(arr)
    mean_val = float(np.mean(arr))
    median_val = float(np.median(arr))
    std_val = float(np.std(arr, ddof=1)) if n > 1 else 0.0
    
    sem = std_val / np.sqrt(n) if n > 0 else 0.0
    ci_95 = 1.96 * sem

    return {
        "n": n,
        "mean": round(mean_val, 4),
        "median": round(median_val, 4),
        "std": round(std_val, 4),
        "ci_95_low": round(mean_val - ci_95, 4),
        "ci_95_high": round(mean_val + ci_95, 4)
    }
