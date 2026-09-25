from __future__ import annotations

from typing import Any, Dict, List

from database.repositories import add_evidence_source, add_source_file, list_files


class EvidenceService:
    def __init__(self, session_id: int):
        self.session_id = session_id

    def register_evidence(self, source_name: str, file_metadata: List[Dict[str, Any]]) -> List[str]:
        evidence = add_evidence_source(self.session_id, source_name, source_type="upload")
        evidence_id = evidence["id"]
        file_ids: List[str] = []
        for meta in file_metadata:
            file_record = add_source_file(
                session_id=self.session_id,
                evidence_id=evidence_id,
                file_name=meta["file_name"],
                file_type=meta["file_type"],
                mime_type=meta["mime_type"],
                size_bytes=meta["size_bytes"],
                sha256=meta["sha256"],
                file_path=meta["file_path"],
                signature=meta["signature"],
                initial_integrity=meta["initial_integrity"],
                analysis_status="queued",
            )
            file_ids.append(file_record["file_id"])
        return file_ids

    def list_session_files(self) -> List[Any]:
        return list_files(self.session_id)
