"""Tests for the template generator (generator_template.py)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
import generator_template


def _make_entry(word, level="B1", academic=False):
    return {"word": word, "page": 1, "level": level, "academic": academic}


# ── Section A ────────────────────────────────────────────────────────────────

def test_section_a_four_options():
    item = generator_template._make_a(_make_entry("likely"))
    assert len(item["options"]) == 4


def test_section_a_answer_is_string():
    item = generator_template._make_a(_make_entry("likely"))
    assert isinstance(item["answer"], str)
    assert item["answer"]


def test_section_a_c1_word_uses_c1_definitions():
    item = generator_template._make_a(_make_entry("outweigh", level="C1"))
    assert "greater in importance" in item["answer"]


def test_section_a_non_c1_word_uses_synonym_mcq():
    item = generator_template._make_a(_make_entry("population", level="B1"))
    assert "people" in item["answer"]


def test_section_a_hint_is_none():
    item = generator_template._make_a(_make_entry("likely"))
    assert item["hint"] is None


# ── Section B ────────────────────────────────────────────────────────────────

def test_section_b_hint_not_cefr_level():
    for word in ["likely", "reduce", "research", "maintain"]:
        item = generator_template._make_b(_make_entry(word))
        assert item["hint"] not in {"A1", "A2", "B1", "B2", "C1", "C2", "off-list"}, (
            f"'{word}' hint is a CEFR label: {item['hint']}"
        )


def test_section_b_blank_in_stem():
    item = generator_template._make_b(_make_entry("likely"))
    assert "___" in item["stem"]


def test_section_b_answer_is_nonempty_string():
    # answer holds the original sentence from FILL_IN_SENTENCES
    item = generator_template._make_b(_make_entry("likely"))
    assert isinstance(item["answer"], str)
    assert len(item["answer"]) > 0


def test_section_b_options_is_none():
    item = generator_template._make_b(_make_entry("likely"))
    assert item["options"] is None


# ── Section C ────────────────────────────────────────────────────────────────

def test_section_c_answer_is_correct_word():
    item = generator_template._make_c(_make_entry("reduce"))
    assert item["answer"] == "reduce"


def test_section_c_stem_has_bold_wrong_word():
    item = generator_template._make_c(_make_entry("reduce"))
    assert "**" in item["stem"]


def test_section_c_wrong_word_differs_from_answer():
    item = generator_template._make_c(_make_entry("reduce"))
    # Extract the bolded word
    import re
    bolded = re.findall(r"\*\*(.+?)\*\*", item["stem"])
    assert bolded, "No bold word found in Section C stem"
    assert bolded[0] != item["answer"]


# ── Section D ────────────────────────────────────────────────────────────────

def test_section_d_prompt_references_word():
    item = generator_template._make_d(_make_entry("research", academic=True))
    assert "research" in item["stem"].lower()


def test_section_d_answer_is_varies():
    item = generator_template._make_d(_make_entry("research", academic=True))
    assert "vary" in item["answer"].lower()


def test_section_d_options_is_none():
    item = generator_template._make_d(_make_entry("research", academic=True))
    assert item["options"] is None


# ── generate() full interface ─────────────────────────────────────────────────

def test_generate_returns_all_sections(fixture_quiz_words):
    from quiz_builder import distribute_sections
    sections_words = distribute_sections(fixture_quiz_words)
    result = generator_template.generate(sections_words)
    assert set(result.keys()) == {"A", "B", "C", "D"}
    assert len(result["A"]) == 5
    assert len(result["B"]) == 5
    assert len(result["C"]) == 3
    assert len(result["D"]) == 2


def test_generate_each_item_has_required_fields(fixture_quiz_words):
    from quiz_builder import distribute_sections
    sections_words = distribute_sections(fixture_quiz_words)
    result = generator_template.generate(sections_words)
    for section, items in result.items():
        for item in items:
            assert "word" in item
            assert "section" in item
            assert "stem" in item
            assert "answer" in item
