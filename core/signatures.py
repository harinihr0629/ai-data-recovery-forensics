from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any, Dict

try:
    import magic
except Exception:  # pragma: no cover
    magic = None

from config.settings import settings


def sha256_file(path: str | os.PathLike[str]) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def get_file_signature(path: str | os.PathLike[str]) -> str:
    if magic:
        try:
            return magic.from_file(str(path))
        except Exception:
            pass
    suffix = Path(str(path)).suffix.lower()
    return {
        ".pdf": "PDF Document",
        ".jpg": "JPEG Image",
        ".jpeg": "JPEG Image",
        ".png": "PNG Image",
        ".docx": "Microsoft Word Document",
        ".xlsx": "Microsoft Excel Workbook",
        ".zip": "ZIP Archive",
        ".rar": "RAR Archive",
        ".7z": "7z Archive",
        ".txt": "Text File",
        ".bin": "Binary Data",
    }.get(suffix, "Unknown Binary")


def detect_mime(path: str | os.PathLike[str]) -> str:
    if magic:
        try:
            return magic.from_file(str(path), mime=True)
        except Exception:
            pass
    suffix = Path(str(path)).suffix.lower()
    mapping = {
        ".pdf": "application/pdf",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".zip": "application/zip",
        ".rar": "application/vnd.rar",
        ".7z": "application/x-7z-compressed",
        ".txt": "text/plain",
    }
    return mapping.get(suffix, "application/octet-stream")


def file_type_summary(path: str | os.PathLike[str]) -> str:
    suffix = Path(str(path)).suffix.lower()
    if suffix in {".pdf", ".jpg", ".jpeg", ".png", ".gif", ".bmp"}:
        return "media"
    if suffix in {".docx", ".doc", ".xlsx", ".xls"}:
        return "document"
    if suffix in {".zip", ".rar", ".7z"}:
        return "archive"
    if suffix in {".bin", ".dat"}:
        return "binary"
    return "unknown"


def safe_storage_path(original_name: str, relative_dir: str = "evidence") -> str:
    root = {
        "evidence": settings.EVIDENCE_STORAGE,
        "fragments": settings.FRAGMENT_STORAGE,
        "recovered": settings.RECOVERED_STORAGE,
        "reports": settings.REPORT_STORAGE,
        "temp": settings.TEMP_STORAGE,
    }.get(relative_dir, settings.EVIDENCE_STORAGE)
    target_dir = Path(root)
    target_dir.mkdir(parents=True, exist_ok=True)
    safe_name = Path(original_name).name.replace("/", "_").replace("\\", "_")
    return str(target_dir / safe_name)


def compute_entropy(payload: bytes) -> float:
    if not payload:
        return 0.0
    counts = {}
    for b in payload:
        counts[b] = counts.get(b, 0) + 1
    total = len(payload)
    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * (p and __import__("math").log2(p) or 0)
    return entropy


def chunk_bytes(payload: bytes, chunk_size: int = 1024) -> list[bytes]:
    return [payload[i : i + chunk_size] for i in range(0, len(payload), chunk_size)]


def simple_file_summary(path: str | os.PathLike[str]) -> Dict[str, Any]:
    file_path = str(path)
    file_size = os.path.getsize(file_path)
    return {
        "size_bytes": file_size,
        "sha256": sha256_file(file_path),
        "mime": detect_mime(file_path),
        "signature": get_file_signature(file_path),
        "type": file_type_summary(file_path),
    }
