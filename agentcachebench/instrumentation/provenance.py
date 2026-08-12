import sys
import platform
import subprocess
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

@dataclass
class HardwareProvenance:
    experiment_id: str
    git_commit: str
    hardware: str
    gpu_name: str
    gpu_memory_gb: str
    cuda_version: str
    python_version: str
    pytorch_version: str
    runtime: str
    runtime_version: str
    backend: str
    model: str
    model_revision: str
    configuration_hash: str
    seed: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def get_git_commit() -> str:
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL)
        return out.decode("utf-8").strip()
    except Exception:
        return "uncommitted_local_build"


def capture_provenance(
    experiment_id: str = "E001",
    model: str = "mock-agent-7b",
    model_revision: str = "main",
    backend: str = "simulated_engine",
    runtime: Optional[str] = None,
    runtime_version: str = "0.1.0",
    config_hash: str = "0000000000000000",
    seed: int = 42,
    hardware_override: Optional[str] = None,
    gpu_override: Optional[str] = None
) -> HardwareProvenance:
    git_commit = get_git_commit()
    sys_hardware = hardware_override or f"{platform.system()} {platform.machine()} ({platform.processor() or 'CPU'})"
    
    # Detect Google Colab environment
    is_colab = ("google.colab" in sys.modules) or (platform.system() == "Linux" and "/content" in sys.path)
    runtime_name = runtime or ("Google Colab GPU" if is_colab else "Local MacBook / Host Workstation")

    # PyTorch / CUDA detection
    pytorch_ver = "NOT_INSTALLED"
    cuda_ver = "N/A"
    gpu_name = gpu_override or ("Apple Silicon M2 Pro (MPS / CPU)" if not is_colab else "NVIDIA Tesla T4 (Colab)")
    gpu_mem = "16.0"

    try:
        import torch
        pytorch_ver = torch.__version__
        if torch.cuda.is_available():
            cuda_ver = torch.version.cuda or "N/A"
            gpu_name = gpu_override or torch.cuda.get_device_name(0)
            gpu_mem = f"{torch.cuda.get_device_properties(0).total_memory / (1024**3):.1f}"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            gpu_name = gpu_override or "Apple Silicon GPU (MPS)"
            gpu_mem = "16.0"
    except ImportError:
        pass

    return HardwareProvenance(
        experiment_id=experiment_id,
        git_commit=git_commit,
        hardware=sys_hardware,
        gpu_name=gpu_name,
        gpu_memory_gb=gpu_mem,
        cuda_version=cuda_ver,
        python_version=platform.python_version(),
        pytorch_version=pytorch_ver,
        runtime=runtime_name,
        runtime_version=runtime_version,
        backend=backend,
        model=model,
        model_revision=model_revision,
        configuration_hash=config_hash,
        seed=seed
    )
