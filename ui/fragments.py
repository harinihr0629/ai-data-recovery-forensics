from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import streamlit as st

from core.analyzer import analyze_file_for_session
from database.repositories import list_files


def render_recovery_workspace(session_id: int) -> None:
    st.markdown("### Upload evidence")
    uploaded = st.file_uploader("Drop evidence here", accept_multiple_files=True)

    if uploaded:
        for uploaded_file in uploaded:
            save_path = Path("storage/temp") / uploaded_file.name
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_bytes(uploaded_file.getvalue())
            analysis = analyze_file_for_session(str(save_path), session_id, uploaded_file.name)
            st.success(f"Processed {analysis['file_name']} — {analysis['signature']}")
            st.json({
                "File name": analysis["file_name"],
                "Type": analysis["file_type"],
                "Size": analysis["size_bytes"],
                "SHA-256": analysis["sha256"],
                "Signature": analysis["signature"],
                "Initial integrity": analysis["initial_integrity"],
                "Analysis status": analysis["analysis_status"],
            })

    st.markdown("### Analysis pipeline")
    pipeline = [
        ("Acquisition", True),
        ("Hashing", True),
        ("File identification", True),
        ("Metadata extraction", True),
        ("Fragment detection", True),
        ("Relationship analysis", False),
        ("AI classification", False),
        ("Reconstruction", False),
        ("Integrity validation", False),
        ("Prioritization", False),
    ]
    for label, state in pipeline:
        marker = "✓" if state else "●" if label == "Relationship analysis" else "○"
        st.write(f"{marker} {label}")

    st.markdown("### Evidence inventory")
    files = list_files(session_id)
    if not files:
        st.info("No evidence has been uploaded for this session yet.")
        return
    rows = [{
        "File ID": f.file_id,
        "File name": f.file_name,
        "Type": f.file_type,
        "Size": f.size_bytes,
        "SHA-256": f.sha256,
        "Signature": f.signature,
        "Integrity": f.initial_integrity,
        "Status": f.analysis_status,
    } for f in files]
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
