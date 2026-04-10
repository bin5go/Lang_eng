"""Tests for quiz_builder.py — section distribution and quiz object shape."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
import quiz_builder
import generator_template


# ── distribute_sections() ────────────────────────────────────────────────────

def test_distribute_sections_sizes(fixture_quiz_words):
    sections = quiz_builder.distribute_sections(fixture_quiz_words)
    assert len(sections["A"]) == 5
    assert len(sections["B"]) == 5
    assert len(sections["C"]) == 3
    assert len(sections["D"]) == 2


def test_distribute_sections_all_15_words_present(fixture_quiz_words):
    sections = quiz_builder.distribute_sections(fixture_quiz_words)
    all_words = (
        sections["A"] + sections["B"] + sections["C"] + sections["D"]
    )
    assert len(all_words) == 15
    input_words = {w["word"] for w in fixture_quiz_words}
    output_words = {w["word"] for w in all_words}
    assert input_words == output_words


def test_distribute_sections_academic_words_in_d(fixture_quiz_words):
    sections = quiz_builder.distribute_sections(fixture_quiz_words)
    # At least one Section D word should be academic (fixture has many academic words)
    assert any(w["academic"] for w in sections["D"])


def test_distribute_sections_14_words():
    """Last quiz of gw2 has 14 words — Section D gets only 1."""
    words_14 = [
        {"word": str(i), "page": i, "level": "B1", "academic": (i % 3 == 0)}
        for i in range(14)
    ]
    sections = quiz_builder.distribute_sections(words_14)
    assert len(sections["D"]) == 1
    total = sum(len(v) for v in sections.values())
    assert total == 14


# ── build() ──────────────────────────────────────────────────────────────────

def test_build_returns_quiz_object(fixture_quiz_words):
    quiz = quiz_builder.build(
        quiz_number=1,
        quiz_words=fixture_quiz_words,
        book="gw2",
        generator=generator_template,
    )
    assert quiz["number"] == 1
    assert quiz["book"] == "gw2"
    assert "page_range" in quiz
    assert "sections" in quiz
    assert set(quiz["sections"].keys()) == {"A", "B", "C", "D"}


def test_build_section_a_has_options(fixture_quiz_words):
    quiz = quiz_builder.build(1, fixture_quiz_words, "gw2", generator_template)
    for item in quiz["sections"]["A"]:
        assert item.get("options") is not None
        assert len(item["options"]) == 4


def test_build_section_b_has_hint(fixture_quiz_words):
    quiz = quiz_builder.build(1, fixture_quiz_words, "gw2", generator_template)
    for item in quiz["sections"]["B"]:
        assert item.get("hint") is not None
        # Hint must NOT be a CEFR level label
        assert item["hint"] not in {"A1", "A2", "B1", "B2", "C1", "C2", "off-list"}


def test_build_section_c_has_no_options(fixture_quiz_words):
    quiz = quiz_builder.build(1, fixture_quiz_words, "gw2", generator_template)
    for item in quiz["sections"]["C"]:
        assert item.get("options") is None


def test_build_section_d_prompt_names_word(fixture_quiz_words):
    quiz = quiz_builder.build(1, fixture_quiz_words, "gw2", generator_template)
    for item in quiz["sections"]["D"]:
        word = item["word"]
        # The prompt should reference the target word (bold in template, either **word** or plain)
        assert word.lower() in item["stem"].lower()


def test_build_answer_key_all_sections(fixture_quiz_words):
    quiz = quiz_builder.build(1, fixture_quiz_words, "gw2", generator_template)
    for section in ["A", "B", "C", "D"]:
        for item in quiz["sections"][section]:
            assert "answer" in item
            assert item["answer"]  # non-empty
