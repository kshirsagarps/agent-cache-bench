# Measurement Protocol (M3 Freeze)

## Protocol Rules
1. **Warm-up Protocol**: Run 1 unmeasured warm-up step prior to recording trajectory steps to prime hardware page allocation.
2. **Deterministic Seeds**: Set global seed = 42 for trajectory generation and mutation steps.
3. **Hardware Isolation**: Run benchmarks on isolated single-tenant GPU or documented CPU/MPS host without competing OS processes.
4. **Provenance Storage**: Every raw output file (`results/raw/*.json`) MUST contain a complete `provenance` block recording git commit, hardware, CUDA version, PyTorch version, model revision, configuration hash, and seed.
5. **Statistical Verification**: All paper claims MUST be independently recomputed by `scripts/m23_independent_audit.py` from raw JSON files before inclusion in manuscript tables or text.
