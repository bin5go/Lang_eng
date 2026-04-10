"""
quiz_builder.py — Distribute words across sections and assemble the quiz object.

Quiz object shape returned by build():
{
    "number": int,
    "book": str,
    "page_range": str,
    "words": [list of all 15 word dicts],
    "sections": {
        "A": [list of 5 QuestionItems],
        "B": [list of 5 QuestionItems],
        "C": [list of 3 QuestionItems],
        "D": [list of 1-2 QuestionItems],
    }
}

QuestionItem shape:
{
    "word": str,
    "section": "A" | "B" | "C" | "D",
    "stem": str,
    "options": list[str] | None,   # Section A only
    "answer": str,
    "hint": str | None,            # Section B only
}
"""

from __future__ import annotations


def distribute_sections(quiz_words: list[dict]) -> dict[str, list[dict]]:
    """
    Split 15 words into sections A–D.
    Academic words are swapped toward Section D slots (positions 13–14)
    so that real-world prompts feature academic vocabulary where possible.
    """
    words = list(quiz_words)
    for target in [13, 14]:
        if target >= len(words):
            break
        if not words[target]["academic"]:
            for src in range(min(13, len(words))):
                if words[src]["academic"]:
                    words[target], words[src] = words[src], words[target]
                    break
    return {
        "A": words[0:5],
        "B": words[5:10],
        "C": words[10:13],
        "D": words[13 : min(15, len(words))],
    }


def build(
    quiz_number: int,
    quiz_words: list[dict],
    book: str,
    generator,
) -> dict:
    """
    Orchestrate: distribute words, call generator, return quiz object.
    generator must expose generate(sections) -> dict[str, list[QuestionItem]].
    """
    sections_words = distribute_sections(quiz_words)
    sections_questions = generator.generate(sections_words)

    page_range = f"pp. {quiz_words[0]['page']}–{quiz_words[-1]['page']}"

    return {
        "number": quiz_number,
        "book": book,
        "page_range": page_range,
        "words": quiz_words,
        "sections": sections_questions,
    }
