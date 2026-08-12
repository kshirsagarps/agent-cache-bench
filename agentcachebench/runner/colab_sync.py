import os
import sys
import json
import subprocess
from typing import Dict, Any, Optional

def is_google_colab() -> bool:
    """Detects whether the Python code is running inside a Google Colab environment."""
    return "google.colab" in sys.modules or os.path.exists("/content")

def mount_google_drive(mount_point: str = "/content/drive") -> bool:
    """Mounts Google Drive in Colab if available."""
    if not is_google_colab():
        print("Not running in Google Colab; skipping Google Drive mount.")
        return False
    try:
        from google.colab import drive
        drive.mount(mount_point, force_remount=False)
        print(f"Google Drive mounted at {mount_point}")
        return True
    except Exception as e:
        print(f"Warning: Failed to mount Google Drive: {e}")
        return False

def get_colab_gpu_provenance() -> Dict[str, Any]:
    """
    Extracts detailed GPU hardware metadata in Google Colab environment.
    Captures GPU name, total VRAM, CUDA version, driver version, PyTorch version.
    """
    gpu_name = "N/A"
    gpu_memory_gb = "0.0"
    cuda_version = "N/A"
    driver_version = "N/A"

    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory_gb = f"{torch.cuda.get_device_properties(0).total_memory / (1024**3):.2f}"
            cuda_version = torch.version.cuda or "N/A"
    except ImportError:
        pass

    try:
        nvidia_smi = subprocess.check_output(["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"], stderr=subprocess.DEVNULL)
        driver_version = nvidia_smi.decode("utf-8").strip()
    except Exception:
        pass

    return {
        "gpu_name": gpu_name,
        "gpu_memory_gb": gpu_memory_gb,
        "cuda_version": cuda_version,
        "driver_version": driver_version,
        "is_colab": is_google_colab()
    }

def save_colab_checkpoint(
    data: Dict[str, Any],
    experiment_id: str,
    output_dir: str = "results/raw",
    drive_backup_dir: Optional[str] = None
) -> str:
    """
    Saves raw experiment result JSON file locally and optionally backs up to Google Drive.
    """
    os.makedirs(output_dir, exist_ok=True)
    local_path = os.path.join(output_dir, f"{experiment_id}.json")
    
    with open(local_path, "w") as f:
        json.dump(data, f, indent=2)
    
    if drive_backup_dir and os.path.exists(drive_backup_dir):
        os.makedirs(drive_backup_dir, exist_ok=True)
        drive_path = os.path.join(drive_backup_dir, f"{experiment_id}.json")
        with open(drive_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Checkpoint saved to local ({local_path}) and Google Drive ({drive_path})")

    return local_path
