import os
import json
import argparse
import numpy as np
from agentcachebench.runner.engine import BenchmarkRunner
from agentcachebench.workloads.tool_use import generate_tool_use_trajectory
from agentcachebench.workloads.coding import generate_coding_trajectory
from agentcachebench.workloads.rag import generate_rag_trajectory
from agentcachebench.workloads.multi_agent import generate_multi_agent_trajectory
from agentcachebench.scenarios.mutations import apply_block_shift, apply_mid_context_replacement

def run_main_experiments():
    raw_dir = "results/raw"
    os.makedirs(raw_dir, exist_ok=True)
    runner = BenchmarkRunner(output_dir=raw_dir)

    print("Running AgentCacheBench Main Experimental Matrix (M6/M7)...")

    experiments = []

    # 1. Baseline Comparisons across Workloads (W1-W4)
    workload_generators = {
        "W1_tool_use": lambda seed: generate_tool_use_trajectory(num_steps=6, seed=seed),
        "W2_coding": lambda seed: generate_coding_trajectory(num_steps=6, seed=seed),
        "W3_rag": lambda seed: generate_rag_trajectory(num_steps=6, seed=seed),
        "W4_multi_agent": lambda seed: generate_multi_agent_trajectory(seed=seed),
    }

    exp_counter = 1

    # Baselines B0, B1, B2, B3, B4 on W1-W4
    for w_name, gen_func in workload_generators.items():
        traj = gen_func(seed=42 + exp_counter)
        
        # B0: Cold recomputation
        exp_id = f"E{exp_counter:03d}_B0_{w_name}"
        runner.run_experiment(exp_id, w_name, traj, scenario_id="S0", baseline_id="B0", adapter_config={"enable_pause_decay": False})
        exp_counter += 1

        # B1: Native Radix Prefix Caching
        exp_id = f"E{exp_counter:03d}_B1_{w_name}"
        runner.run_experiment(exp_id, w_name, traj, scenario_id="S1", baseline_id="B1", adapter_config={"enable_pause_decay": False})
        exp_counter += 1

        # B2: Persistent Session State
        exp_id = f"E{exp_counter:03d}_B2_{w_name}"
        runner.run_experiment(exp_id, w_name, traj, scenario_id="S2", baseline_id="B2", adapter_config={"enable_pause_decay": False})
        exp_counter += 1

        # B3: Memory-Constrained LRU Reuse
        exp_id = f"E{exp_counter:03d}_B3_{w_name}"
        runner.run_experiment(exp_id, w_name, traj, scenario_id="S4", baseline_id="B3", adapter_config={"enable_pause_decay": True, "max_cache_blocks": 128})
        exp_counter += 1

    # 2. Context Mutation Stress Matrix (0%, 5%, 15%, 30%, 50%)
    mutation_ratios = [0.0, 0.05, 0.15, 0.30, 0.50]
    for ratio in mutation_ratios:
        base_traj = generate_coding_trajectory(num_steps=6, seed=100 + int(ratio * 100))
        mutated_traj = []
        for step in base_traj:
            tokens = step["prompt_tokens"]
            if ratio > 0 and step["step_id"] in [2, 4]:
                tokens = apply_mid_context_replacement(tokens, replace_ratio=ratio)
                if ratio >= 0.15:
                    tokens = apply_block_shift(tokens, shift_size=int(ratio * 10))
            mutated_traj.append({
                "step_id": step["step_id"],
                "prompt_tokens": tokens,
                "pause_ms": 1000.0,
                "event_type": f"mutation_{int(ratio*100)}pct"
            })
        
        exp_id = f"E{exp_counter:03d}_mutation_{int(ratio*100)}pct"
        runner.run_experiment(exp_id, "W2_coding", mutated_traj, scenario_id="S3", baseline_id="B1", adapter_config={"enable_pause_decay": False})
        exp_counter += 1

    # 3. Inter-Tool Pause Duration Stress Matrix (100ms, 1s, 5s, 30s, 300s)
    pauses_sec = [0.1, 1.0, 5.0, 30.0, 300.0]
    for p_sec in pauses_sec:
        base_traj = generate_tool_use_trajectory(num_steps=6, pause_ms=p_sec * 1000.0, seed=200 + int(p_sec))
        exp_id = f"E{exp_counter:03d}_pause_{int(p_sec)}s"
        runner.run_experiment(exp_id, "W1_tool_use", base_traj, scenario_id="S4", baseline_id="B3", adapter_config={"enable_pause_decay": True, "max_cache_blocks": 256})
        exp_counter += 1

    print(f"Main Experimental Matrix Executed. Total Raw Experiment Runs: {exp_counter - 1}")

if __name__ == "__main__":
    run_main_experiments()
