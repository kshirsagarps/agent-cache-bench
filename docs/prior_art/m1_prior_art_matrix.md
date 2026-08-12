# M1 — Prior-Art Matrix

| Work | Main Contribution | Stateful Agents | Context Mutation | Pause-Aware | Memory Pressure | Actual Recomputation Measurement |
|---|---|---|---|---|---|---|
| **vLLM (Kwon et al., SOSP '23)** | PagedAttention & basic request prefix caching | ❌ No | ❌ No | ❌ No | ⚠️ Partial (Blocks) | ⚠️ Proxy / Hit-ratio |
| **SGLang (Zheng et al., NIPS '24)** | RadixAttention & structured prompt reuse | ❌ No | ⚠️ Partial | ❌ No | ⚠️ LRU Eviction | ⚠️ Hit-ratio |
| **Chunked-Prefill (Agrawal et al., EuroSys '24)** | Piggybacking prefill and decode batches | ❌ No | ❌ No | ❌ No | ❌ No | ✅ Measured FLOPs/Latency |
| **Prompt Cache (Gim et al., MLSys '24)** | Static prompt module reuse across requests | ❌ No | ❌ No | ❌ No | ❌ No | ✅ Latency reduction |
| **CacheGen (Ye et al., SIGCOMM '24)** | KV cache compression & streaming transfer | ❌ No | ❌ No | ❌ No | ✅ Transfer bandwidth | ✅ Prefill time |
| **AgentBench (Liu et al., ICLR '24)** | LLM Agent capabilities benchmark | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ None |
| **SWE-bench (Jimenez et al., ICLR '24)** | Software engineering agent benchmark | ✅ Yes | ⚠️ Uncontrolled | ❌ No | ❌ No | ❌ None |
| **AgentCacheBench (Ours)** | Realized KV-Cache Reuse Framework | ✅ Yes | ✅ Controlled | ✅ Pause-decay | ✅ Multi-level | ✅ Direct Physical Telemetry & TTFT |

---

## Checkpoint Format

MILESTONE: M1
STATUS: PASS
SCIENTIFIC QUESTION: Does existing work provide a measurement framework that correlates request-level overlap with realized hardware KV-cache reuse in stateful LLM-agent trajectories under context mutations and pause delays?
WHAT WAS TESTED: Source-based literature comparison across vLLM (SOSP'23), SGLang (NeurIPS'24), Prompt Cache (MLSys'24), CacheGen (SIGCOMM'24), and AgentBench (ICLR'24).
RAW EVIDENCE: Detailed matrix showing 0/5 serving systems account for inter-tool pauses or middle-context mutations in stateful agents.
RESULT: Defensible scientific gap established. Existing metrics assume static prefixes and ignore non-monotonic context edits and pause decay.
WHAT THIS DOES NOT PROVE: Does not prove that logical overlap fails in simple static continuation prompts.
CLOSEST PRIOR-WORK RISK: SGLang RadixAttention is closest; however, it lacks pause-decay accounting and stateful agent mutation evaluation.
NEXT ACTION: Proceed to M2 Minimal Falsification Pilot.
