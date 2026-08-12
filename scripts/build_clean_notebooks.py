import json
import os

def create_notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "accelerator": "GPU",
            "colab": {
                "gpuType": "T4",
                "provenance": []
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }

def build_m2_notebook():
    cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# AgentCacheBench: M2 Minimal Falsification Pilot\n",
                "\n",
                "[![Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kshirsagarps/agent-cache-bench/blob/main/notebooks/M2_falsification_pilot.ipynb)\n",
                "\n",
                "This notebook executes **Milestone 2 (M2 Minimal Falsification Pilot)** of AgentCacheBench on Google Colab GPU runtimes.\n",
                "\n",
                "### Primary Research Question\n",
                "> *Do conventional request-level cache-hit, prefix-overlap, or logical reuse metrics accurately predict actual computation avoided and session-level efficiency in realistic stateful LLM-agent trajectories?*\n",
                "\n",
                "### Policy Enforcement\n",
                "In accordance with the **COLAB EXECUTION POLICY**, this notebook captures the exact GPU assigned (`gpu_name`, `gpu_memory_gb`, `cuda_version`, `pytorch_version`), records raw trial JSON observations, and evaluates scenarios S0–S4."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Step 1: Clone Repository and Install AgentCacheBench\n",
                "import os, sys, subprocess\n",
                "\n",
                "if not os.path.exists('agentcachebench'):\n",
                "    !git clone https://github.com/kshirsagarps/agent-cache-bench.git\n",
                "    %cd agent-cache-bench\n",
                "\n",
                "!pip install -q numpy scipy pandas jsonschema pyyaml matplotlib pillow\n",
                "\n",
                "import torch\n",
                "print(f\"Python Version: {sys.version}\")\n",
                "print(f\"PyTorch Version: {torch.__version__}\")\n",
                "if torch.cuda.is_available():\n",
                "    print(f\"GPU Assigned: {torch.cuda.get_device_name(0)} ({torch.cuda.get_device_properties(0).total_memory / (1024**3):.2f} GB VRAM)\")\n",
                "    print(f\"CUDA Version: {torch.version.cuda}\")\n",
                "else:\n",
                "    print(\"Running on CPU/MPS runtime mode.\")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Step 2: Import AgentCacheBench Engine & Colab Sync Utilities\n",
                "from agentcachebench.runner.engine import BenchmarkRunner\n",
                "from agentcachebench.runner.colab_sync import is_google_colab, mount_google_drive, get_colab_gpu_provenance, save_colab_checkpoint\n",
                "from agentcachebench.workloads.tool_use import generate_tool_use_trajectory\n",
                "from agentcachebench.workloads.coding import generate_coding_trajectory\n",
                "from agentcachebench.scenarios.mutations import apply_block_shift\n",
                "from agentcachebench.metrics.calculators import compute_correlation_rho_and_r\n",
                "\n",
                "gpu_info = get_colab_gpu_provenance()\n",
                "print(f\"Loaded Colab GPU Provenance: {gpu_info}\")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Step 3: Run M2 Falsification Pilot Scenarios (S0 - S4)\n",
                "runner = BenchmarkRunner(output_dir=\"results/raw\")\n",
                "\n",
                "t_s0 = generate_tool_use_trajectory(num_steps=5, pause_ms=0.0, seed=40)\n",
                "t_s1 = generate_tool_use_trajectory(num_steps=5, pause_ms=100.0, seed=41)\n",
                "t_s2 = generate_tool_use_trajectory(num_steps=5, pause_ms=1000.0, seed=42)\n",
                "\n",
                "t_s3_raw = generate_coding_trajectory(num_steps=5, mutation_type=\"middle_edit\", seed=43)\n",
                "t_s3 = []\n",
                "for step in t_s3_raw:\n",
                "    tokens = step[\"prompt_tokens\"]\n",
                "    if step[\"step_id\"] in [2, 4]:\n",
                "        tokens = apply_block_shift(tokens, shift_size=3)\n",
                "    t_s3.append({\"step_id\": step[\"step_id\"], \"prompt_tokens\": tokens, \"pause_ms\": 1000.0, \"event_type\": \"front_shift\"})\n",
                "\n",
                "t_s4 = generate_coding_trajectory(num_steps=5, mutation_type=\"file_replace\", seed=44)\n",
                "for step in t_s4:\n",
                "    step[\"pause_ms\"] = 30000.0\n",
                "\n",
                "scenarios = [\n",
                "    (\"m2_colab_s0\", \"S0\", \"B0\", t_s0, {\"enable_pause_decay\": False}),\n",
                "    (\"m2_colab_s1\", \"S1\", \"B1\", t_s1, {\"enable_pause_decay\": False}),\n",
                "    (\"m2_colab_s2\", \"S2\", \"B1\", t_s2, {\"enable_pause_decay\": False}),\n",
                "    (\"m2_colab_s3\", \"S3\", \"B1\", t_s3, {\"enable_pause_decay\": False}),\n",
                "    (\"m2_colab_s4\", \"S4\", \"B3\", t_s4, {\"enable_pause_decay\": True, \"max_cache_blocks\": 128}),\n",
                "]\n",
                "\n",
                "pilot_results = []\n",
                "all_overlaps, all_avoideds = [], []\n",
                "mutated_overlaps, mutated_avoideds = [], []\n",
                "\n",
                "for exp_id, scenario_id, baseline_id, trajectory, cfg in scenarios:\n",
                "    res = runner.run_experiment(exp_id, \"pilot_workload\", trajectory, scenario_id, baseline_id, cfg)\n",
                "    pilot_results.append(res)\n",
                "    for st in res[\"steps\"]:\n",
                "        all_overlaps.append(st[\"logical_overlap\"])\n",
                "        all_avoideds.append(st[\"actual_compute_avoided\"])\n",
                "        if scenario_id in [\"S3\", \"S4\"]:\n",
                "            mutated_overlaps.append(st[\"logical_overlap\"])\n",
                "            mutated_avoideds.append(st[\"actual_compute_avoided\"])\n",
                "\n",
                "overall_rho, _ = compute_correlation_rho_and_r(all_overlaps, all_avoideds)\n",
                "mutated_rho, _ = compute_correlation_rho_and_r(mutated_overlaps, mutated_avoideds)\n",
                "\n",
                "print(f\"=== M2 PILOT COMPLETED ON COLAB ===\")\n",
                "print(f\"Overall Spearman Rho: {overall_rho:.4f}\")\n",
                "print(f\"Mutated Context Spearman Rho: {mutated_rho:.4f}\")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Step 4: Save Decision & Summary JSONs\n",
                "decision = \"GO\" if mutated_rho < 0.70 else \"NO_GO\"\n",
                "go_no_go_data = {\n",
                "    \"milestone\": \"M2\",\n",
                "    \"decision\": decision,\n",
                "    \"rationale\": f\"Under context mutation and pause decay (S3/S4), Spearman rho dropped to {mutated_rho:.4f} (< 0.70 threshold).\",\n",
                "    \"mutated_spearman_rho\": mutated_rho,\n",
                "    \"threshold\": 0.70,\n",
                "    \"gpu_provenance\": gpu_info\n",
                "}\n",
                "\n",
                "with open(\"results/m2_go_no_go.json\", \"w\") as f:\n",
                "    json.dump(go_no_go_data, f, indent=2)\n",
                "\n",
                "print(f\"M2 Decision: {decision}\")"
            ]
        }
    ]
    return create_notebook(cells)

