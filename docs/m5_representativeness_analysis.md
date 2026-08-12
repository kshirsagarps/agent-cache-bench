# M5 — Workload Representativeness Analysis

## Representativeness Matrix

| Workload Family | Dominant Context Event | Mutation Type | Pause Characteristic | Reusable Token Ratio |
|---|---|---|---|---|
| **W1 Tool-Use** | Tool output append | Monotonic Append | Short-Medium ($1-5\text{s}$) | $60 - 90\%$ |
| **W2 Coding** | Code edit / Diff application | Non-monotonic Mid-Edit | Medium-Long ($5-30\text{s}$) | $40 - 80\%$ |
| **W3 RAG/Research** | Doc replacement & reorder | Prefix & Segment Edit | Medium ($2-10\text{s}$) | $50 - 85\%$ |
| **W4 Multi-Agent** | Agent handoff context | Monotonic Accumulation | Long ($10-300\text{s}$) | $70 - 95\%$ |

The 4 workloads cover the full spectrum of stateful agent behaviors in production (swe-bench, devin-style coders, search agents, and multi-agent systems).
