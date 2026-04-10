"""
word_store.py — Load, validate, sort, and slice vocabulary word lists.
"""

import json
import sys
from pathlib import Path

REQUIRED_FIELDS = {"word", "page", "level", "academic"}
VALID_LEVELS = {"A1", "A2", "B1", "B2", "C1", "C2", "off-list"}

BUILT_IN = {
    "gw2": Path(__file__).parent / "words_gw2.json",
    "gw3": Path(__file__).parent / "words_gw3.json",
}


def load(book: str = "gw2", wordlist_path: str | None = None) -> list[dict]:
    """
    Load and validate a word list.
    wordlist_path takes precedence over book if both are provided.
    Returns a list of word dicts sorted ascending by page number.
    """
    if wordlist_path:
        path = Path(wordlist_path)
    else:
        path = BUILT_IN.get(book)
        if path is None:
            sys.exit(f"Error: unknown book '{book}'. Choose gw2 or gw3.")

    if not path.exists():
        sys.exit(f"Error: word list file not found: {path}")

    with open(path, encoding="utf-8") as f:
        try:
            words = json.load(f)
        except json.JSONDecodeError as e:
            sys.exit(f"Error: invalid JSON in {path}: {e}")

    if not isinstance(words, list) or len(words) == 0:
        sys.exit(f"Error: {path} must contain a non-empty JSON array.")

    errors = []
    for i, entry in enumerate(words):
        missing = REQUIRED_FIELDS - entry.keys()
        if missing:
            errors.append(f"  Entry {i}: missing fields {missing}")
        elif entry["level"] not in VALID_LEVELS:
            errors.append(f"  Entry {i} '{entry['word']}': invalid level '{entry['level']}'")
        elif not isinstance(entry["academic"], bool):
            errors.append(f"  Entry {i} '{entry['word']}': 'academic' must be true or false")
    if errors:
        sys.exit("Error: word list schema validation failed:\n" + "\n".join(errors))

    return sorted(words, key=lambda w: w["page"])


def total_quizzes(words: list[dict]) -> int:
    return (len(words) + 14) // 15


def get_quiz_words(words: list[dict], quiz_number: int) -> list[dict]:
    start = (quiz_number - 1) * 15
    return words[start : start + 15]
