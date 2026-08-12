# M1 — Closest Work Analysis

## 1. SGLang (Zheng et al., NeurIPS 2024)
- **Mechanism**: Maintains a Radix Tree of cached tokens across requests. Matches shared prefixes from root to leaves.
- **Key Gap**: SGLang assumes immutable append-only prefix matches starting strictly from position 0. When an agent inserts tool output or diffs into the middle of the context window (context mutation), RadixAttention invalidates the entire trailing prefix. Furthermore, SGLang does not model inter-tool pause times where LRU cache blocks are evicted by competing concurrent workloads.

## 2. vLLM Automatic Prefix Caching (Kwon et al., SOSP 2023)
- **Mechanism**: Block-based hash lookup of token blocks (default block size = 16).
- **Key Gap**: PagedAttention reports logical prefix hits based on block hash equality. However, in stateful agent sessions, memory pressure causes silent physical block eviction. Textual cache-hit flags report theoretical hits, but physical execution undergoes cold prefill recomputation.

## 3. Prompt Cache (Gim et al., MLSys 2024)
- **Mechanism**: Pre-computes and caches state for reusable prompt modules.
- **Key Gap**: Static module reuse cannot handle dynamic multi-step agent trajectories with evolving file buffers, compiler logs, and tool outputs.

## Conclusion
AgentCacheBench addresses a distinct, unmeasured gap: evaluating *realized* physical KV-cache reuse vs *logical* overlap in stateful, dynamic, pause-heavy LLM agent workloads.
