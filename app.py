"""
PyQuiz — Streamlit entry point.

Run with:
    streamlit run app.py
"""
from __future__ import annotations

from pathlib import Path

import streamlit as st

from state import go_to, init_state
from screens import analysis, history, menu, quiz, results, setup
from utils.storage import clear_history

APP_DIR = Path(__file__).parent
CSS_PATH = APP_DIR / "assets" / "style.css"


def inject_css() -> None:
    """Inject custom stylesheet into the app."""
    if CSS_PATH.exists():
        st.markdown(f"<style>{CSS_PATH.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def render_header() -> None:
    st.markdown(
        """
        <div class="app-header">
          <div class="app-logo">▸ Interactive Learning</div>
          <h1 class="app-title">Py<span>Quiz</span></h1>
          <div class="app-subtitle">Test your Python knowledge · Track your progress</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_exit_confirm() -> None:
    st.markdown("#### ⚠️ Clear all data?")
    st.warning("This will permanently delete ALL saved quiz history. This cannot be undone.")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Cancel", use_container_width=True, key="exit_cancel"):
            go_to("menu")
            st.rerun()
    with c2:
        if st.button("🗑️ Delete Everything", use_container_width=True, type="primary", key="exit_confirm"):
            clear_history()
            st.session_state.history = []
            st.session_state.last_result = None
            go_to("menu")
            st.success("✅ All data cleared. Starting fresh.")
            st.rerun()


SCREEN_ROUTER = {
    "menu": menu.render,
    "setup": setup.render,
    "quiz": quiz.render,
    "results": results.render,
    "history": history.render,
    "analysis": analysis.render,
    "exit_confirm": render_exit_confirm,
}


def main() -> None:
    st.set_page_config(
        page_title="PyQuiz — Python Quiz System",
        page_icon="🐍",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    inject_css()
    init_state()

    # Show a hard error if questions failed to load
    if hasattr(st.session_state, "load_error") and not st.session_state.all_questions:
        st.error(f"❌ Could not load questions.json: {st.session_state.load_error}")
        st.info("Make sure `data/questions.json` exists relative to `app.py`.")
        return

    render_header()

    render_fn = SCREEN_ROUTER.get(st.session_state.screen, menu.render)
    render_fn()


if __name__ == "__main__":
    main()
