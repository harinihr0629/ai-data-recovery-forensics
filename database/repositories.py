from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from database.connection import SessionLocal
from database.models import (
    AIAction,
    AIConversation,
    AuditLog,
    EvidenceSource,
    FileMetadata,
    FileSignature,
    Fragment,
    IntegrityResult,
    PriorityResult,
    ProcessingJob,
    RecoverabilityScore,
    RecoveredFile,
    ReconstructionAttempt,
    Session as RecoverySession,
    SourceFile,
    SystemSetting,
    Tag,
)


def get_db() -> Session:
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise


def create_default_session(name: str = "Primary Investigation Session") -> Dict[str, Any]:
    db = get_db()
    try:
        session_id = f"SESS-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"
        session = RecoverySession(session_id=session_id, name=name)
        db.add(session)
        db.commit()
        db.refresh(session)
        return {"id": session.id, "session_id": session.session_id, "name": session.name}
    finally:
        db.close()


def get_session_by_id(session_id: int) -> Optional[RecoverySession]:
    db = get_db()
    try:
        return db.query(RecoverySession).filter(RecoverySession.id == session_id).first()
    finally:
        db.close()


def list_sessions() -> List[RecoverySession]:
    db = get_db()
    try:
        return db.query(RecoverySession).order_by(RecoverySession.created_at.desc()).all()
    finally:
        db.close()


def add_audit_log(session_id: int, user: str, action: str, evidence_id: str | None, file_id: str | None, operation: str | None, previous_hash: str | None, new_hash: str | None, result: str) -> None:
    db = get_db()
    try:
        log = AuditLog(
            session_id=session_id,
            user=user,
            action=action,
            evidence_id=evidence_id,
            file_id=file_id,
            operation=operation,
            previous_hash=previous_hash,
            new_hash=new_hash,
            result=result,
        )
        db.add(log)
        db.commit()
    finally:
        db.close()


def add_system_setting(key: str, value: str) -> None:
    db = get_db()
    try:
        existing = db.query(SystemSetting).filter(SystemSetting.key == key).first()
        if existing:
            existing.value = value
        else:
            db.add(SystemSetting(key=key, value=value))
        db.commit()
    finally:
        db.close()


def get_system_setting(key: str, default: str = "") -> str:
    db = get_db()
    try:
        row = db.query(SystemSetting).filter(SystemSetting.key == key).first()
        return row.value if row else default
    finally:
        db.close()


def add_evidence_source(session_id: int, source_name: str, source_type: str = "upload", description: str = "", user_id: int | None = None) -> Dict[str, Any]:
    db = get_db()
    try:
        evidence_id = f"EV-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        evidence = EvidenceSource(
            evidence_id=evidence_id,
            session_id=session_id,
            source_name=source_name,
            source_type=source_type,
            description=description,
            user_id=user_id,
        )
        db.add(evidence)
        db.commit()
        db.refresh(evidence)
        return {"id": evidence.id, "evidence_id": evidence.evidence_id}
    finally:
        db.close()


