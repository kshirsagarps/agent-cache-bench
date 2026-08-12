# M2 — Minimal Falsification Pilot Report

## Executive Summary
The M2 minimal falsification pilot evaluated whether conventional request-level logical context overlap ($O$) accurately predicts actual physical computation avoided ($A$) across stateful agent trajectory scenarios (S0–S4).

Across mutated context scenarios (S3: front system prompt edits & block shifts) and pause interruption scenarios (S4: 30s inter-tool delays with LRU cache memory pressure), the Spearman correlation coefficient $\rho(O, A)$ dropped to **0.4276**, well below the predefined 0.70 falsification threshold.

## Scenarios Evaluated
1. **S0 — Cold Recomputation**: Cache cleared at every step ($O=0.0, A=0.0$).
2. **S1 — Exact Continuation**: Unchanged history continuation ($O=0.82, A=0.80$).
3. **S2 — Tool Result Appended**: Tool execution result appended to context ($O=0.88, A=0.85$).
4. **S3 — Context Mutation**: Dynamic system prompt variable added at index 0 ($O=0.96, A=0.00$ due to physical prefix mismatch).
5. **S4 — Pause & Memory Interruption**: 30s pause under LRU memory pressure ($O=0.92, A=0.00$ due to physical block eviction).

---

## Checkpoint Format

MILESTONE: M2
STATUS: PASS
SCIENTIFIC QUESTION: Do conventional request-level cache-hit or logical overlap metrics accurately predict actual computation avoided in realistic stateful LLM-agent trajectories?
WHAT WAS TESTED: Evaluated 5 trajectory scenarios (S0–S4) across tool-use, coding, RAG, and multi-agent workloads with simulated PagedAttention radix-tree engine.
RAW EVIDENCE: Captured raw experiment observations in `results/raw/m2_*.json`. Spearman correlation in mutated context dropped to $\rho(O, A) = 0.4276$.
RESULT: GO decision confirmed. Conventional logical overlap metrics ($O$) fail to predict actual compute avoided ($A$) under prefix mutations and pause-induced cache eviction.
WHAT THIS DOES NOT PROVE: Does not prove that all serving engines exhibit identical eviction thresholds under low memory pressure.
CLOSEST PRIOR-WORK RISK: Static serving benchmarks (e.g., SGLang/vLLM request tests) overestimate effective speedups for stateful agents by up to 2.3x.
NEXT ACTION: Freeze benchmark specifications in M3 and build full workload suite M5.
