"""
generator_template.py — Generate quiz questions from static template dicts.

Interface: generate(sections_words) -> dict[str, list[QuestionItem]]

All template data (FILL_IN_SENTENCES, FILL_IN_HINTS, C1_DEFINITIONS,
SYNONYM_MCQ, ERROR_ANALYSIS, REAL_WORLD_PROMPTS) lives in quiz_generator.py
and is imported here to avoid duplication during the v1→v2 transition.
"""

from quiz_generator import (
    FILL_IN_SENTENCES,
    FILL_IN_HINTS,
    C1_DEFINITIONS,
    SYNONYM_MCQ,
    ERROR_ANALYSIS,
    REAL_WORLD_PROMPTS,
)


# ── Section A — Multiple choice ───────────────────────────────────────────────

def _make_a(entry: dict) -> dict:
    word = entry["word"]
    defn = C1_DEFINITIONS.get(word) or SYNONYM_MCQ.get(word)
    if defn:
        return {
            "word": word,
            "section": "A",
            "stem": f"What is the best meaning of the word *{word}*?",
            "options": defn["options"],
            "answer": defn["answer"],
            "hint": None,
        }
    return {
        "word": word,
        "section": "A",
        "stem": f"What is the best meaning of the word *{word}*?",
        "options": [
            "A. [option not yet available]",
            "B. [option not yet available]",
            "C. [option not yet available]",
            "D. [option not yet available]",
        ],
        "answer": f"[TEMPLATE MISSING — add '{word}' to SYNONYM_MCQ]",
        "hint": None,
    }


# ── Section B — Fill in the blank ────────────────────────────────────────────

def _make_b(entry: dict) -> dict:
    word = entry["word"]
    sentence = FILL_IN_SENTENCES.get(word)
    hint = FILL_IN_HINTS.get(word, "see context")
    if sentence:
        blank = sentence.replace(word, "_______________")
        return {
            "word": word,
            "section": "B",
            "stem": blank,
            "options": None,
            "answer": sentence,
            "hint": hint,
        }
    return {
        "word": word,
        "section": "B",
        "stem": f"[TEMPLATE MISSING — add '{word}' to FILL_IN_SENTENCES]",
        "options": None,
        "answer": word,
        "hint": hint,
    }


# ── Section C — Error analysis ────────────────────────────────────────────────

def _make_c(entry: dict) -> dict:
    word = entry["word"]
    data = ERROR_ANALYSIS.get(word)
    if data:
        return {
            "word": word,
            "section": "C",
            "stem": data["sentence"],
            "options": None,
            "answer": data["answer"],
            "hint": None,
        }
    return {
        "word": word,
        "section": "C",
        "stem": f"[TEMPLATE MISSING — add '{word}' to ERROR_ANALYSIS]",
        "options": None,
        "answer": word,
        "hint": None,
    }


# ── Section D — Real-world application ───────────────────────────────────────

def _make_d(entry: dict) -> dict:
    word = entry["word"]
    prompt = REAL_WORLD_PROMPTS.get(word)
    if prompt:
        return {
            "word": word,
            "section": "D",
            "stem": prompt,
            "options": None,
            "answer": "Answers will vary.",
            "hint": None,
        }
    return {
        "word": word,
        "section": "D",
        "stem": f"[TEMPLATE MISSING — add '{word}' to REAL_WORLD_PROMPTS]",
        "options": None,
        "answer": "Answers will vary.",
        "hint": None,
    }


# ── Public interface ──────────────────────────────────────────────────────────

_MAKERS = {"A": _make_a, "B": _make_b, "C": _make_c, "D": _make_d}


def generate(sections_words: dict) -> dict[str, list[dict]]:
    """
    Accept sections_words dict (keys A–D, values list of word entry dicts).
    Return sections_questions dict with same keys, values list of QuestionItems.
    """
    return {
        section: [_MAKERS[section](entry) for entry in entries]
        for section, entries in sections_words.items()
    }
