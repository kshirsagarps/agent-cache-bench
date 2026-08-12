# COLAB EXECUTION POLICY

## Overview & Scientific Rationale

For developers working on local laptops (e.g., Apple MacBook), running GPU-heavy LLM inference, PagedAttention KV-cache benchmarks, long-context scaling ($4\text{K} \rightarrow 32\text{K}$), and high-concurrency stress testing requires external GPU resources. 

AgentCacheBench adopts a **Hybrid Workflow Strategy**:
- **Local MacBook**: Software architecture, unit testing, workload trajectory generation, M23 independent statistical audit, figure/table generation, and IEEE LaTeX manuscript writing.
- **Google Colab GPU Runtimes**: Feasibility experiments (M2 pilot), runtime adapter testing, model inference, baseline runs (M6), and main experimental matrix execution (M7).

Google Colab provides dynamic GPU hardware resources (e.g., NVIDIA Tesla T4, V100, A100, L4). However, GPU availability and runtime lifetimes vary dynamically. To maintain scientific validity and IEEE publication standards, all experiments running on Google Colab MUST adhere strictly to the following 8 policy rules:

---

## The 8 Mandatory Policy Rules

1. **Exact GPU Recording**: Record the exact GPU assigned by the runtime (`gpu_name`, `gpu_memory_gb`, e.g., `"NVIDIA Tesla T4"`, `"15.0 GB"`).
2. **Software Provenance Recording**: Record CUDA version, PyTorch version, OS driver version, runtime environment (`"Google Colab"`), git commit hash, configuration hash, and random seed.
3. **Controlled Hardware Comparison**: Do NOT compare latency or throughput numbers across different GPU configurations without explicitly labeling the hardware difference. All primary baseline comparisons ($B_0$--$B_4$) in paper claims MUST be executed on the *same* GPU hardware configuration.
4. **Hardware-Specific Labeling**: Run primary baseline comparisons on a single documented hardware setup (e.g., Primary Benchmark: NVIDIA Tesla T4). Optional secondary GPUs (e.g., NVIDIA A100) must be categorized explicitly as generalization experiments.
5. **Granular Trial Storage**: Store every individual trial as a separate raw observation file (`results/raw/ACB_001.json`, `ACB_002.json`, ...) rather than writing aggregated CSV summaries. M23 audit recomputes metrics from raw observation files.
6. **Frequent Intermediate Checkpointing**: Save intermediate results frequently to Google Drive or remote storage to safeguard against Colab runtime timeouts or preemption.
7. **Environment vs. Provenance Distinction**: Treat Google Colab strictly as an execution environment, not as the experimental provenance itself.
8. **M24 Clean Reproduction Protocol**: M24 must reproduce the selected core benchmark matrix from a fresh environment using the documented hardware configuration.

---

## Milestone Execution Mapping

| Milestone | Execution Host | Rationale |
|---|---|---|
| **M0 — Repository & Foundation** | Local MacBook | Fast iteration, dependency locking, unit tests (`pytest`). |
| **M1 — Prior-Art & Novelty Gate** | Local MacBook | Scientific literature audit, matrix documentation. |
| **M2 — Minimal Falsification Pilot** | Google Colab GPU | Early GPU feasibility test for hypothesis $H_1$ ($\rho(O, A) < 0.70$). |
| **M3 — Benchmark Specification** | Local MacBook | Freezing metric equations, protocol rules, scenario YAMLs. |
| **M4 — Instrumentation & Adapters** | MacBook + Colab | Local mock adapter logic, Colab GPU telemetry testing. |
| **M5 — Workload Creation** | Local MacBook | Synthetic and trace-based trajectory generation. |
| **M6 — Baselines (B0–B4)** | Google Colab GPU | GPU execution of cold, native cache, and LRU baselines. |
| **M7 — Main Experiments** | Google Colab GPU / Cloud | Stress matrix ($4\text{K}\rightarrow 32\text{K}$, mutations, pause decay). |
| **M8 — Quality & Correctness** | Google Colab GPU | LLM decoding invariance & accuracy verification. |
| **M9 — M23 Independent Audit** | Local MacBook | Recomputing all manuscript numbers from raw JSONs. |
| **M10 — M24 Reproduction** | Fresh Colab Environment | End-to-end clean pipeline validation (`run_all.sh`). |
| **M11 — Reviewer Red Team** | Local MacBook | Counter-argument defense & evidence matrix compilation. |
| **M12 — Paper Generation** | Local MacBook | LaTeX manuscript compilation (`pdflatex`, `bibtex`). |

---

## Raw Result Provenance Schema

Every experiment executed on Colab MUST log the following provenance block:

```json
{
  "experiment_id": "ACB-M7-001",
  "git_commit": "eef577f64e33",
  "hardware": "Linux 5.15.120+ (x86_64)",
  "gpu_name": "NVIDIA Tesla T4",
  "gpu_memory_gb": "15.0",
  "cuda_version": "12.2",
  "python_version": "3.11.1",
  "pytorch_version": "2.2.0+cu121",
  "runtime": "Google Colab GPU",
  "runtime_version": "Colab 2026.08",
  "backend": "vllm_apc / simulated_radix",
  "model": "meta-llama/Llama-3-8b-instruct",
  "model_revision": "main",
  "configuration_hash": "a8f9c2e401b3d7e8",
  "seed": 42
}
```
