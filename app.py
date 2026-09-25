from __future__ import annotations

import streamlit as st

from database.connection import init_db
from database.repositories import create_default_session, get_session_stats
from database.seed import seed_demo_data
from ui.dashboard import render_dashboard
from ui.recovery import render_recovery_workspace
from ui.fragments import render_fragment_intelligence
from ui.recovered import render_recovered_data
from ui.ai_assistant import render_ai_assistant
from ui.integrity import render_integrity
from ui.investigation import render_investigation
from ui.reports import render_reports
from ui.history import render_history
from ui.settings import render_settings
from ui.theme import apply_theme


st.set_page_config(page_title="AI Recovery Platform", layout="wide", page_icon="🛡️")
apply_theme()
init_db()

if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Dashboard"

if "active_session_id" not in st.session_state:
    session = create_default_session("Primary Investigation Session")
    st.session_state.active_session_id = session["id"]

seed_demo_data(st.session_state.active_session_id)

PAGES = {
    "Dashboard": render_dashboard,
    "Recovery": render_recovery_workspace,
    "Fragments": render_fragment_intelligence,
    "Recovered": render_recovered_data,
    "AI Recovery Assistant": render_ai_assistant,
    "Integrity": render_integrity,
    "Investigation": render_investigation,
    "Reports": render_reports,
    "History": render_history,
    "Settings": render_settings,
}

with st.sidebar:
    st.markdown("### AI Recovery Platform")
    st.caption(f"Session: {st.session_state.active_session_id}")
    selected_page = st.radio("Navigation", list(PAGES.keys()), index=0)
    st.session_state.selected_page = selected_page
    st.markdown("---")
    st.caption("Investigation Console")
    stats = get_session_stats(st.session_state.active_session_id)
    st.metric("Files analyzed", stats.get("files_analyzed", 0))
    st.metric("Recoverable", stats.get("recoverable", 0))
    st.metric("AI confidence", f"{stats.get('ai_confidence', 0):.0f}%")

main_title = st.session_state.selected_page
st.title(main_title)

if main_title in PAGES:
    PAGES[main_title](st.session_state.active_session_id)
