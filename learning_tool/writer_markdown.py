"""
writer_markdown.py — Render a quiz object to a Markdown file.
"""

from pathlib import Path


def _question_number(sections: dict, section: str, index: int) -> int:
    """Return the continuous question number across all sections."""
    order = ["A", "B", "C", "D"]
    offset = 1
    for s in order:
        if s == section:
            return offset + index
        offset += len(sections[s])
    return offset + index


def write(quiz: dict, output_dir: Path) -> Path:
    n = quiz["number"]
    book_label = quiz["book"].upper()
    page_range = quiz["page_range"]
    words = quiz["words"]
    sections = quiz["sections"]

    word_preview = ", ".join(w["word"] for w in words)

    lines = [
        f"# Great Writing {book_label[-1]} — Vocabulary Quiz {n:02d}",
        f"**Words:** {page_range} (ascending page order) | **Total words:** {len(words)} | **Time:** 20 minutes",
        f"*Words covered: {word_preview}*",
        "",
        "**Name:** ___________________________ &nbsp;&nbsp; **Class:** _______ &nbsp;&nbsp; **Date:** ___________",
        "",
        "---",
        "",
        "## Instructions",
        "- **Section A:** Circle the letter of the best answer.",
        "- **Section B:** Write the missing word on the line. Use the synonym clue to help you.",
        "- **Section C:** Each sentence has one incorrect word (shown in **bold**). Write the correct word on the line.",
        "- **Section D:** Write 1–2 sentences in response to the prompt. Use the vocabulary word and underline it.",
        "",
    ]

    # ── Section A ────────────────────────────────────────────────────────────
    lines += ["---", "", "## Section A — Multiple Choice", ""]
    for i, item in enumerate(sections["A"]):
        q = _question_number(sections, "A", i)
        lines.append(f"**{q}.** {item['stem']}")
        if item.get("options"):
            for opt in item["options"]:
                lines.append(f"   {opt}")
        lines.append("")

    # ── Section B ────────────────────────────────────────────────────────────
    lines += ["---", "", "## Section B — Fill in the Blank", ""]
    for i, item in enumerate(sections["B"]):
        q = _question_number(sections, "B", i)
        hint = item.get("hint", "")
        lines.append(f"**{q}.** Fill in the blank with the correct word.")
        lines.append(f"   *(synonym: {hint})* — {item['stem']}")
        lines.append("")

    # ── Section C ────────────────────────────────────────────────────────────
    lines += [
        "---",
        "",
        "## Section C — Error Analysis",
        "*Each sentence contains one incorrect word (shown in bold). Identify the error and write the correct word.*",
        "",
    ]
    for i, item in enumerate(sections["C"]):
        q = _question_number(sections, "C", i)
        lines.append(f"**{q}.** {item['stem']}")
        lines.append(f"   Correct word: _______________")
        lines.append("")

    # ── Section D ────────────────────────────────────────────────────────────
    lines += [
        "---",
        "",
        "## Section D — Real-World Application",
        "*Write 1–2 sentences in response to each prompt. Use the vocabulary word and underline it.*",
        "",
    ]
    for i, item in enumerate(sections["D"]):
        q = _question_number(sections, "D", i)
        lines.append(f"**{q}.** {item['stem']}")
        lines.append(f"   _______________________________________________")
        lines.append(f"   _______________________________________________")
        lines.append("")

    # ── Answer Key ───────────────────────────────────────────────────────────
    lines += ["---", "", "## Answer Key *(Teacher Copy)*", ""]

    lines += ["### Section A", ""]
    for i, item in enumerate(sections["A"]):
        q = _question_number(sections, "A", i)
        lines.append(f"{q}. **{item['word']}** — {item['answer']}")

    lines += ["", "### Section B", ""]
    for i, item in enumerate(sections["B"]):
        q = _question_number(sections, "B", i)
        lines.append(f"{q}. **{item['word']}** — {item['answer']}")

    lines += ["", "### Section C", ""]
    for i, item in enumerate(sections["C"]):
        q = _question_number(sections, "C", i)
        lines.append(f"{q}. **{item['answer']}**")

    lines += ["", "### Section D", ""]
    for i, item in enumerate(sections["D"]):
        q = _question_number(sections, "D", i)
        lines.append(
            f"{q}. Answers will vary. The word **{item['word']}** must appear underlined."
        )

    output_path = output_dir / f"quiz_{n:02d}.md"
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path
