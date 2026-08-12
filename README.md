# AgentCacheBench: A Benchmark and Measurement Framework for Realized KV-Cache Reuse in Stateful LLM Agents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Run Full Suite in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kshirsagarps/agent-cache-bench/blob/main/notebooks/AgentCacheBench_Full_Suite.ipynb)

AgentCacheBench is a scientific benchmark and rigorous measurement framework designed to evaluate physical Key-Value (KV) cache reuse, recomputation avoidance, and session-level performance in stateful LLM agent workloads.

## Hybrid Development & Execution Workflow

AgentCacheBench uses a **Hybrid Local + Google Colab GPU Workflow**:
- **Local MacBook / Workstation**: Code editing, unit testing (`pytest`), trajectory generation, M23 independent statistical verification, and IEEE LaTeX manuscript generation.
- **Google Colab GPU Runtimes**: GPU inference, model execution, PagedAttention/RadixTree KV-cache testing, and main experiment matrix runs.

```
Your Computer (MacBook)             Google Colab GPU Runtimes
├── Write code & refactor           ├── GPU inference & KV-cache experiments
├── Unit tests & workloads          ├── M2 falsification pilot notebook
├── M23 statistical audit     ◄─────┤ M6 baselines & M7 stress matrix
└── IEEE Paper generation   Sync    └── Export raw result JSONs with GPU provenance
```

### COLAB EXECUTION POLICY

All experiments executed on Google Colab enforce the following mandatory rules (see [`docs/colab_execution_policy.md`](docs/colab_execution_policy.md)):
1. **GPU Provenance Logging**: Automatically capture assigned `gpu_name` (e.g. `NVIDIA Tesla T4`), `gpu_memory_gb`, `cuda_version`, `pytorch_version`, `runtime: Google Colab`, `git_commit`, and `configuration_hash`.
2. **Controlled Hardware Comparison**: Primary baseline comparisons ($B_0$--$B_4$) are evaluated on identical hardware setups to avoid conflating hardware differences with algorithmic performance.
3. **Granular Trial Storage**: Save raw observations individually (`ACB_001.json`, `ACB_002.json`) to Google Drive to prevent data loss and enable M23 independent auditing.

---

## Repository Structure

```
AgentCacheBench/
├── README.md                           # Overview & Hybrid Quickstart
├── LICENSE                             # MIT License
├── pyproject.toml                      # Project metadata & dependencies
├── requirements.lock                   # Pinned dependency lock file
├── agentcachebench/                    # Core Python package
│   ├── adapters/                       # Runtime engine adapters (vLLM, SGLang, Simulated)
│   ├── instrumentation/                # Micro-telemetry & metric collectors
│   ├── metrics/                        # Formal metric definitions & calculators
│   ├── runner/                         # Benchmark runner, colab sync, hashing, schema
│   ├── scenarios/                      # Mutation & pause scenario generators
│   └── workloads/                      # Workload generators (Tool-Use, Coding, RAG, Multi-Agent)
├── configs/                            # Scenario, baseline, and stress matrix YAML configs
├── data/                               # Workload trajectory datasets
├── docs/                               # Milestone reports & specs (M1-M11, Colab Policy)
├── notebooks/                          # Google Colab Jupyter Notebooks (M2, M6, M7)
│   ├── M2_falsification_pilot.ipynb    # Colab Notebook for M2 Pilot
│   ├── M6_baselines.ipynb              # Colab Notebook for M6 Baselines
│   └── M7_main_experiments.ipynb       # Colab Notebook for M7 Stress Matrix
├── results/                            # Raw JSON observations & verified final metrics
├── scripts/                            # Independent statistical audit & plot generators
├── tests/                              # Unit test suite
├── reproducibility/                    # One-step reproduction runner (`run_all.sh`)
└── paper/                              # IEEE LaTeX paper source & compiled PDF
```

---

## Quick Start

### 1. Local Setup & Unit Tests

```bash
git clone https://github.com/agentcachebench/agentcachebench.git
cd agentcachebench
pip install -e .
PYTHONPATH=. python3 -m pytest tests/
```

### 2. Run Experiments on Google Colab

Open one of the pre-configured Colab notebooks in `notebooks/`:
- [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kshirsagarps/agent-cache-bench/blob/main/notebooks/M2_falsification_pilot.ipynb) **`M2_falsification_pilot.ipynb`**
- [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kshirsagarps/agent-cache-bench/blob/main/notebooks/M6_baselines.ipynb) **`M6_baselines.ipynb`**
- [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kshirsagarps/agent-cache-bench/blob/main/notebooks/M7_main_experiments.ipynb) **`M7_main_experiments.ipynb`**

### 3. Local Audit & Paper Generation

```bash
# Run M23 Independent Statistical Audit on raw results synced from Colab
PYTHONPATH=. python3 scripts/m23_independent_audit.py

# Run full reproduction pipeline
bash reproducibility/run_all.sh
```

---

## Citation

If you use AgentCacheBench in your research, please cite:

```bibtex
@article{agentcachebench2026,
  title={AgentCacheBench: A Benchmark and Measurement Framework for Realized KV-Cache Reuse in Stateful LLM Agents},
  author={AgentCacheBench Team},
  journal={IEEE Transactions on Software Engineering / IEEE Computer Society},
  year={2026}
}
```
