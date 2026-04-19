"""Performance analysis screen — aggregated stats across all attempts."""
from __future__ import annotations

import streamlit as st

from state import go_to


def render() -> None:
    st.markdown("#### Performance Analysis")

    history = st.session_state.history
    if not history:
        st.markdown(
            "<div class='empty-state'>"
            "<div class='empty-icon'>📈</div>"
            "<p>No data yet. Complete at least one quiz to see analysis!</p>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown("---")
        if st.button("← Back to Menu", use_container_width=True, key="ana_back_empty"):
            go_to("menu")
            st.rerun()
        return

    total_correct = sum(r["correct"] for r in history)
    total_wrong = sum(r["wrong"] for r in history)
    total_skipped = sum(r["skipped"] for r in history)
    total_score = sum(r["score"] for r in history)

    rank_counts = {"Beginner": 0, "Intermediate": 0, "Advanced": 0, "Expert": 0}
    for r in history:
        if r["rank"] in rank_counts:
            rank_counts[r["rank"]] += 1

    answered = total_correct + total_wrong + total_skipped
    accuracy = round((total_correct / answered) * 100) if answered else 0
    avg_score = total_score / len(history)

    # Best rank achieved
    best_rank = "Beginner"
    for rk in ("Expert", "Advanced", "Intermediate"):
        if rank_counts[rk]:
            best_rank = rk
            break

    # Top-line stats
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"<div class='stat-box'><div class='stat-val'>{len(history)}</div>"
            f"<div class='stat-lbl'>ATTEMPTS</div></div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"<div class='stat-box'><div class='stat-val'>{avg_score:.2f}</div>"
            f"<div class='stat-lbl'>AVG SCORE</div></div>",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"<div class='stat-box stat-correct'><div class='stat-val'>{accuracy}%</div>"
            f"<div class='stat-lbl'>ACCURACY</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("**Answer Breakdown**")

    def pct(n: int) -> int:
        return round((n / answered) * 100) if answered else 0

    def bar(label: str, count: int, color_cls: str) -> None:
        p = pct(count)
        st.markdown(
            f"<div class='analysis-row'>"
            f"<div class='analysis-row-label'><span>{label}</span><span>{count} ({p}%)</span></div>"
            f"<div class='analysis-bar'><div class='analysis-bar-fill {color_cls}' style='width:{p}%'></div></div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    bar("✅ Correct", total_correct, "fill-correct")
    bar("❌ Wrong", total_wrong, "fill-wrong")
    bar("⏭️ Skipped", total_skipped, "fill-skipped")

    st.markdown("---")
    st.markdown("**Rank Distribution**")

    for rk, count in rank_counts.items():
        times_word = "time" if count == 1 else "times"
        st.markdown(
            f"<div class='rank-row'>"
            f"<span class='rank-pill rank-{rk.lower()}'>{rk}</span>"
            f"<span class='rank-count'>{count} {times_word}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("**Best Rank Achieved**")
    st.markdown(
        f"<div style='text-align:center;margin:8px 0;'>"
        f"<span class='rank-pill rank-{best_rank.lower()}' style='font-size:16px;padding:10px 20px;'>{best_rank}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    if st.button("← Back to Menu", use_container_width=True, key="ana_back"):
        go_to("menu")
        st.rerun()
