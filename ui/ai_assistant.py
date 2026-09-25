from __future__ import annotations

import pandas as pd
import streamlit as st

from database.repositories import list_recovered


def render_recovered_data(session_id: int) -> None:
    recovered = list_recovered(session_id)
    if not recovered:
        st.warning("No recovered artifacts have been identified yet.")
        return
    rows = [{
        "Recovered ID": r.recovered_id,
        "File name": r.file_name,
        "Type": r.file_type,
        "Status": r.status,
        "Recoverability": round(r.recoverability * 100, 1),
        "Integrity": round(r.integrity * 100, 1),
        "Confidence": round(r.confidence * 100, 1),
    } for r in recovered]
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
