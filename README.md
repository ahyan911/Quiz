# PyQuiz 🐍

A Python quiz application built with **Streamlit**, ported from a vanilla JS/HTML/CSS version. Dark neon theme, 30-second per-question timer, optional negative marking, persistent score history, and a performance analysis dashboard.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.37+-red.svg)

## Features

- **4 difficulty modes** — Easy, Medium, Hard, Mixed (random 10)
- **30-second timer** per question with live countdown (auto-skips on timeout)
- **Optional negative marking** (-0.25 per wrong answer)
- **Live score tracking** during the quiz
- **Rank system** — Beginner / Intermediate / Advanced / Expert
- **Persistent history** saved to `~/.pyquiz_history.json` (survives restarts)
- **Performance analytics** — accuracy, rank distribution, answer breakdown
- **Explanations** shown after every answer

## Quick Start

```bash
# 1. Clone
git clone https://github.com/<your-username>/pyquiz.git
cd pyquiz

# 2. (recommended) Create a virtual env
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## Project Structure

```
pyquiz/
├── app.py                 # Entry point — CSS injection + screen router
├── state.py               # Session state defaults + navigation helpers
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── questions.json     # Question bank (15 questions across 3 difficulties)
│
├── screens/               # One file per UI screen
│   ├── __init__.py
│   ├── menu.py            # Home / main menu
│   ├── setup.py           # Player name + difficulty picker
│   ├── quiz.py            # Active quiz with timer
│   ├── results.py         # Final score + rank
│   ├── history.py         # List of past attempts
│   └── analysis.py        # Aggregated performance stats
│
├── utils/
│   ├── __init__.py
│   ├── quiz_logic.py      # Pure functions: scoring, ranking, question selection
│   └── storage.py         # JSON file persistence for history
│
└── assets/
    └── style.css          # Dark neon theme (custom CSS)
```

### Why split into multiple files?

- `app.py` stays small — just routing and CSS.
- `state.py` centralizes all session defaults so every screen can safely read any key.
- `utils/quiz_logic.py` has **zero Streamlit imports** — pure functions, easy to unit test.
- `utils/storage.py` is swappable — replace with SQLite, Redis, or S3 without touching UI code.
- Each screen is ~50–150 lines in its own file instead of one massive 800-line script.

## Adding Your Own Questions

Append to `data/questions.json`:

```json
{
  "id": 16,
  "difficulty": "medium",
  "category": "Your Category",
  "question": "Your question text here?",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "answer": 2,
  "explanation": "Why the correct answer is correct."
}
```

- `difficulty` must be `"easy"`, `"medium"`, or `"hard"`.
- `answer` is a **0-indexed** integer pointing at the correct option.
- Multi-line questions (e.g. code snippets) work — use `\n` in the string.

## Configuration

Key constants live in `utils/quiz_logic.py`:

```python
QUESTION_TIME_SECONDS = 30       # Seconds per question
WRONG_PENALTY = 0.25             # Deducted per wrong answer when negative marking is on
QUESTIONS_PER_DIFFICULTY = 5     # For easy/medium/hard modes
MIXED_QUESTION_COUNT = 10        # For mixed mode
```

History location is defined in `utils/storage.py` (default: `~/.pyquiz_history.json`).

## Deploying to Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Pick your repo, branch, and set the main file to `app.py`.
4. Deploy. Done.

> **Note:** On Streamlit Cloud, `~/.pyquiz_history.json` lives on ephemeral container storage and may reset on restart. For durable multi-user history, swap `utils/storage.py` for a real database.

## License

MIT
