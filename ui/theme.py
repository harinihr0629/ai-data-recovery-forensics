from __future__ import annotations

from typing import Any, Dict, List

from ai.tools import (
    find_related_fragments,
    generate_recovery_summary,
    get_audit_history,
    get_file_details,
    get_fragment_details,
    get_integrity_report,
    get_reconstruction_history,
    get_recovery_score,
    get_session_statistics,
    search_files,
    search_metadata,
)


def answer_question(question: str, session_id: int) -> Dict[str, Any]:
    q = question.lower().strip()
    if "highest recovery" in q or "recoverable" in q:
        summary = generate_recovery_summary(session_id)
        return {"answer": summary["summary"], "confidence": 0.88, "tools": ["generate_recovery_summary"]}
    if "pdf" in q:
        files = search_metadata(session_id, "pdf")
        return {"answer": f"I found {len(files)} PDF-related entries.", "confidence": 0.82, "tools": ["search_metadata"]}
    if "corrupted image" in q or "image" in q and "corrupt" in q:
        files = search_files(session_id, "jpg")
        return {"answer": f"I found {len(files)} image candidates to inspect.", "confidence": 0.80, "tools": ["search_files"]}
    if "integrity" in q:
        report = get_integrity_report(session_id)
        return {"answer": f"Average integrity is {report.get('avg_integrity', 0)}% across {report.get('files_analyzed', 0)} files.", "confidence": 0.86, "tools": ["get_integrity_report"]}
    if "fragment" in q and "related" in q:
        return {"answer": "I can inspect fragment relationships using the fragment graph and offset similarity heuristics.", "confidence": 0.84, "tools": ["find_related_fragments"]}
    if "audit" in q:
        history = get_audit_history(session_id)
        return {"answer": f"Audit trail contains {len(history)} recent operations.", "confidence": 0.83, "tools": ["get_audit_history"]}
    stats = get_session_statistics(session_id)
    return {
        "answer": f"The active session has {stats.get('files_analyzed', 0)} analyzed files and {stats.get('recoverable', 0)} recoverable candidates. There is insufficient evidence to determine more specific conclusions without additional file analysis.",
        "confidence": 0.75,
        "tools": ["get_session_statistics"],
    }
