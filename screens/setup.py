"""Quiz setup screen — player name, difficulty, negative marking toggle."""
from __future__ import annotations

import streamlit as st

from state import go_to, reset_quiz_progress, start_question_timer
from utils.quiz_logic import select_questions


DIFFICULTIES = [
    ("easy",   "🌱", "Easy",   "5 questions"),
    ("medium", "⚡", "Medium", "5 questions"),
    ("hard",   "🔥", "Hard",   "5 questions"),
    ("mixed",  "🎲", "Mixed",  "Random 10 questions"),
]


def _diff_button(col, diff_id: str, icon: str, label: str, desc: str) -> None:
    with col:
        is_selected = st.session_state.difficulty == diff_id
        if st.button(
            f"{icon}  {label}",
            use_container_width=True,
            type="primary" if is_selected else "secondary",
            key=f"diff_{diff_id}",
        ):
            st.session_state.difficulty = diff_id
            st.rerun()
        st.caption(desc)


def render() -> None:
    st.markdown("#### New Quiz Setup")

    # Name input
    name = st.text_input(
        "Your Name",
        value=st.session_state.player_name,
        max_chars=30,
        placeholder="Enter your name...",
        key="setup_name_input",
    )

    st.markdown("**Difficulty Level**")

    cols = st.columns(3)
    for i, (diff_id, icon, label, desc) in enumerate(DIFFICULTIES[:3]):
        _diff_button(cols[i], diff_id, icon, label, desc)

    # Mixed button full-width below
    diff_id, icon, label, desc = DIFFICULTIES[3]
    is_selected = st.session_state.difficulty == diff_id
    if st.button(
        f"{icon}  Mixed (All Levels) — {desc}",
        use_container_width=True,
        type="primary" if is_selected else "secondary",
        key=f"diff_{diff_id}",
    ):
        st.session_state.difficulty = diff_id
        st.rerun()

    st.markdown("---")

    # Negative marking toggle
    st.session_state.negative_marking = st.toggle(
        "⚠️ **Negative Marking** — Deduct 0.25 marks for each wrong answer",
        value=st.session_state.negative_marking,
        key="setup_neg_toggle",
    )

    st.markdown("---")

    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True, key="setup_back"):
            go_to("menu")
            st.rerun()
    with col2:
        if st.button("Start Quiz 🚀", use_container_width=True, type="primary", key="setup_start"):
            if not name.strip():
                st.error("⚠️ Please enter your name to continue.")
                return

            pool = select_questions(
                st.session_state.all_questions,
                st.session_state.difficulty,
            )
            if not pool:
                st.error("No questions available for this difficulty.")
                return

            st.session_state.player_name = name.strip()
            reset_quiz_progress()
            st.session_state.active_questions = pool
            start_question_timer()
            go_to("quiz")
            st.rerun()
