import os
import pytest
from agentcachebench.workloads.tool_use import generate_tool_use_trajectory
from agentcachebench.workloads.coding import generate_coding_trajectory
from agentcachebench.workloads.rag import generate_rag_trajectory
from agentcachebench.workloads.multi_agent import generate_multi_agent_trajectory
from agentcachebench.runner.engine import BenchmarkRunner

def test_workload_generators():
    w1 = generate_tool_use_trajectory(num_steps=3)
    assert len(w1) == 3
    w2 = generate_coding_trajectory(num_steps=3)
    assert len(w2) == 3
    w3 = generate_rag_trajectory(num_steps=3)
    assert len(w3) == 3
    w4 = generate_multi_agent_trajectory()
    assert len(w4) == 4

def test_runner_execution(tmp_path):
    runner = BenchmarkRunner(output_dir=str(tmp_path))
    traj = generate_tool_use_trajectory(num_steps=3)
    res = runner.run_experiment(
        experiment_id="test_exp_01",
        workload_name="tool_use",
        trajectory=traj,
        scenario_id="S1",
        baseline_id="B1"
    )
    assert res["experiment_id"] == "test_exp_01"
    assert os.path.exists(os.path.join(tmp_path, "test_exp_01.json"))
