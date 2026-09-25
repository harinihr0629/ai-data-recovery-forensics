from __future__ import annotations

from typing import Dict


def score_recoverability(integrity: float, confidence: float, fragment_count: int) -> Dict[str, float]:
    recoverability = (integrity * 0.5) + (confidence * 0.4) + min(0.1, fragment_count / 100)
    reconstruction = (recoverability * 0.8) + (confidence * 0.2)
    return {
        "recoverability": round(min(1.0, recoverability), 4),
        "integrity": round(min(1.0, integrity), 4),
        "reconstruction": round(min(1.0, reconstruction), 4),
        "ai_confidence": round(min(1.0, confidence), 4),
    }
