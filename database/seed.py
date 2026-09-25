from __future__ import annotations

from database.repositories import (
    add_audit_log,
    add_evidence_source,
    add_file_metadata,
    add_file_signature,
    add_fragment,
    add_integrity_result,
    add_priority,
    add_recovered_file,
    add_reconstruction_attempt,
    add_recoverability,
    add_source_file,
    list_files,
)


def seed_demo_data(session_id: int) -> None:
    if list_files(session_id):
        return

    evidence = add_evidence_source(
        session_id=session_id,
        source_name="DEMO / SYNTHETIC DATA",
        source_type="demo",
        description="Synthetic damaged dataset for recovery workflow validation.",
    )
    evidence_id = evidence["id"]

    demo_records = [
        ("damaged_jpeg.jpg", "image/jpeg", "JPEG Image", 870_000, 0.82),
        ("partial_pdf.pdf", "application/pdf", "PDF Document", 1_150_000, 0.71),
        ("broken_docx.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "Microsoft Word Document", 650_000, 0.58),
        ("unknown_binary.bin", "application/octet-stream", "Unknown Binary", 250_000, 0.42),
    ]

    for file_name, mime_type, signature, size_bytes, integrity in demo_records:
        file_record = add_source_file(
            session_id=session_id,
            evidence_id=evidence_id,
            file_name=file_name,
            file_type="media" if file_name.endswith((".jpg", ".pdf")) else "document" if file_name.endswith(".docx") else "binary",
            mime_type=mime_type,
            size_bytes=size_bytes,
            sha256=f"{abs(hash(file_name)) : 064x}",
            file_path=f"storage/evidence/{file_name}",
            signature=signature,
            initial_integrity=integrity,
            analysis_status="analyzed",
        )
        file_row_id = file_record["id"]
        add_file_signature(file_row_id, "magic", signature)
        add_file_metadata(file_row_id, "source", "Synthetic dataset")
        add_integrity_result(file_row_id, integrity, "moderate" if integrity < 0.8 else "low", "Synthetic evidence includes damaged offsets and partial structure.")
        add_recoverability(file_row_id, recoverability=0.76, integrity=integrity, reconstruction=0.81, ai_confidence=0.87)
        add_priority(file_row_id, "high" if integrity >= 0.7 else "medium", 0.81, "Potentially relevant artifact with moderate structural damage.")

        for idx in range(3):
            add_fragment(
                file_record_id=file_row_id,
                session_id=session_id,
                offset=idx * 256,
                size=256,
                entropy=4.2 + idx * 0.3,
                header=f"AA{idx:02d}",
                footer=f"BB{idx:02d}",
                confidence=0.75 + idx * 0.06,
            )

        recovered = add_recovered_file(
            session_id=session_id,
            file_name=file_name,
            file_type="reconstruction",
            status="partially recovered" if integrity < 0.8 else "recovered",
            recoverability=0.72,
            integrity=integrity,
            confidence=0.83,
        )
        add_reconstruction_attempt(
            recovered_id=recovered["id"],
            method="hybrid",
            integrity=integrity,
            confidence=0.83,
            fragments_used="fragment_1,fragment_2,fragment_3",
        )
        add_audit_log(
            session_id=session_id,
            user="investigator",
            action="analysis",
            evidence_id="DEMO-SET",
            file_id=file_record["file_id"],
            operation="signature-analysis",
            previous_hash=None,
            new_hash=file_record["file_id"],
            result="Synthetic artifact analyzed with recovery recommendation",
        )
