# Shared fixtures for the quiz generator test suite.
# Uses a small 17-word list so tests are independent of words_gw2.json.

import pytest

FIXTURE_WORDS = [
    {"word": "accomplish",   "page":  1, "level": "B1", "academic": False},
    {"word": "affect",       "page":  2, "level": "B2", "academic": True},
    {"word": "benefit",      "page":  3, "level": "B1", "academic": True},
    {"word": "calculate",    "page":  4, "level": "B1", "academic": False},
    {"word": "damage",       "page":  5, "level": "B1", "academic": False},
    {"word": "effective",    "page":  6, "level": "B2", "academic": True},
    {"word": "focus",        "page":  7, "level": "B2", "academic": True},
    {"word": "generally",    "page":  8, "level": "B1", "academic": True},
    {"word": "improve",      "page":  9, "level": "A2", "academic": False},
    {"word": "likely",       "page": 10, "level": "B1", "academic": False},
    {"word": "maintain",     "page": 11, "level": "B2", "academic": True},
    {"word": "obtain",       "page": 12, "level": "B2", "academic": True},
    {"word": "prevent",      "page": 13, "level": "B2", "academic": False},
    {"word": "reduce",       "page": 14, "level": "B1", "academic": True},
    {"word": "research",     "page": 15, "level": "B1", "academic": True},
    {"word": "select",       "page": 16, "level": "B2", "academic": True},
    {"word": "valid",        "page": 17, "level": "B2", "academic": True},
]

# First 15 words sorted by page (they are already in order above)
FIXTURE_QUIZ_WORDS = FIXTURE_WORDS[:15]


@pytest.fixture
def fixture_words():
    return list(FIXTURE_WORDS)


@pytest.fixture
def fixture_quiz_words():
    return list(FIXTURE_QUIZ_WORDS)
