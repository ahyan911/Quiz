"""Results screen — shown at the end of a quiz."""
from __future__ import annotations

import streamlit as st

from state import go_to
from utils.quiz_logic import format_score


def render() -> None:
    r = st.session_state.last_result
    if not r:
        st.warning("No recent result.")
        if st.button("🏠 Back to Menu"):
            go_to("menu")
            st.rerun()
        return

    # Header
    st.markdown(
        f"<div class='results-header'>"
        f"<div class='results-emoji'>{r['emoji']}</div>"
        f"<div class='results-title'>{r['title']}</div>"
        f"<div class='results-subtitle'>{r['subtitle']}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # Big score circle
    st.markdown(
        f"<div class='score-circle-wrap'>"
        f"<div class='score-circle'>"
        f"<div class='score-num'>{format_score(r['score'])}</div>"
        f"<div class='score-total'>out of {r['total']}</div>"
        f"</div></div>",
        unsafe_allow_html=True,
    )

    # Stats row
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"<div class='stat-box stat-correct'><div class='stat-val'>{r['correct']}</div>"
            f"<div class='stat-lbl'>CORRECT</div></div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"<div class='stat-box stat-wrong'><div class='stat-val'>{r['wrong']}</div>"
            f"<div class='stat-lbl'>WRONG</div></div>",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"<div class='stat-box stat-skipped'><div class='stat-val'>{r['skipped']}</div>"
            f"<div class='stat-lbl'>SKIPPED</div></div>",
            unsafe_allow_html=True,
        )

    # Rank + feedback
    st.markdown(
        f"<div class='rank-display'>"
        f"<div class='rank-pill rank-{r['rank'].lower()}'>{r['rank']}</div>"
        f"<div class='rank-feedback'>{r['feedback']}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    if r["negative"] and r["penalty"] > 0:
        st.caption(f"⚠️ Includes -{r['penalty']:.2f} penalty for wrong answers")

    st.markdown("---")

    # Action buttons
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏠 Menu", use_container_width=True, key="res_menu"):
            go_to("menu")
            st.rerun()
    with c2:
        if st.button("🔄 Play Again", use_container_width=True, type="primary", key="res_again"):
            go_to("setup")
            st.rerun()
