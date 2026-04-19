"""Score history screen — shows all past attempts."""
from __future__ import annotations

import streamlit as st

from state import go_to
from utils.quiz_logic import format_score


def render() -> None:
    st.markdown("#### Score History")

    history = st.session_state.history
    if not history:
        st.markdown(
            "<div class='empty-state'>"
            "<div class='empty-icon'>📋</div>"
            "<p>No quiz attempts yet. Play your first quiz to see history here!</p>"
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        for r in reversed(history):
            neg_suffix = " · ⚠️ Neg" if r.get("negative") else ""
            st.markdown(
                f"<div class='history-item'>"
                f"<div>"
                f"<div class='hi-name'>{r['name']}</div>"
                f"<div class='hi-meta'>{r['date']} · {r['difficulty'].upper()} · {r['rank']}{neg_suffix}</div>"
                f"</div>"
                f"<div class='hi-score'>{format_score(r['score'])}/{r['total']}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")
    if st.button("← Back to Menu", use_container_width=True, key="hist_back"):
        go_to("menu")
        st.rerun()
