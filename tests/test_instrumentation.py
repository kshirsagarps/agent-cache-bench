import pytest
from agentcachebench import NOT_OBSERVABLE
from agentcachebench.instrumentation.context_overlap import compute_logical_overlap
from agentcachebench.instrumentation.realized_reuse import compute_realized_reuse
from agentcachebench.instrumentation.compute_accounting import compute_actual_compute_avoided
from agentcachebench.metrics.calculators import compute_correlation_rho_and_r

def test_logical_overlap_calculation():
    tokens_prev = [1, 2, 3, 4, 5]
    tokens_curr = [1, 2, 3, 9, 10]
    res = compute_logical_overlap(tokens_curr, tokens_prev)
    assert res["n_shared"] == 3
    assert res["n_total"] == 5
    assert res["logical_overlap"] == 0.6

def test_realized_reuse_not_observable():
    res = compute_realized_reuse(None, 100)
    assert res["realized_reuse"] == NOT_OBSERVABLE
    assert res["is_observable"] is False

def test_realized_reuse_observable():
    res = compute_realized_reuse(80, 100)
    assert res["realized_reuse"] == 0.8
    assert res["is_observable"] is True

def test_compute_avoided():
    res = compute_actual_compute_avoided(c_actual=25.0, c_cold=100.0)
    assert res["actual_compute_avoided"] == 0.75

def test_correlation_calculation():
    overlaps = [0.0, 0.5, 0.9, 1.0]
    avoideds = [0.0, 0.45, 0.85, 0.95]
    rho, r = compute_correlation_rho_and_r(overlaps, avoideds)
    assert rho > 0.9
    assert r > 0.9
