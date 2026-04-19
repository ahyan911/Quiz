"""
Session state initialization for PyQuiz.

Streamlit's session_state is the single source of truth across reruns.
All defaults live here so every screen can rely on keys existing.
"""
from __future__ import annotations

import time

import streamlit as st

from utils.quiz_logic import load_questions
from utils.storage import load_history

QUESTIONS_PATH = "data/questions.json"


def init_state() -> None:
    """Populate st.session_state with defaults on first run."""
    defaults: dict = {
        "screen": "menu",
        "all_questions": None,
        "active_questions": [],
        "current_index": 0,
        "score": 0.0,
        "correct": 0,
        "wrong": 0,
        "skipped": 0,
        "penalty": 0.0,
        "player_name": "",
        "difficulty": "easy",
        "negative_marking": False,
        "question_start_time": None,
        "answered": False,
        "selected_option": None,
        "history": None,
        "last_result": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Load questions once per session
    if st.session_state.all_questions is None:
        try:
            st.session_state.all_questions = load_questions(QUESTIONS_PATH)
        except Exception as e:
            st.session_state.all_questions = []
            st.session_state.load_error = str(e)

    # Load history once per session
    if st.session_state.history is None:
        st.session_state.history = load_history()


def go_to(screen_name: str) -> None:
    """Navigate to a different screen."""
    st.session_state.screen = screen_name


def reset_quiz_progress() -> None:
    """Reset active quiz state (does not touch history or settings)."""
    st.session_state.active_questions = []
    st.session_state.current_index = 0
    st.session_state.score = 0.0
    st.session_state.correct = 0
    st.session_state.wrong = 0
    st.session_state.skipped = 0
    st.session_state.penalty = 0.0
    st.session_state.answered = False
    st.session_state.selected_option = None
    st.session_state.question_start_time = None


def start_question_timer() -> None:
    """Mark the current wall-clock time as the question start."""
    st.session_state.question_start_time = time.time()
    st.session_state.answered = False
    st.session_state.selected_option = None
