from __future__ import annotations

from typing import Any, Dict, List

from database.repositories import (
    get_file_by_id,
    get_recovered_by_id,
    get_session_stats,
    list_files,
    list_fragments,
    list_recovered,
    list_recent_audit,
)


def search_files(session_id: int, query: str = "") -> List[Dict[str, Any]]:
    files = list_files(session_id)
    q = (query or "").lower()
    if not q:
        return [{"file_id": f.file_id, "file_name": f.file_name, "file_type": f.file_type, "sha256": f.sha256} for f in files]
    return [
        {"file_id": f.file_id, "file_name": f.file_name, "file_type": f.file_type, "sha256": f.sha256}
        for f in files
        if q in f.file_name.lower() or q in f.file_type.lower() or q in (f.sha256 or "").lower()
    ]


def get_file_details(file_id: str) -> Dict[str, Any]:
    file = get_file_by_id(file_id)
    if not file:
        return {"error": "File not found."}
    return {
        "file_id": file.file_id,
        "file_name": file.file_name,
        "mime": file.mime_type,
        "size_bytes": file.size_bytes,
        "sha256": file.sha256,
        "signature": file.signature,
        "initial_integrity": file.initial_integrity,
        "status": file.analysis_status,
    }


def get_fragment_details(fragment_id: str) -> Dict[str, Any]:
    for item in list_fragments(1):
        if item.fragment_id == fragment_id:
            return {"fragment_id": item.fragment_id, "offset": item.offset, "size": item.size, "entropy": item.entropy, "confidence": item.confidence}
    return {"error": "Fragment not found."}


def find_related_fragments(session_id: int, fragment_id: str) -> List[Dict[str, Any]]:
    fragments = list_fragments(session_id)
    target = next((f for f in fragments if f.fragment_id == fragment_id), None)
    if not target:
        return []
    return [
        {"fragment_id": f.fragment_id, "offset": f.offset, "confidence": f.confidence}
        for f in fragments if f.fragment_id != fragment_id and abs(f.offset - target.offset) <= 512
    ]


def get_integrity_report(session_id: int) -> Dict[str, Any]:
    stats = get_session_stats(session_id)
    return {"avg_integrity": stats.get("avg_integrity", 0.0), "files_analyzed": stats.get("files_analyzed", 0), "corrupted": stats.get("corrupted", 0)}


def get_recovery_score(session_id: int, file_id: str | None = None) -> Dict[str, Any]:
    if file_id:
        file = get_file_by_id(file_id)
        if file:
            return {"file_id": file_id, "recoverability": float(file.initial_integrity), "integrity": float(file.initial_integrity), "confidence": 0.9}
        return {"error": "File not found."}
    stats = get_session_stats(session_id)
    return {"recoverability": stats.get("avg_recoverability", 0.0), "integrity": stats.get("avg_integrity", 0.0), "confidence": stats.get("ai_confidence", 0.0)}


def get_reconstruction_history(session_id: int) -> List[Dict[str, Any]]:
    recovered = list_recovered(session_id)
    return [{"recovered_id": r.recovered_id, "status": r.status, "confidence": r.confidence, "recoverability": r.recoverability} for r in recovered]


def search_metadata(session_id: int, query: str) -> List[Dict[str, Any]]:
    files = list_files(session_id)
    return [{"file_id": f.file_id, "file_name": f.file_name, "mime": f.mime_type} for f in files if query.lower() in f.mime_type.lower() or query.lower() in f.file_name.lower()]


def get_session_statistics(session_id: int) -> Dict[str, Any]:
    return get_session_stats(session_id)


def get_audit_history(session_id: int) -> List[Dict[str, Any]]:
    logs = list_recent_audit(session_id, limit=20)
    return [{"action": l.action, "result": l.result, "evidence_id": l.evidence_id, "created_at": str(l.created_at)} for l in logs]


def generate_recovery_summary(session_id: int) -> Dict[str, Any]:
    stats = get_session_stats(session_id)
    return {
        "summary": f"The current analysis identified {stats.get('recoverable', 0)} potentially recoverable artifacts. {stats.get('reconstructed', 0)} have sufficient evidence for reconstruction.",
        "artifacts": stats.get("recoverable", 0),
    }
