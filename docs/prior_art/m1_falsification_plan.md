# M1 — Falsification Plan

## Falsification Objective
Test whether the central research hypothesis can be falsified early in M2:
> *Hypothesis H1*: Spearman correlation $\rho(O, A)$ between logical context overlap $O$ and actual compute avoided $A$ drops significantly ($\rho < 0.70$) in stateful agent workloads under context mutations and pause delays, proving that request-level overlap metrics fail to predict realized efficiency.

## Failure / Pivot Threshold
If $\rho(O, A) \ge 0.95$ across all stateful scenarios (S0-S4), then conventional request-level overlap metrics *do* accurately predict compute avoided in agent workloads, and the proposed benchmarking gap is INVALID. In that case, PIVOT.
