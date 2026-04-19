"""Main menu screen."""
from __future__ import annotations

import streamlit as st

from state import go_to
from utils.quiz_logic import format_score


def _menu_tile(col, icon: str, title: str, desc: str, target: str, key: str) -> None:
    """Render a single menu tile: big button + caption below."""
    with col:
        if st.button(f"{icon}  {title}", use_container_width=True, key=key):
            go_to(target)
            st.rerun()
        st.caption(desc)


def render() -> None:
    history = st.session_state.history

    # Last session banner
    if history:
        last = history[-1]
        st.markdown(
            f"<div class='last-score-banner'>"
            f"<div class='banner-label'>LAST SESSION</div>"
            f"<div class='banner-main'><strong>{last['name']}</strong> — "
            f"{format_score(last['score'])} / {last['total']} "
            f"({last['percentage']}%) "
            f"<span class='rank-pill rank-{last['rank'].lower()}'>{last['rank']}</span></div>"
            f"<div class='banner-meta'>{last['date']} · {last['difficulty'].upper()}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("")

    col1, col2 = st.columns(2)
    _menu_tile(col1, "🚀", "Start Quiz", "Choose difficulty & begin", "setup", "menu_start")
    _menu_tile(col2, "📊", "Score History", "Review past scores", "history", "menu_history")
    _menu_tile(col1, "📈", "Performance Analysis", "Detailed breakdown", "analysis", "menu_analysis")
    _menu_tile(col2, "🚪", "Exit & Reset", "Clear all data", "exit_confirm", "menu_exit")
