from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from database.repositories import get_session_stats


def render_dashboard(session_id: int) -> None:
    stats = get_session_stats(session_id)
    dp = {
        "label": ["Files analyzed", "Recoverable", "Reconstructed", "Partial", "Corrupted", "High priority"],
        "value": [stats.get("files_analyzed", 0), stats.get("recoverable", 0), stats.get("reconstructed", 0), stats.get("partial", 0), stats.get("corrupted", 0), stats.get("high_priority", 0)],
    }

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    metrics = [
        ("FILES ANALYZED", stats.get("files_analyzed", 0), col1),
        ("RECOVERABLE", stats.get("recoverable", 0), col2),
        ("RECONSTRUCTED", stats.get("reconstructed", 0), col3),
        ("PARTIAL", stats.get("partial", 0), col4),
        ("CORRUPTED", stats.get("corrupted", 0), col5),
        ("HIGH PRIORITY", stats.get("high_priority", 0), col6),
    ]
    for label, value, column in metrics:
        with column:
            st.metric(label, value)

    st.markdown("### Recovery status")
    summary = (
        f"The current analysis identified {stats.get('recoverable', 0)} potentially recoverable artifacts.\n\n"
        f"{stats.get('reconstructed', 0)} artifacts have sufficient structural evidence for reconstruction.\n\n"
        f"{stats.get('partial', 0)} artifacts remain partially recoverable.\n\n"
        f"{stats.get('high_priority', 0)} artifacts have been prioritized for further investigation."
    )
    st.info(summary)

    st.markdown("### Operational overview")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Average integrity", f"{stats.get('avg_integrity', 0):.1f}%")
    with c2:
        st.metric("Average recoverability", f"{stats.get('avg_recoverability', 0):.1f}%")
    with c3:
        st.metric("AI confidence", f"{stats.get('ai_confidence', 0):.1f}%")
    with c4:
        st.metric("Total fragments", stats.get("total_fragments", 0))

    df = pd.DataFrame(dp)
    fig = px.bar(df, x="label", y="value", color="label", title="Investigation distribution")
    fig.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
