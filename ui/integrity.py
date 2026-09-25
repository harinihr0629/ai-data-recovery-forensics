from __future__ import annotations

import streamlit as st

from ai.assistant import answer_question
from database.repositories import add_ai_conversation, list_ai_conversations


def render_ai_assistant(session_id: int) -> None:
    st.markdown("### AI Recovery Assistant")
    st.caption("Ask about recoverability, integrity, fragments, and evidence relationships.")

    user_input = st.text_input("Ask anything about this recovery session.", placeholder="Which files have the highest recovery potential?")
    if st.button("Ask AI") and user_input:
        response = answer_question(user_input, session_id)
        add_ai_conversation(session_id, user_input, response.get("answer", "No answer."), ", ".join(response.get("tools", [])), "session", float(response.get("confidence", 0.0)))
        st.success(response.get("answer", "No answer."))
        st.caption(f"Confidence: {float(response.get('confidence', 0.0)) * 100:.0f}%")

    conversations = list_ai_conversations(session_id)
    if conversations:
        st.markdown("### Conversation history")
        for convo in conversations:
            with st.expander(f"{convo.created_at} — {convo.user_question[:48]}"):
                st.write(convo.user_question)
                st.write(convo.ai_response)
                st.caption(f"Confidence: {convo.confidence * 100:.0f}%")
