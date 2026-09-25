from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Dict, List

from database.repositories import compute_entropy


def build_fragments(file_path: str, chunk_size: int = 256) -> List[Dict[str, Any]]:
    payload = Path(file_path).read_bytes()
    fragments = []
    for idx, start in enumerate(range(0, len(payload), chunk_size)):
        chunk = payload[start : start + chunk_size]
        fragments.append({
            "offset": start,
            "size": len(chunk),
            "header": chunk[:12].hex(),
            "footer": chunk[-12:].hex(),
            "entropy": round(compute_entropy(chunk), 4),
            "confidence": round(min(0.99, 0.5 + (len(chunk) / chunk_size) * 0.25 + (compute_entropy(chunk) / 8.0)), 4),
            "fragment_index": idx,
        })
    return fragments[:12]
