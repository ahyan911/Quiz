"""Active quiz screen — handles question display, timer, answer submission."""
from __future__ import annotations

import time
from datetime import datetime

import streamlit as st

from state import go_to, start_question_timer
from utils.quiz_logic import (
    QUESTION_TIME_SECONDS,
    apply_answer,
    compute_rank,
    format_score,
)
from utils.storage import save_history

OPTION_LABELS = ["A", "B", "C", "D"]


def _finalize_quiz() -> None:
    """Compute final result, push to history, move to results screen."""
    total = len(st.session_state.active_questions)
    percentage = max(0.0, (st.session_state.score / total) * 100) if total else 0.0
    rank_info = compute_rank(percentage, st.session_state.player_name)

    result = {
        "name": st.session_state.player_name,
        "score": round(st.session_state.score, 2),
        "total": total,
        "percentage": round(percentage, 1),
        "correct": st.session_state.correct,
        "wrong": st.session_state.wrong,
        "skipped": st.session_state.skipped,
        "difficulty": st.session_state.difficulty,
        "rank": rank_info["rank"],
        "negative": st.session_state.negative_marking,
        "penalty": round(st.session_state.penalty, 2),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    st.session_state.history.append(result)
    st.session_state.last_result = {**result, **rank_info}
    save_history(st.session_state.history)
    go_to("results")


def _advance() -> None:
    """Move to the next question or finalize if done."""
    st.session_state.current_index += 1
    if st.session_state.current_index >= len(st.session_state.active_questions):
        _finalize_quiz()
    else:
        start_question_timer()


def _submit_answer(selected_idx: int) -> None:
    """Register the user's selected answer."""
    if st.session_state.answered:
        return
    q = st.session_state.active_questions[st.session_state.current_index]
    is_correct = selected_idx == q["answer"]

    new_score, new_penalty = apply_answer(
        st.session_state.score,
        st.session_state.penalty,
        is_correct,
        st.session_state.negative_marking,
    )
    st.session_state.score = new_score
    st.session_state.penalty = new_penalty

    if is_correct:
        st.session_state.correct += 1
    else:
        st.session_state.wrong += 1

    st.session_state.selected_option = selected_idx
    st.session_state.answered = True


def _handle_timeout() -> None:
    """Handle a question where time ran out."""
    if st.session_state.answered:
        return
    st.session_state.skipped += 1
    st.session_state.answered = True
    st.session_state.selected_option = None


def _compute_time_left() -> int:
    """Seconds remaining for the current question (non-negative)."""
    start = st.session_state.question_start_time
    if start is None:
        return QUESTION_TIME_SECONDS
    elapsed = time.time() - start
    return max(0, int(QUESTION_TIME_SECONDS - elapsed))


@st.fragment(run_every=1)
def _timer_fragment() -> None:
    """Auto-refreshing timer. Only the fragment reruns each second, not the full page."""
    if st.session_state.answered:
        # Freeze the displayed number at whatever it was when answered — show final state.
        remaining = _compute_time_left()
        st.markdown(
            f"<div class='timer-pill'>{remaining}s</div>",
            unsafe_allow_html=True,
        )
        return

    remaining = _compute_time_left()
    urgent_cls = "timer-pill urgent" if remaining <= 5 else "timer-pill"
    st.markdown(f"<div class='{urgent_cls}'>{remaining}s</div>", unsafe_allow_html=True)

    if remaining <= 0:
        _handle_timeout()
        st.rerun()


def render() -> None:
    questions = st.session_state.active_questions
    idx = st.session_state.current_index
    total = len(questions)

    if not questions:
        st.warning("No active quiz. Head back to the menu.")
        if st.button("🏠 Back to Menu"):
            go_to("menu")
            st.rerun()
        return

    q = questions[idx]

    # Top bar
    top_l, top_c, top_r = st.columns([2, 1, 2])
    with top_l:
        st.markdown(
            f"<div class='quiz-progress'>Question <b>{idx + 1}</b> of <b>{total}</b></div>",
            unsafe_allow_html=True,
        )
    with top_c:
        _timer_fragment()
    with top_r:
        st.markdown(
            f"<div class='score-pill'>Score: <b>{format_score(st.session_state.score)}</b></div>",
            unsafe_allow_html=True,
        )

    # Progress bar
    st.progress(idx / total if total else 0)

    # Difficulty badge + category
    st.markdown(
        f"<span class='diff-badge badge-{q['difficulty']}'>"
        f"{q['difficulty'].upper()} · {q['category']}</span>",
        unsafe_allow_html=True,
    )

    # Question text (preserve line breaks for code snippets)
    st.markdown(f"<div class='question-text'>{q['question']}</div>", unsafe_allow_html=True)

    # Options
    if not st.session_state.answered:
        for i, opt in enumerate(q["options"]):
            if st.button(
                f"**{OPTION_LABELS[i]}**   {opt}",
                key=f"opt_{idx}_{i}",
                use_container_width=True,
            ):
                _submit_answer(i)
                st.rerun()
    else:
        # Answered state — show options with coloring via markdown
        correct_idx = q["answer"]
        selected = st.session_state.selected_option
        for i, opt in enumerate(q["options"]):
            if i == correct_idx:
                cls = "opt-display correct"
                marker = "✓"
            elif i == selected:
                cls = "opt-display wrong"
                marker = "✗"
            else:
                cls = "opt-display"
                marker = " "
            st.markdown(
                f"<div class='{cls}'>"
                f"<span class='opt-letter'>{OPTION_LABELS[i]}</span>"
                f"<span class='opt-text'>{opt}</span>"
                f"<span class='opt-marker'>{marker}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

        # Feedback
        if selected is None:
            st.warning(
                f"⏰ **Time's up!** Correct answer: "
                f"**{OPTION_LABELS[correct_idx]}. {q['options'][correct_idx]}**\n\n"
                f"_{q['explanation']}_"
            )
        elif selected == correct_idx:
            st.success(f"✅ **Correct!** +1 mark\n\n_{q['explanation']}_")
        else:
            penalty_txt = " (-0.25)" if st.session_state.negative_marking else ""
            st.error(
                f"❌ **Wrong{penalty_txt}.** Correct answer: "
                f"**{OPTION_LABELS[correct_idx]}. {q['options'][correct_idx]}**\n\n"
                f"_{q['explanation']}_"
            )

        # Next button
        next_label = "Next Question →" if idx + 1 < total else "See Results 🏁"
        if st.button(next_label, use_container_width=True, type="primary", key=f"next_{idx}"):
            _advance()
            st.rerun()
