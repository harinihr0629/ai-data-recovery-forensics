from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from database.repositories import get_file_signature, sha256_file, compute_entropy


def analyze_signature(file_path: str) -> Dict[str, Any]:
    path = Path(file_path)
    payload = path.read_bytes() if path.exists() else b""
    return {
        "file_name": path.name,
        "size_bytes": len(payload),
        "sha256": sha256_file(file_path),
        "signature": get_file_signature(file_path),
        "entropy": compute_entropy(payload),
        "extension": path.suffix.lower(),
    }
