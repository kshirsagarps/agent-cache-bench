import hashlib
import json
from typing import Dict, Any

def compute_config_hash(config: Dict[str, Any]) -> str:
    """Computes a deterministic SHA256 hex digest of a configuration dictionary."""
    encoded = json.dumps(config, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:16]
