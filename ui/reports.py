from __future__ import annotations

import pandas as pd
import streamlit as st

from database.repositories import list_files


def render_investigation(session_id: int) -> None:
    search_term = st.text_input("Search artifacts")
    files = list_files(session_id)
    if not search_term:
        filt = files
    else:
        filt = [f for f in files if search_term.lower() in f.file_name.lower() or search_term.lower() in f.file_type.lower() or search_term.lower() in (f.sha256 or "").lower()]
    if not filt:
        st.info("No records matched the search criteria.")
        return
    st.dataframe(pd.DataFrame([
        {"File ID": f.file_id, "File name": f.file_name, "Type": f.file_type, "SHA-256": f.sha256, "Status": f.analysis_status}
        for f in filt
    ]), use_container_width=True)