def add_source_file(session_id: int, evidence_id: int, file_name: str, file_type: str, mime_type: str, size_bytes: int, sha256: str, file_path: str, signature: str, initial_integrity: float, analysis_status: str = "analyzed") -> Dict[str, Any]:
    db = get_db()
    try:
        file_id = f"FILE-{uuid.uuid4().hex[:8].upper()}"
        record = SourceFile(
            file_id=file_id,
            evidence_id=evidence_id,
            session_id=session_id,
            file_name=file_name,
            original_name=file_name,
            file_type=file_type,
            mime_type=mime_type,
            size_bytes=size_bytes,
            sha256=sha256,
            file_path=file_path,
            signature=signature,
            initial_integrity=initial_integrity,
            analysis_status=analysis_status,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return {"id": record.id, "file_id": record.file_id}
    finally:
        db.close()


def add_file_signature(file_record_id: int, signature_name: str, signature_value: str) -> None:
    db = get_db()
    try:
        db.add(FileSignature(file_id=file_record_id, signature_name=signature_name, signature_value=signature_value))
        db.commit()
    finally:
        db.close()


def add_file_metadata(file_record_id: int, key: str, value: str) -> None:
    db = get_db()
    try:
        db.add(FileMetadata(file_id=file_record_id, key=key, value=value))
        db.commit()
    finally:
        db.close()


def add_fragment(file_record_id: int, session_id: int, offset: int, size: int, entropy: float, header: str, footer: str, confidence: float) -> Dict[str, Any]:
    db = get_db()
    try:
        fragment_id = f"FRAG-{uuid.uuid4().hex[:8].upper()}"
        fragment = Fragment(
            fragment_id=fragment_id,
            file_id=file_record_id,
            session_id=session_id,
            offset=offset,
            size=size,
            entropy=entropy,
            header=header,
            footer=footer,
            confidence=confidence,
            relationship_score=confidence,
        )
        db.add(fragment)
        db.commit()
        db.refresh(fragment)
        return {"id": fragment.id, "fragment_id": fragment.fragment_id}
    finally:
        db.close()


def add_integrity_result(file_record_id: int, integrity_score: float, corruption_level: str, notes: str) -> None:
    db = get_db()
    try:
        db.add(IntegrityResult(file_id=file_record_id, integrity_score=integrity_score, corruption_level=corruption_level, analysis_notes=notes))
        db.commit()
    finally:
        db.close()


def add_recoverability(file_record_id: int, recoverability: float, integrity: float, reconstruction: float, ai_confidence: float) -> None:
    db = get_db()
    try:
        db.add(RecoverabilityScore(file_id=file_record_id, recoverability=recoverability, integrity=integrity, reconstruction=reconstruction, ai_confidence=ai_confidence))
        db.commit()
    finally:
        db.close()


def add_priority(file_record_id: int, priority: str, score: float, reasoning: str) -> None:
    db = get_db()
    try:
        db.add(PriorityResult(file_id=file_record_id, priority=priority, score=score, reasoning=reasoning))
        db.commit()
    finally:
        db.close()


def add_recovered_file(session_id: int, file_name: str, file_type: str, status: str, recoverability: float, integrity: float, confidence: float) -> Dict[str, Any]:
    db = get_db()
    try:
        recovered_id = f"REC-{uuid.uuid4().hex[:8].upper()}"
        record = RecoveredFile(
            recovered_id=recovered_id,
            session_id=session_id,
            file_name=file_name,
            file_type=file_type,
            status=status,
            recoverability=recoverability,
            integrity=integrity,
            confidence=confidence,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return {"id": record.id, "recovered_id": record.recovered_id}
    finally:
        db.close()


def add_reconstruction_attempt(recovered_id: int, method: str, integrity: float, confidence: float, fragments_used: str) -> None:
    db = get_db()
    try:
        reconstruction_id = f"REC-{uuid.uuid4().hex[:8].upper()}"
        db.add(ReconstructionAttempt(reconstruction_id=reconstruction_id, recovered_id=recovered_id, method=method, integrity=integrity, confidence=confidence, fragments_used=fragments_used))
        db.commit()
    finally:
        db.close()


def add_ai_conversation(session_id: int, user_question: str, ai_response: str, tools_used: str, evidence: str, confidence: float) -> None:
    db = get_db()
    try:
        conversation_id = f"AI-{uuid.uuid4().hex[:8].upper()}"
        db.add(AIConversation(conversation_id=conversation_id, session_id=session_id, user_question=user_question, ai_response=ai_response, tools_used=tools_used, evidence_referenced=evidence, confidence=confidence))
        db.commit()
    finally:
        db.close()


def add_ai_action(session_id: int, action: str, evidence: str, confidence: float) -> None:
    db = get_db()
    try:
        db.add(AIAction(session_id=session_id, action=action, evidence=evidence, confidence=confidence))
        db.commit()
    finally:
        db.close()


def get_session_stats(session_id: int) -> Dict[str, Any]:
    db = get_db()
    try:
        file_count = db.query(SourceFile).filter(SourceFile.session_id == session_id).count()
        recovered_count = db.query(RecoveredFile).filter(RecoveredFile.session_id == session_id).count()
        frag_count = db.query(Fragment).filter(Fragment.session_id == session_id).count()
        integrity_rows = db.query(IntegrityResult).join(SourceFile).filter(SourceFile.session_id == session_id).all()
        avg_integrity = sum(r.integrity_score for r in integrity_rows) / len(integrity_rows) if integrity_rows else 0.0
        recoverability_rows = db.query(RecoverabilityScore).join(SourceFile).filter(SourceFile.session_id == session_id).all()
        avg_recoverability = sum(r.recoverability for r in recoverability_rows) / len(recoverability_rows) if recoverability_rows else 0.0
        ai_conf = 0.0
        ai_rows = db.query(AIConversation).filter(AIConversation.session_id == session_id).all()
        if ai_rows:
            ai_conf = sum(r.confidence for r in ai_rows) / len(ai_rows)
        return {
            "files_analyzed": file_count,
            "recoverable": recovered_count,
            "reconstructed": max(0, recovered_count - 1),
            "partial": max(0, len(recoverability_rows) // 3),
            "corrupted": max(0, file_count - recovered_count),
            "high_priority": db.query(PriorityResult).join(SourceFile).filter(SourceFile.session_id == session_id, PriorityResult.priority.in_(["high", "critical"])).count(),
            "avg_integrity": round(avg_integrity * 100, 1),
            "avg_recoverability": round(avg_recoverability * 100, 1),
            "ai_confidence": round(ai_conf * 100, 1),
            "total_fragments": frag_count,
            "relationships_detected": frag_count,
        }
    finally:
        db.close()


def list_recent_audit(session_id: int, limit: int = 10) -> List[AuditLog]:
    db = get_db()
    try:
        return db.query(AuditLog).filter(AuditLog.session_id == session_id).order_by(AuditLog.created_at.desc()).limit(limit).all()
    finally:
        db.close()


def list_files(session_id: int) -> List[SourceFile]:
    db = get_db()
    try:
        return db.query(SourceFile).filter(SourceFile.session_id == session_id).order_by(SourceFile.created_at.desc()).all()
    finally:
        db.close()


def list_fragments(session_id: int) -> List[Fragment]:
    db = get_db()
    try:
        return db.query(Fragment).filter(Fragment.session_id == session_id).order_by(Fragment.created_at.desc()).all()
    finally:
        db.close()


def list_recovered(session_id: int) -> List[RecoveredFile]:
    db = get_db()
    try:
        return db.query(RecoveredFile).filter(RecoveredFile.session_id == session_id).order_by(RecoveredFile.created_at.desc()).all()
    finally:
        db.close()


def list_ai_conversations(session_id: int) -> List[AIConversation]:
    db = get_db()
    try:
        return db.query(AIConversation).filter(AIConversation.session_id == session_id).order_by(AIConversation.created_at.desc()).all()
    finally:
        db.close()


def get_file_by_id(file_id: str) -> Optional[SourceFile]:
    db = get_db()
    try:
        return db.query(SourceFile).filter(SourceFile.file_id == file_id).first()
    finally:
        db.close()


def get_recovered_by_id(recovered_id: str) -> Optional[RecoveredFile]:
    db = get_db()
    try:
        return db.query(RecoveredFile).filter(RecoveredFile.recovered_id == recovered_id).first()
    finally:
        db.close()

