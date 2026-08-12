# Benchmark Specification (M3 Freeze)

## 1. Workload Scope & Trajectories
AgentCacheBench incorporates four distinct stateful agent workload families:
1. **W1 — Tool Use**: Alternating LLM calls and tool executions with small/large outputs and variable execution latency.
2. **W2 — Coding**: Code generation, file edits, git diff applications, compiler error traces, and test suite execution.
3. **W3 — RAG / Research**: Multi-turn document retrieval, evidence insertion, document replacement, and evidence reordering.
4. **W4 — Multi-Agent**: Agent-to-agent state handoffs (Planner → Researcher → Coder → Reviewer) with growing cumulative context.

## 2. Benchmark Scenarios
- **S0 (Cold Recomputation)**: Zero cache reuse baseline ($B_0$).
- **S1 (Exact Continuation)**: Monotonic append-only history ($B_1$).
- **S2 (Tool Result Appended)**: Appending tool JSON/string responses ($B_1/B_2$).
- **S3 (Context Mutation)**: Non-monotonic context modifications (front edits, middle insertions, diff replacements) ($B_1/B_4$).
- **S4 (Pause / Interruption)**: Inter-tool execution delays ($100\text{ ms} - 300\text{ s}$) under memory pressure ($B_3$).

## 3. Stress Dimensions
- **Mutation Level**: $0\%, 5\%, 15\%, 30\%, 50\%$ context edits.
- **Pause Duration**: $100\text{ ms}, 1\text{ s}, 5\text{ s}, 30\text{ s}, 300\text{ s}$.
- **Memory Pressure**: Low ($<50\%$), Medium ($50-85\%$), High ($>85\%$).
- **Concurrency**: 1, 4, 8, 16 concurrent agent sessions.
