from __future__ import annotations

from typing import Dict


def assess_integrity(file_size: int, entropy: float, signature: str) -> Dict[str, float | str]:
    base = 0.82
    if "Image" in signature or "PDF" in signature:
        base += 0.05
    if file_size < 500000:
        base += 0.04
    weight = min(0.95, max(0.15, base - (entropy / 12.0) * 0.2))
    corruption = "low" if weight > 0.75 else "moderate" if weight > 0.5 else "high"
    return {
        "integrity_score": round(weight, 4),
        "corruption_level": corruption,
        "notes": f"Signature '{signature}' with entropy {entropy:.2f} indicates {corruption} corruption risk.",
    }
