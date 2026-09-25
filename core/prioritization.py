from __future__ import annotations

from typing import Dict, List


def select_strategy(file_type: str, fragment_count: int) -> str:
    if file_type in {"media", "archive"} and fragment_count > 4:
        return "hybrid"
    if file_type == "document":
        return "metadata-based"
    if fragment_count <= 2:
        return "signature-based"
    return "sequential"


def reconstruct_artifact(file_name: str, file_type: str, fragment_count: int) -> Dict[str, Any]:
    strategy = select_strategy(file_type, fragment_count)
    confidence = 0.68 + min(0.25, fragment_count * 0.04)
    return {
        "reconstruction_id": f"REC-{file_name[:8].upper()}",
        "strategy": strategy,
        "confidence": round(confidence, 4),
        "fragments_used": max(1, min(8, fragment_count)),
    }