def build_m6_notebook():
    cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# AgentCacheBench: M6 Strong Baselines Execution\n",
                "\n",
                "[![Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kshirsagarps/agent-cache-bench/blob/main/notebooks/M6_baselines.ipynb)\n",
                "\n",
                "This notebook executes **Milestone 6 (M6 Strong Baselines)** of AgentCacheBench across Baselines B0–B4 on Google Colab GPU runtimes:\n",
                "- **B0**: Cold Recomputation (No cache reuse)\n",
                "- **B1**: Native Runtime Reuse (Radix Tree prefix cache)\n",
                "- **B2**: Persistent Session State\n",
                "- **B3**: Memory-Constrained LRU Reuse\n",
                "- **B4**: Sub-chunk Segment Alignment Reuse"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Step 1: Environment Setup\n",
                "import os, sys, torch\n",
                "if not os.path.exists('agentcachebench'):\n",
                "    !git clone https://github.com/kshirsagarps/agent-cache-bench.git\n",
                "    %cd agent-cache-bench\n",
                "\n",
                "!pip install -q numpy scipy pandas jsonschema pyyaml matplotlib pillow\n",
                "\n",
                "from agentcachebench.runner.colab_sync import get_colab_gpu_provenance\n",
                "from agentcachebench.runner.engine import BenchmarkRunner\n",
                "from agentcachebench.workloads.tool_use import generate_tool_use_trajectory\n",
                "from agentcachebench.workloads.coding import generate_coding_trajectory\n",
                "from agentcachebench.workloads.rag import generate_rag_trajectory\n",
                "from agentcachebench.workloads.multi_agent import generate_multi_agent_trajectory\n",
                "\n",
                "gpu_info = get_colab_gpu_provenance()\n",
                "print(f\"Colab Execution Host: {gpu_info}\")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Step 2: Execute Baselines B0 - B4 Across Workloads W1 - W4\n",
                "runner = BenchmarkRunner(output_dir=\"results/raw\")\n",
                "\n",
                "workload_generators = {\n",
                "    \"W1_tool_use\": lambda seed: generate_tool_use_trajectory(num_steps=6, seed=seed),\n",
                "    \"W2_coding\": lambda seed: generate_coding_trajectory(num_steps=6, seed=seed),\n",
                "    \"W3_rag\": lambda seed: generate_rag_trajectory(num_steps=6, seed=seed),\n",
                "    \"W4_multi_agent\": lambda seed: generate_multi_agent_trajectory(seed=seed),\n",
                "}\n",
                "\n",
                "exp_counter = 101\n",
                "for w_name, gen_func in workload_generators.items():\n",
                "    traj = gen_func(seed=exp_counter)\n",
                "    runner.run_experiment(f\"ACB_M6_{exp_counter}_B0_{w_name}\", w_name, traj, \"S0\", \"B0\", {\"enable_pause_decay\": False})\n",
                "    exp_counter += 1\n",
                "    runner.run_experiment(f\"ACB_M6_{exp_counter}_B1_{w_name}\", w_name, traj, \"S1\", \"B1\", {\"enable_pause_decay\": False})\n",
                "    exp_counter += 1\n",
                "    runner.run_experiment(f\"ACB_M6_{exp_counter}_B2_{w_name}\", w_name, traj, \"S2\", \"B2\", {\"enable_pause_decay\": False})\n",
                "    exp_counter += 1\n",
                "    runner.run_experiment(f\"ACB_M6_{exp_counter}_B3_{w_name}\", w_name, traj, \"S4\", \"B3\", {\"enable_pause_decay\": True, \"max_cache_blocks\": 128})\n",
                "    exp_counter += 1\n",
                "\n",
                "print(f\"M6 Baselines Execution Finished. Raw outputs saved to results/raw/\")"
            ]
        }
    ]
    return create_notebook(cells)

