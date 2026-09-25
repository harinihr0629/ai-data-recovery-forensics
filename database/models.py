from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint, Index
from sqlalchemy.orm import relationship

from database.connection import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128), unique=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(String(64), default="investigator")
    created_at = Column(DateTime, default=datetime.utcnow)


class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String(64), default="active")


class EvidenceSource(Base):
    __tablename__ = "evidence_sources"
    id = Column(Integer, primary_key=True, index=True)
    evidence_id = Column(String(64), unique=True, nullable=False, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    source_name = Column(String(255), nullable=False)
    description = Column(Text, default="")
    source_type = Column(String(64), default="upload")
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)


class SourceFile(Base):
    __tablename__ = "source_files"
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(String(64), unique=True, nullable=False, index=True)
    evidence_id = Column(Integer, ForeignKey("evidence_sources.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    original_name = Column(String(255), nullable=False)
    file_type = Column(String(128), default="unknown")
    mime_type = Column(String(128), default="application/octet-stream")
    size_bytes = Column(Integer, default=0)
    sha256 = Column(String(128), nullable=True)
    file_path = Column(String(500), nullable=True)
    signature = Column(String(256), nullable=True)
    initial_integrity = Column(Float, default=0.0)
    analysis_status = Column(String(64), default="queued")
    created_at = Column(DateTime, default=datetime.utcnow)


class FileSignature(Base):
    __tablename__ = "file_signatures"
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("source_files.id"), nullable=False)
    signature_name = Column(String(128), nullable=False)
    signature_value = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class FileMetadata(Base):
    __tablename__ = "file_metadata"
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("source_files.id"), nullable=False)
    key = Column(String(128), nullable=False)
    value = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Fragment(Base):
    __tablename__ = "fragments"
    id = Column(Integer, primary_key=True, index=True)
    fragment_id = Column(String(64), unique=True, nullable=False, index=True)
    file_id = Column(Integer, ForeignKey("source_files.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    offset = Column(Integer, default=0)
    size = Column(Integer, default=0)
    entropy = Column(Float, default=0.0)
    header = Column(String(128), nullable=True)
    footer = Column(String(128), nullable=True)
    relationship_score = Column(Float, default=0.0)
    confidence = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class FragmentFeature(Base):
    __tablename__ = "fragment_features"
    id = Column(Integer, primary_key=True, index=True)
    fragment_id = Column(Integer, ForeignKey("fragments.id"), nullable=False)
    feature_name = Column(String(128), nullable=False)
    feature_value = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class FragmentRelationship(Base):
    __tablename__ = "fragment_relationships"
    id = Column(Integer, primary_key=True, index=True)
    source_fragment_id = Column(Integer, ForeignKey("fragments.id"), nullable=False)
    target_fragment_id = Column(Integer, ForeignKey("fragments.id"), nullable=False)
    relationship_type = Column(String(64), default="similarity")
    score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class RecoveredFile(Base):
    __tablename__ = "recovered_files"
    id = Column(Integer, primary_key=True, index=True)
    recovered_id = Column(String(64), unique=True, nullable=False, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(128), default="unknown")
    status = Column(String(64), default="detected")
    recoverability = Column(Float, default=0.0)
    integrity = Column(Float, default=0.0)
    confidence = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class ReconstructionAttempt(Base):
    __tablename__ = "reconstruction_attempts"
    id = Column(Integer, primary_key=True, index=True)
    reconstruction_id = Column(String(64), unique=True, nullable=False, index=True)
    recovered_id = Column(Integer, ForeignKey("recovered_files.id"), nullable=False)
    method = Column(String(128), default="hybrid")
    integrity = Column(Float, default=0.0)
    confidence = Column(Float, default=0.0)
    fragments_used = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class IntegrityResult(Base):
    __tablename__ = "integrity_results"
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("source_files.id"), nullable=False)
    integrity_score = Column(Float, default=0.0)
    corruption_level = Column(String(64), default="unknown")
    analysis_notes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class RecoverabilityScore(Base):
    __tablename__ = "recoverability_scores"
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("source_files.id"), nullable=False)
    recoverability = Column(Float, default=0.0)
    integrity = Column(Float, default=0.0)
    reconstruction = Column(Float, default=0.0)
    ai_confidence = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class PriorityResult(Base):
    __tablename__ = "priority_results"
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("source_files.id"), nullable=False)
    priority = Column(String(64), default="medium")
    score = Column(Float, default=0.0)
    reasoning = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class AIAnalysis(Base):
    __tablename__ = "ai_analysis"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    entity_type = Column(String(64), default="file")
    entity_id = Column(String(64), nullable=False)
    summary = Column(Text, nullable=False)
    confidence = Column(Float, default=0.0)
    evidence = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class AIConversation(Base):
    __tablename__ = "ai_conversations"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String(64), unique=True, nullable=False, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    user_question = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    tools_used = Column(Text, default="")
    evidence_referenced = Column(Text, default="")
    confidence = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class AIAction(Base):
    __tablename__ = "ai_actions"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    action = Column(String(128), nullable=False)
    evidence = Column(Text, default="")
    confidence = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = Column(String(128), default="investigator")


class InvestigationNote(Base):
    __tablename__ = "investigation_notes"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    entity_type = Column(String(64), default="file")
    entity_id = Column(String(64), nullable=False)
    note = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class FileTag(Base):
    __tablename__ = "file_tags"
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("source_files.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(String(64), unique=True, nullable=False, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    title = Column(String(255), nullable=False)
    type = Column(String(64), default="session")
    content = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class ProcessingJob(Base):
    __tablename__ = "processing_jobs"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(64), unique=True, nullable=False, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    operation = Column(String(255), nullable=False)
    status = Column(String(64), default="queued")
    progress = Column(Float, default=0.0)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


class ProcessingLog(Base):
    __tablename__ = "processing_logs"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("processing_jobs.id"), nullable=False)
    message = Column(Text, nullable=False)
    level = Column(String(32), default="INFO")
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    user = Column(String(128), default="investigator")
    action = Column(String(128), nullable=False)
    evidence_id = Column(String(64), nullable=True)
    file_id = Column(String(64), nullable=True)
    operation = Column(String(128), nullable=True)
    previous_hash = Column(String(128), nullable=True)
    new_hash = Column(String(128), nullable=True)
    result = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class SystemSetting(Base):
    __tablename__ = "system_settings"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(128), unique=True, nullable=False)
    value = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


Base = Base

__all__ = [
    "User",
    "Session",
    "EvidenceSource",
    "SourceFile",
    "FileSignature",
    "FileMetadata",
    "Fragment",
    "FragmentFeature",
    "FragmentRelationship",
    "RecoveredFile",
    "ReconstructionAttempt",
    "IntegrityResult",
    "RecoverabilityScore",
    "PriorityResult",
    "AIAnalysis",
    "AIConversation",
    "AIAction",
    "InvestigationNote",
    "Tag",
    "FileTag",
    "Report",
    "ProcessingJob",
    "ProcessingLog",
    "AuditLog",
    "SystemSetting",
    "Base",
]
