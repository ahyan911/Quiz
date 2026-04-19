"""
Storage module — persists quiz history to a local JSON file.

Streamlit reruns the whole script on every interaction, so we deliberately use
simple file-based JSON rather than in-memory storage. History survives restarts.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_HISTORY_PATH = Path.home() / ".pyquiz_history.json"


def load_history(path: Path = DEFAULT_HISTORY_PATH) -> list[dict[str, Any]]:
    """Load history list from disk. Returns [] if missing or unreadable."""
    try:
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_history(history: list[dict[str, Any]], path: Path = DEFAULT_HISTORY_PATH) -> bool:
    """Persist history list to disk. Returns True on success."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        return True
    except OSError:
        return False


def clear_history(path: Path = DEFAULT_HISTORY_PATH) -> bool:
    """Delete the history file. Returns True on success or if already missing."""
    try:
        if path.exists():
            path.unlink()
        return True
    except OSError:
        return False
