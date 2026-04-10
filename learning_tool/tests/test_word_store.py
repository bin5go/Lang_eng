"""Tests for word_store.py"""

import json
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
import word_store


# ── load() ───────────────────────────────────────────────────────────────────

def test_load_gw2_returns_list():
    words = word_store.load("gw2")
    assert isinstance(words, list)
    assert len(words) > 0


def test_load_gw3_returns_list():
    words = word_store.load("gw3")
    assert isinstance(words, list)
    assert len(words) > 0


def test_load_ascending_page_order():
    words = word_store.load("gw2")
    pages = [w["page"] for w in words]
    assert pages == sorted(pages)


def test_load_all_required_fields():
    words = word_store.load("gw2")
    for entry in words:
        assert "word" in entry
        assert "page" in entry
        assert "level" in entry
        assert "academic" in entry


def test_load_custom_wordlist(tmp_path):
    custom = [
        {"word": "example", "page": 1, "level": "B1", "academic": False},
        {"word": "another", "page": 2, "level": "B2", "academic": True},
    ]
    p = tmp_path / "custom.json"
    p.write_text(json.dumps(custom))
    words = word_store.load(wordlist_path=str(p))
    assert len(words) == 2
    assert words[0]["word"] == "example"


def test_load_custom_takes_precedence_over_book(tmp_path):
    custom = [{"word": "only", "page": 1, "level": "B1", "academic": False}]
    p = tmp_path / "custom.json"
    p.write_text(json.dumps(custom))
    words = word_store.load(book="gw3", wordlist_path=str(p))
    assert len(words) == 1
    assert words[0]["word"] == "only"


def test_load_invalid_json_exits(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("not json{{{")
    with pytest.raises(SystemExit):
        word_store.load(wordlist_path=str(p))


def test_load_missing_field_exits(tmp_path):
    bad = [{"word": "test", "page": 1}]  # missing level and academic
    p = tmp_path / "bad.json"
    p.write_text(json.dumps(bad))
    with pytest.raises(SystemExit):
        word_store.load(wordlist_path=str(p))


def test_load_off_list_words_included():
    words = word_store.load("gw2")
    levels = {w["level"] for w in words}
    assert "off-list" in levels


# ── total_quizzes() ───────────────────────────────────────────────────────────

def test_total_quizzes_gw2():
    words = word_store.load("gw2")
    total = word_store.total_quizzes(words)
    assert total == (len(words) + 14) // 15


def test_total_quizzes_exact_multiple():
    words = [{"word": str(i), "page": i, "level": "B1", "academic": False} for i in range(30)]
    assert word_store.total_quizzes(words) == 2


def test_total_quizzes_remainder():
    words = [{"word": str(i), "page": i, "level": "B1", "academic": False} for i in range(31)]
    assert word_store.total_quizzes(words) == 3


# ── get_quiz_words() ─────────────────────────────────────────────────────────

def test_get_quiz_words_returns_15(fixture_words):
    batch = word_store.get_quiz_words(fixture_words, 1)
    assert len(batch) == 15


def test_get_quiz_words_ascending_order(fixture_words):
    batch = word_store.get_quiz_words(fixture_words, 1)
    pages = [w["page"] for w in batch]
    assert pages == sorted(pages)


def test_get_quiz_words_correct_window(fixture_words):
    batch1 = word_store.get_quiz_words(fixture_words, 1)
    batch2 = word_store.get_quiz_words(fixture_words, 2)
    assert batch1[0]["page"] < batch2[0]["page"]


def test_get_quiz_words_last_quiz_may_be_shorter():
    words = [{"word": str(i), "page": i, "level": "B1", "academic": False} for i in range(17)]
    batch = word_store.get_quiz_words(words, 2)
    assert len(batch) == 2  # 17 - 15 = 2
