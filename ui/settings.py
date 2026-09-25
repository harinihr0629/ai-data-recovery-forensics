from __future__ import annotations

import pandas as pd
import streamlit as st

from database.repositories import list_sessions, list_recent_audit


def render_history(session_id: int) -> None:
    sessions = list_sessions()
    if not sessions:
        st.info("No previous sessions exist yet.")
        return
    st.markdown("### Session history")
    st.dataframe(pd.DataFrame([{"Session ID": s.session_id, "Name": s.name, "Status": s.status, "Created": str(s.created_at)} for s in sessions]), use_container_width=True)

    st.markdown("### Recent audit log")
    logs = list_recent_audit(session_id, limit=20)
    if not logs:
        st.info("No recent audit records are available.")
        return
    st.dataframe(pd.DataFrame([{"Action": l.action, "Evidence": l.evidence_id, "File": l.file_id, "Result": l.result, "Timestamp": str(l.created_at)} for l in logs]), use_container_width=True)
