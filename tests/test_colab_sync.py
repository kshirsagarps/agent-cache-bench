import os
import json
import pytest
from agentcachebench.runner.colab_sync import is_google_colab, get_colab_gpu_provenance, save_colab_checkpoint
from agentcachebench.instrumentation.provenance import capture_provenance

def test_is_google_colab_returns_bool():
    res = is_google_colab()
    assert isinstance(res, bool)

def test_get_colab_gpu_provenance():
    prov = get_colab_gpu_provenance()
    assert "gpu_name" in prov
    assert "cuda_version" in prov
    assert "is_colab" in prov

def test_capture_provenance_runtime():
    prov = capture_provenance("EXP_TEST_01")
    assert prov.experiment_id == "EXP_TEST_01"
    assert prov.runtime is not None

def test_save_colab_checkpoint(tmp_path):
    out_dir = str(tmp_path / "raw")
    backup_dir = str(tmp_path / "drive")
    data = {"experiment_id": "TEST_COLAB_01", "status": "PASS"}
    path = save_colab_checkpoint(data, "TEST_COLAB_01", output_dir=out_dir, drive_backup_dir=backup_dir)
    assert os.path.exists(path)
    assert os.path.exists(os.path.join(backup_dir, "TEST_COLAB_01.json"))
