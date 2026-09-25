from __future__ import annotations

from typing import Dict


def prioritize_file(file_name: str, recoverability: float, integrity: float, confidence: float) -> Dict[str, any]:
    priority_score = (recoverability * 0.5) + (confidence * 0.3) + (integrity * 0.2)
    if priority_score > 0.8:
        priority = "high"
    elif priority_score > 0.6:
        priority = "medium"
    else:
        priority = "low"
    return {
        "priority": priority,
        "score": round(priority_score, 4),
        "reasoning": f"{file_name} scored {priority_score:.2f} based on recoverability, integrity, and confidence.",
    }
