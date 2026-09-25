from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from database.repositories import list_fragments


def render_fragment_intelligence(session_id: int) -> None:
    fragments = list_fragments(session_id)
    if not fragments:
        st.info("No fragments have been discovered for this session yet.")
        return
    rows = [{"Fragment ID": f.fragment_id, "Offset": f.offset, "Size": f.size, "Entropy": round(f.entropy, 2), "Confidence": round(f.confidence, 2)} for f in fragments]
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

    fig = go.Figure()
    for item in fragments[:6]:
        fig.add_trace(go.Scatter(x=[item.offset, item.offset + item.size], y=[item.confidence, item.confidence], mode="lines+markers", name=item.fragment_id))
    fig.update_layout(title="Fragment relationship graph", xaxis_title="Offset", yaxis_title="Confidence")
    st.plotly_chart(fig, use_container_width=True)
