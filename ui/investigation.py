from __future__ import annotations

import pandas as pd
import streamlit as st

from database.repositories import list_files


def render_integrity(session_id: int) -> None:
    files = list_files(session_id)
    if not files:
        st.info("No integrity records are available yet.")
        return
    rows = [{
        "File name": f.file_name,
        "Type": f.file_type,
        "Integrity": round(float(f.initial_integrity) * 100, 1),
        "Status": f.analysis_status,
    } for f in files]
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

    st.markdown("### Integrity assessment")
    for item in files[:5]:
        val = round(float(item.initial_integrity) * 100, 1)
        st.progress(min(100, max(0, val)) / 100)
        st.write(f"{item.file_name}: {val}% integrity")