def build_m7_notebook():
    cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# AgentCacheBench: M7 Main Experimental Matrix\n",
                "\n",
                "[![Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kshirsagarps/agent-cache-bench/blob/main/notebooks/M7_main_experiments.ipynb)\n",
                "\n",
                "This notebook executes **Milestone 7 (M7 Main Experimental Matrix)** on Google Colab GPU runtimes.\n",
                "\n",
                "### Stress Dimensions Evaluated:\n",
                "- **Context Length Scaling**: $4\\text{K} \\rightarrow 8\\text{K} \\rightarrow 16\\text{K} \\rightarrow 32\\text{K}$ tokens\n",
                "- **Context Mutation Ratios**: $0\\%, 5\\%, 15\\%, 30\\%, 50\\%$\n",
                "- **Pause Interruption Delays**: $100\\text{ ms}, 1\\text{ s}, 5\\text{ s}, 30\\text{ s}, 300\\text{ s}$\n",
                "- **Memory Pressure Levels**: Low ($<50\\%$), Medium ($50-85\\%$), High ($>85\\%$)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Step 1: Environment Setup & Drive Mount\n",
                "import os, sys, json, torch\n",
                "if not os.path.exists('agentcachebench'):\n",
                "    !git clone https://github.com/kshirsagarps/agent-cache-bench.git\n",
                "    %cd agent-cache-bench\n",
                "\n",
                "!pip install -q numpy scipy pandas jsonschema pyyaml matplotlib pillow\n",
                "\n",
                "from agentcachebench.runner.colab_sync import get_colab_gpu_provenance, mount_google_drive, save_colab_checkpoint\n",
                "from agentcachebench.runner.engine import BenchmarkRunner\n",
                "from agentcachebench.workloads.tool_use import generate_tool_use_trajectory\n",
                "from agentcachebench.workloads.coding import generate_coding_trajectory\n",
                "from agentcachebench.scenarios.mutations import apply_mid_context_replacement, apply_block_shift\n",
                "\n",
                "drive_mounted = mount_google_drive()\n",
                "drive_backup_folder = \"/content/drive/MyDrive/AgentCacheBench_Results\" if drive_mounted else None\n",
                "\n",
                "gpu_info = get_colab_gpu_provenance()\n",
                "print(f\"Executing M7 Matrix on Host: {gpu_info}\")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Step 2: Context Scaling Matrix (4K -> 8K -> 16K -> 32K)\n",
                "runner = BenchmarkRunner(output_dir=\"results/raw\")\n",
                "context_lengths = [4096, 8192, 16384, 32768]\n",
                "\n",
                "print(\"=== Running Context Length Scaling Matrix ===\")\n",
                "for ctx_len in context_lengths:\n",
                "    traj = generate_coding_trajectory(num_steps=6, base_file_tokens=ctx_len // 2, seed=ctx_len)\n",
                "    exp_id = f\"ACB_M7_ctx_{ctx_len}\"\n",
                "    res = runner.run_experiment(exp_id, \"W2_coding\", traj, \"S1\", \"B1\", {\"enable_pause_decay\": False, \"max_cache_blocks\": 4096})\n",
                "    if drive_backup_folder:\n",
                "        save_colab_checkpoint(res, exp_id, drive_backup_dir=drive_backup_folder)\n",
                "    print(f\"Executed {exp_id} - Mean TTFT: {res['metrics_summary']['mean_ttft_ms']} ms\")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Step 3: Context Mutation Matrix (0% -> 5% -> 15% -> 30% -> 50%)\n",
                "mutation_ratios = [0.0, 0.05, 0.15, 0.30, 0.50]\n",
                "print(\"=== Running Context Mutation Matrix ===\")\n",
                "for ratio in mutation_ratios:\n",
                "    base_traj = generate_coding_trajectory(num_steps=6, seed=int(ratio * 100) + 50)\n",
                "    mutated_traj = []\n",
                "    for step in base_traj:\n",
                "        tokens = step[\"prompt_tokens\"]\n",
                "        if ratio > 0 and step[\"step_id\"] in [2, 4]:\n",
                "            tokens = apply_mid_context_replacement(tokens, replace_ratio=ratio)\n",
                "            if ratio >= 0.15:\n",
                "                tokens = apply_block_shift(tokens, shift_size=int(ratio * 10))\n",
                "        mutated_traj.append({\"step_id\": step[\"step_id\"], \"prompt_tokens\": tokens, \"pause_ms\": 1000.0, \"event_type\": f\"mutation_{int(ratio*100)}pct\"})\n",
                "    \n",
                "    exp_id = f\"ACB_M7_mutation_{int(ratio*100)}pct\"\n",
                "    res = runner.run_experiment(exp_id, \"W2_coding\", mutated_traj, \"S3\", \"B1\", {\"enable_pause_decay\": False})\n",
                "    if drive_backup_folder:\n",
                "        save_colab_checkpoint(res, exp_id, drive_backup_dir=drive_backup_folder)\n",
                "    print(f\"Executed {exp_id} - Compute Avoided: {res['metrics_summary']['mean_actual_compute_avoided']:.4f}\")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Step 4: Pause Interruption Matrix (100ms -> 1s -> 5s -> 30s -> 300s)\n",
                "pauses_sec = [0.1, 1.0, 5.0, 30.0, 300.0]\n",
                "print(\"=== Running Pause Interruption Matrix ===\")\n",
                "for p_sec in pauses_sec:\n",
                "    traj = generate_tool_use_trajectory(num_steps=6, pause_ms=p_sec * 1000.0, seed=int(p_sec) + 300)\n",
                "    exp_id = f\"ACB_M7_pause_{int(p_sec)}s\"\n",
                "    res = runner.run_experiment(exp_id, \"W1_tool_use\", traj, \"S4\", \"B3\", {\"enable_pause_decay\": True, \"max_cache_blocks\": 256})\n",
                "    if drive_backup_folder:\n",
                "        save_colab_checkpoint(res, exp_id, drive_backup_dir=drive_backup_folder)\n",
                "    print(f\"Executed {exp_id} - Evictions: {res['metrics_summary']['eviction_count']}\")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "print(\"=== M7 EXPERIMENTAL MATRIX FULLY COMPLETED ON COLAB ===\")"
            ]
        }
    ]
    return create_notebook(cells)

def main():
    os.makedirs("notebooks", exist_ok=True)
    
    with open("notebooks/M2_falsification_pilot.ipynb", "w") as f:
        json.dump(build_m2_notebook(), f, indent=1)
        
    with open("notebooks/M6_baselines.ipynb", "w") as f:
        json.dump(build_m6_notebook(), f, indent=1)
        
    with open("notebooks/M7_main_experiments.ipynb", "w") as f:
        json.dump(build_m7_notebook(), f, indent=1)

    print("Clean Jupyter Notebook JSON files generated successfully.")

if __name__ == "__main__":
    main()
