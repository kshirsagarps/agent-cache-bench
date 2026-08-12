# M1 — Go / No-Go Report

## Status: GO

### Justification
1. **Precise Scientific Gap Established**: Prior serving frameworks (vLLM, SGLang, Prompt Cache) evaluate append-only static prompt reuse and rely on logical hit ratios. They ignore stateful agent behaviors: context mutations, multi-step history edits, and pause-induced cache decay under memory pressure.
2. **Defensible Novelty Statement**: AgentCacheBench provides the first framework measuring Realized KV-Cache Reuse ($R$) and Actual Compute Avoided ($A$) in stateful agent workloads.
3. **Falsification Criteria Defined**: Clear mathematical gate ($\rho(O, A) < 0.70$) established for M2 pilot.

### Next Step
Execute M2 Minimal Falsification Pilot across Scenarios S0–S4.
