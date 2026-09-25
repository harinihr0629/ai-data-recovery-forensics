from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List

from database.repositories import safe_storage_path, simple_file_summary
from database.repositories import compute_entropy


def analyze_file_for_session(file_path: str, session_id: int, evidence_name: str = "upload") -> Dict[str, Any]:
    original_path = Path(file_path)
    original_name = original_path.name
    storage_name = safe_storage_path(original_name, "evidence")
    if str(original_path) != storage_name:
        if not os.path.exists(storage_name):
            os.makedirs(os.path.dirname(storage_name), exist_ok=True)
            with open(storage_name, "wb") as dst:
                dst.write(original_path.read_bytes())
    summary = simple_file_summary(storage_name)
    initial_integrity = max(0.1, min(0.98, 0.9 - (summary["size_bytes"] / 100000000) * 0.1))
    fragment_count = max(1, min(12, len(summary["sha256"]) // 8))
    return {
        "evidence_name": evidence_name,
        "storage_path": storage_name,
        "file_name": original_name,
        "file_type": summary["type"],
        "mime_type": summary["mime"],
        "size_bytes": summary["size_bytes"],
        "sha256": summary["sha256"],
        "signature": summary["signature"],
        "initial_integrity": round(initial_integrity, 4),
        "analysis_status": "analyzed",
        "fragment_count": fragment_count,
        "entropy": round(compute_entropy(Path(storage_name).read_bytes()), 4),
        "session_id": session_id,
    }
