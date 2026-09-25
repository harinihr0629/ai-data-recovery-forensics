from __future__ import annotations

import streamlit as st


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #0b1220;
            --panel: #111b2e;
            --panel-strong: #16233c;
            --border: rgba(148, 163, 184, 0.16);
            --text: #e5eefb;
            --muted: #9fb4d3;
            --blue: #4f9cff;
            --cyan: #5eead4;
            --green: #4ade80;
            --amber: #fbbf24;
            --red: #f87171;
        }
        .stApp {
            background: linear-gradient(180deg, #0b1220 0%, #0d1728 100%);
            color: var(--text);
        }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }
        div[data-testid="stSidebar"] {
            background: rgba(17,27,46,0.92);
            border-right: 1px solid var(--border);
        }
        [data-testid="stMetricValue"] {
            font-size: 1.8rem;
            font-weight: 700;
        }
        .stCard, .element-container > div {
            border: 1px solid var(--border);
            border-radius: 16px;
            box-shadow: 0 6px 24px rgba(0,0,0,0.15);
            background: rgba(17,27,46,0.75);
        }
        h1, h2, h3 {
            color: var(--text);
        }
        .stButton > button {
            border-radius: 10px;
            border: 1px solid rgba(79,156,255,0.4);
            background: rgba(79,156,255,0.12);
            color: var(--text);
        }
        .stDownloadButton > button {
            border-radius: 10px;
            background: rgba(94,234,212,0.12);
            color: var(--text);
        }
        .status-pill {
            display: inline-block;
            padding: 0.3rem 0.6rem;
            border-radius: 999px;
            background: rgba(74,222,128,0.12);
            color: var(--green);
            font-size: 0.75rem;
            border: 1px solid rgba(74,222,128,0.15);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
