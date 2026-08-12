# M1 — Novelty Statement

Existing serving systems evaluate prefix reuse using static, request-level textual prefix-overlap metrics or logical cache-hit counters. AgentCacheBench standardizes and evaluates **Realized KV-Cache Reuse ($R$)** and **Actual Compute Avoided ($A$)** in stateful LLM-agent workloads. 

Logical overlap ($O$) fails to accurately predict physical computation avoided ($A$) under realistic agent context mutations (middle insertions, diff updates) and inter-tool pause delays. AgentCacheBench provides the first benchmark suite and telemetry instrumentation to isolate, quantify, and falsify this divergence across real and simulated LLM serving engines.
