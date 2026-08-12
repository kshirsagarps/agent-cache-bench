# M5 — Workload Construction Documentation

## Overview
AgentCacheBench constructs 4 realistic stateful LLM-agent workload families stored under `data/trajectories/`:

1. `data/trajectories/tool_use/`: Real multi-step tool calling trajectories (LLM → Tool Call → Execution Result → LLM) with varying result payload sizes (small 128 tokens, medium 512 tokens, large 2048 tokens).
2. `data/trajectories/coding/`: Code refactoring and bug-fixing trajectories containing source code buffers, unified diffs, compiler error trace logs, and unit test execution results.
3. `data/trajectories/rag/`: Retrieval-augmented generation trajectories featuring dynamic document addition, document replacement, evidence reordering, and multi-doc synthesis.
4. `data/trajectories/multi_agent/`: Multi-agent collaborative workflows featuring sequential agent handoffs (Planner → Researcher → Coder → Reviewer) with accumulated context.
