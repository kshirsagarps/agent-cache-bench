# Metric Definitions (M3 Freeze)

## Primary Quantities

### 1. Logical Overlap ($O$)
$$O = \frac{N_{\text{shared\_set}}}{N_{\text{total}}}$$
The ratio of tokens in the current prompt that match tokens present in the previous session step context.

### 2. Longest Common Prefix Overlap ($O_{\text{LCP}}$)
$$O_{\text{LCP}} = \frac{N_{\text{LCP}}}{N_{\text{total}}}$$
The ratio of contiguous matching prefix tokens starting from index 0 between current and previous prompt.

### 3. Realized KV-Cache Reuse ($R$)
$$R = \frac{N_{\text{actually\_reused\_kv}}}{N_{\text{eligible}}}$$
Directly observed hardware/runtime KV-cache block hit count divided by theoretically eligible tokens. If telemetry is unobservable, output `NOT_OBSERVABLE`.

### 4. Actual Compute Avoided ($A$)
$$A = 1 - \frac{C_{\text{actual}}}{C_{\text{cold}}}$$
The empirical reduction in prefill time or prefill FLOPs compared to cold recomputation.

### 5. Session Efficiency ($\text{Eff}_{\text{session}}$)
$$\text{Eff}_{\text{session}} = \frac{\sum N_{\text{output\_tokens}}}{\sum T_{\text{step\_latency\_ms}} / 1000}$$
End-to-end multi-step agent token generation throughput (tokens/sec).
