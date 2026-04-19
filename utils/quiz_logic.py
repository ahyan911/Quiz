"""
Quiz logic module — pure functions for scoring, ranking, and question selection.
No Streamlit imports here. Keeps business logic independent of the UI layer.
"""
from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any

QUESTION_TIME_SECONDS = 30
WRONG_PENALTY = 0.25
QUESTIONS_PER_DIFFICULTY = 5
MIXED_QUESTION_COUNT = 10


def load_questions(path: str | Path) -> list[dict[str, Any]]:
    """Load questions from a JSON file. Raises FileNotFoundError/JSONDecodeError on failure."""
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("questions.json must contain a top-level JSON array")
    return data


def select_questions(
    all_questions: list[dict[str, Any]],
    difficulty: str,
    rng: random.Random | None = None,
) -> list[dict[str, Any]]:
    """Pick the pool of questions for the session based on difficulty."""
    rng = rng or random.Random()

    if difficulty == "mixed":
        pool = list(all_questions)
        rng.shuffle(pool)
        return pool[:MIXED_QUESTION_COUNT]

    filtered = [q for q in all_questions if q.get("difficulty") == difficulty]
    rng.shuffle(filtered)
    return filtered[:QUESTIONS_PER_DIFFICULTY]


def compute_rank(percentage: float, player_name: str) -> dict[str, str]:
    """Return rank/title/emoji/feedback for a given percentage score."""
    if percentage >= 90:
        return {
            "rank": "Expert",
            "emoji": "🏆",
            "title": "Outstanding!",
            "subtitle": "You've mastered Python at this level.",
            "feedback": f"Phenomenal work, {player_name}. Keep pushing deeper.",
        }
    if percentage >= 70:
        return {
            "rank": "Advanced",
            "emoji": "🌟",
            "title": "Great Work!",
            "subtitle": "Strong Python knowledge — polish the weak spots.",
            "feedback": f"Solid performance, {player_name}. Review missed topics.",
        }
    if percentage >= 45:
        return {
            "rank": "Intermediate",
            "emoji": "📚",
            "title": "Good Effort!",
            "subtitle": "You're on the right track — keep practicing.",
            "feedback": f"Nice try, {player_name}. Focus on loops, functions, and data structures.",
        }
    return {
        "rank": "Beginner",
        "emoji": "🌱",
        "title": "Keep Going!",
        "subtitle": "Every expert was once a beginner.",
        "feedback": f"Don't give up, {player_name}. Review the basics and try again.",
    }


def format_score(score: float) -> str:
    """Drop trailing .00 for cleaner display."""
    s = f"{score:.2f}"
    return s[:-3] if s.endswith(".00") else s


def apply_answer(
    score: float,
    penalty: float,
    is_correct: bool,
    negative_marking: bool,
) -> tuple[float, float]:
    """
    Apply the scoring rules for a single answer. Returns (new_score, new_penalty).
    - Correct: +1
    - Wrong with negative marking: -0.25 (and accumulate penalty)
    - Wrong without negative marking: no change
    """
    if is_correct:
        return score + 1, penalty
    if negative_marking:
        return score - WRONG_PENALTY, penalty + WRONG_PENALTY
    return score, penalty
