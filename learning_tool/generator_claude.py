"""
generator_claude.py — Generate quiz questions via the Claude API (one batch call).

Interface: generate(sections_words) -> dict[str, list[QuestionItem]]
Falls back to generator_template on API error or JSON parse failure.
"""

import json
import os
import sys

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

import generator_template

MODEL = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = """\
You are a vocabulary quiz writer for Grade-8 English students (CEFR B1–C1) \
using the Great Writing textbook series. You produce structured, pedagogically \
sound questions appropriate to each word's difficulty level.

Rules:
- Section A (Multiple Choice): One 4-option MCQ testing the best definition \
or synonym. Wrong options must be plausible — same word class, related meaning, \
NOT obviously wrong or absurd.
- Section B (Fill in the Blank): One sentence with the target word removed as \
a blank (_______________). Include a hint that is a short synonym or meaning \
clue (2–5 words). NEVER use the CEFR level as the hint. The sentence context \
must make the target word unambiguous.
- Section C (Error Analysis): One sentence where a plausible but wrong word \
replaces the target word. The wrong word must be the same word class and close \
enough in meaning to require genuine vocabulary discrimination. Wrap the wrong \
word in double asterisks (**wrong_word**).
- Section D (Real-World Application): One short prompt (2–3 sentences) set in \
a realistic Grade-8 school or daily-life scenario. Name the target word in \
bold (**word**) and instruct the student to use it in a 1–2 sentence response.
- Academic words should be used in more formal, academic contexts.
- All sentences must be at B1–B2 reading level. Avoid idioms unfamiliar to \
non-native English speakers.

Return ONLY a valid JSON array. No explanation, no markdown fences, no extra text.
"""


def _user_prompt(sections_words: dict) -> str:
    order = ["A", "B", "C", "D"]
    all_words = []
    for s in order:
        for entry in sections_words.get(s, []):
            all_words.append({**entry, "section": s})

    words_json = json.dumps(all_words, ensure_ascii=False, indent=2)

    return f"""\
Generate quiz questions for the following {len(all_words)} vocabulary words. \
Each entry shows the word, its CEFR level, whether it is academic vocabulary, \
and which quiz section it belongs to.

Words:
{words_json}

Return a JSON array with exactly {len(all_words)} objects, one per word, \
in the SAME ORDER as the input. Each object must follow this schema exactly:

{{
  "word": "<the vocabulary word>",
  "section": "A" | "B" | "C" | "D",
  "stem": "<question sentence or prompt text>",
  "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
  "answer": "<correct answer string>",
  "hint": "<synonym or meaning clue, 2-5 words>"
}}

Field rules:
- "options": include for Section A only; omit (null) for B, C, D.
- "hint": include for Section B only; omit (null) for A, C, D.
- Section C "stem": the wrong word must be wrapped in **double asterisks**. \
"answer" must be the correct target word.
- Section D "stem": the full scenario prompt with the target word in **bold**. \
"answer" should be "Answers will vary."
"""


def _parse_response(text: str, sections_words: dict) -> dict[str, list[dict]]:
    items = json.loads(text)
    if not isinstance(items, list):
        raise ValueError("Response is not a JSON array")

    result: dict[str, list[dict]] = {"A": [], "B": [], "C": [], "D": []}
    for item in items:
        section = item.get("section")
        if section not in result:
            raise ValueError(f"Unknown section '{section}' in response")
        result[section].append({
            "word": item["word"],
            "section": section,
            "stem": item["stem"],
            "options": item.get("options"),
            "answer": item["answer"],
            "hint": item.get("hint"),
        })

    # Validate section sizes match the input
    for s, entries in sections_words.items():
        if len(result[s]) != len(entries):
            raise ValueError(
                f"Section {s}: expected {len(entries)} items, got {len(result[s])}"
            )
    return result


def generate(sections_words: dict) -> dict[str, list[dict]]:
    """
    Call Claude API to generate questions for all sections.
    Falls back to generator_template on any failure.
    """
    if not ANTHROPIC_AVAILABLE:
        print("Warning: anthropic package not installed. Using template generator.")
        return generator_template.generate(sections_words)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Warning: ANTHROPIC_API_KEY not set. Using template generator.")
        return generator_template.generate(sections_words)

    client = anthropic.Anthropic(api_key=api_key)

    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": _user_prompt(sections_words)}],
        )
        raw = message.content[0].text
        return _parse_response(raw, sections_words)

    except (anthropic.APIError, json.JSONDecodeError, ValueError, KeyError) as e:
        print(f"Warning: Claude API generation failed ({e}). Using template generator.")
        return generator_template.generate(sections_words)
