from __future__ import annotations

import json
from datetime import datetime

import streamlit as st

from database.repositories import get_session_stats, list_files, list_recovered


def render_reports(session_id: int) -> None:
    st.markdown("### Generate report")
    stats = get_session_stats(session_id)
    report = {
        "session_id": session_id,
        "timestamp": datetime.utcnow().isoformat(),
        "summary": {
            "files_analyzed": stats.get("files_analyzed", 0),
            "recoverable": stats.get("recoverable", 0),
            "reconstructed": stats.get("reconstructed", 0),
            "high_priority": stats.get("high_priority", 0),
        },
        "artifacts": [{"name": f.file_name, "type": f.file_type, "sha256": f.sha256} for f in list_files(session_id)],
        "recovered": [{"name": r.file_name, "status": r.status, "confidence": r.confidence} for r in list_recovered(session_id)],
    }
    st.json(report)
    if st.button("Export JSON"):
        st.download_button("Download report", data=json.dumps(report, indent=2), file_name="session_report.json", mime="application/json")
