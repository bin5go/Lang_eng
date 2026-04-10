# PRD: Vocabulary Quiz Generator for Grade-8 Students

## Problem Statement

A grade-8 English teacher needs a reliable, repeatable way to generate vocabulary quizzes aligned to the *Great Writing 2* (and eventually *Great Writing 3*) textbook series. Currently, quiz preparation is manual — selecting words, writing context sentences, and formatting question sheets all take significant time. The tool must respect CEFR proficiency levels to ensure appropriate question types per word, highlight academic vocabulary, and produce a clean, print-ready output that can be handed directly to students.

The current v1 implementation uses hard-coded template sentences and a small dictionary of C1 definitions, which limits question variety and requires manual maintenance whenever new words or question types are needed.

---

## Solution

A Python CLI tool that:

1. Reads a structured word list (JSON) for GW2 and GW3.
2. Selects 15 words per quiz in **ascending page-number order**.
3. Calls the **Claude API** to generate high-quality, contextually varied questions for every word — replacing static templates with AI-generated questions across four structured sections.
4. Exports the finished quiz as a **print-ready DOCX** (and Markdown) file, including a teacher answer key.

### Quiz Structure (4 sections per quiz)

Each quiz is divided into four sections. Words are distributed across sections; all 15 words appear at least once.

**Section A — Multiple Choice**
One question per word for a subset of words. Students choose the best definition or synonym from four options.
> *Example:*
> What is the best meaning of the word **likely**?
> A. certain to happen
> B. probable or expected
> C. impossible under any condition
> D. already decided

**Section B — Fill in the Blank**
A context sentence with the target word removed. Students write the missing word on the line.
Hint format: a meaning clue or synonym, **not** the CEFR level.
> *Example:*
> *(synonym: probable)* — It is _______________ to rain tomorrow, so bring an umbrella.

**Section C — Error Analysis**
Each sentence contains one incorrect word (underlined). Students identify the error and write the correct word.
> *Example:*
> She studied hard; **despite**, she passed the exam easily.
> Correct word: _______________

**Section D — Real-World Application**
Short-answer prompts (1–2 sentences each). Students write a response using a specified vocabulary word and underline it.
> *Example prompt:*
> Your friend says, "I'll never be good at science because I failed one quiz." Give your friend advice using the word **likely** to explain why they are wrong to assume that.
> *Student response:* Failing one quiz does not mean you will **likely** fail the whole course — one result does not define your ability.

The stretch goal (next milestone) adds Claude API question generation and DOCX export on top of the working v1 foundation.

---

## User Stories

1. As a teacher, I want to run a single CLI command and get a ready-to-print quiz, so that I spend no time on manual formatting.
2. As a teacher, I want each quiz to cover exactly 15 words in ascending page order, so that the quiz follows the chapter sequence in the textbook.
3. As a teacher, I want Section A (MCQ) to test word definitions or synonyms, so that students practise recognising vocabulary meaning.
4. As a teacher, I want Section B (fill-in-the-blank) hints to show a meaning clue or synonym rather than a CEFR level, so that hints are pedagogically useful without giving the answer away.
5. As a teacher, I want Section C (error analysis) to present sentences with one underlined incorrect word, so that students practise noticing and correcting vocabulary misuse.
6. As a teacher, I want Section D (real-world application) to give short contextual prompts where students write 1–2 sentences using a specific vocabulary word and underline it, so that students practise using words in meaningful, authentic contexts.
7. As a teacher, I want academic vocabulary (marked *) to appear in Section D prompts, so that students build academic register in their own writing.
8. As a teacher, I want a teacher copy with the answer key for all four sections at the end of every output file, so that I can mark papers quickly.
9. As a teacher, I want to generate any specific quiz number (e.g. `--quiz 5`), so that I can regenerate or skip to any point in the word list.
10. As a teacher, I want to list all available quiz groups with their word previews (`--list`), so that I can plan which quiz to assign next.
11. As a teacher, I want the quiz exported as a DOCX file, so that I can make last-minute edits before printing.
12. As a teacher, I want the quiz also saved as a Markdown file, so that I can version-control quizzes in Git.
13. As a teacher, I want Claude API to generate all MCQ options, fill-in-the-blank sentences, error-analysis sentences, and real-world prompts, so that question quality and variety are higher than hand-written templates.
14. As a teacher, I want Claude-generated hints in Section B to reflect the word's meaning or a synonym, so that students get a useful clue without having the answer given to them.
15. As a teacher, I want Claude-generated error-analysis sentences to use a plausible but wrong word (not a random one), so that the exercise tests genuine vocabulary discrimination.
16. As a teacher, I want Claude-generated real-world prompts to include a realistic scenario and specify which vocabulary word to use, so that students understand exactly what is expected.
17. As a teacher, I want the tool to support both GW2 and GW3 word lists via a `--book` flag (e.g. `--book gw3`), so that I can use one tool across both textbooks.
18. As a teacher, I want the word list JSON for GW3 to be generated from its source images, so that no manual transcription is needed for the second book.
19. As a teacher, I want the tool to warn me if the `ANTHROPIC_API_KEY` environment variable is missing and fall back to templates, so that the tool does not crash in offline environments.
20. As a teacher, I want each quiz DOCX to include the school name, class, date, and a student name line at the top, so that it looks like a professional test paper.
21. As a teacher, I want off-list words to be treated the same as B1 for question-type selection, so that they are never skipped or cause errors.
22. As a teacher, I want the total number of available quizzes to be shown when I run `--list`, so that I can plan the whole semester.
23. As a teacher, I want previously generated quizzes to be overwritten cleanly when I regenerate them, so that stale files never accumulate.
24. As a teacher, I want to bring in a word list from any textbook by providing a JSON file that follows the standard schema, so that I am not limited to GW2 and GW3.
25. As a teacher, I want the CLI to accept a `--wordlist path/to/words.json` flag, so that I can point to any custom word list without modifying the source code.

---

## Implementation Decisions

### Modules

| Module | Responsibility |
|--------|---------------|
| **Word store** | Loads and validates `words_gw2.json` / `words_gw3.json`; sorts by page **ascending**; slices 15-word windows by quiz number. Single source of truth for word data. |
| **Question generator — template** | Produces questions from static dicts for all four section types (fallback when API unavailable). |
| **Question generator — Claude API** | Calls Claude API with all 15 words in one batch; returns structured JSON with questions for all four sections per word. |
| **Quiz builder** | Orchestrates: receives 15-word list, calls the active question generator, distributes words across sections A–D, assembles header + sections + answer key. |
| **Markdown writer** | Renders quiz object → `quiz_NN.md`. |
| **DOCX writer** | Renders quiz object → `quiz_NN.docx` using `python-docx`; includes school header, student name line. |
| **CLI** | Parses `--quiz N`, `--list`, `--book gw2|gw3`, `--no-ai` flags; wires modules together; handles missing API key gracefully. |

### Quiz section distribution (15 words)

| Section | Type | Words used | Notes |
|---------|------|-----------|-------|
| A | Multiple choice | 5 | Definition or best synonym; 4 options each |
| B | Fill in the blank | 5 | Hint = meaning clue or synonym (not CEFR level) |
| C | Error analysis | 3 | Sentence with one underlined wrong word; write correct word |
| D | Real-world application | 2 | 1–2 sentence response; underline the vocabulary word used |

Words for each section are selected by the quiz builder to spread CEFR levels and ensure academic words appear in Section D where possible.

- Both question generator modules implement the same interface: accept a list of word entries, return a quiz object with questions organised by section (A, B, C, D).
- The quiz builder is agnostic to which generator it calls — dependency injection via a flag.
- Writers accept the same quiz object — both Markdown and DOCX output share one data model.

### Claude API usage

- Model: `claude-haiku-4-5-20251001` (fast, low cost, sufficient for structured question generation).
- One batch call per quiz (15 words in a single prompt) to minimise latency and cost.
- Response parsed as JSON with shape `{ word, section, stem, options?, answer, hint? }` for each item.
- System prompt instructs Claude to: use meaning clues/synonyms (not CEFR labels) for Section B hints; use plausible near-miss words (not random) for Section C errors; craft realistic real-world scenarios for Section D.
- Falls back to template generator on parse error.

### Word data

- `--book gw2|gw3` selects a built-in word list; `--wordlist path/to/words.json` accepts any custom JSON file following the standard schema `{ word, page, level, academic }`.
- If both flags are provided, `--wordlist` takes precedence.
- The word store validates the schema on load and reports clear errors for missing or malformed fields.

### DOCX

- Library: `python-docx`.
- Header section: school name (hardcoded or `--school` flag), class, date, student name line.
- MCQ options styled with hanging indent; fill-in-the-blank underline via tab stops.

---

## Testing Decisions

**What makes a good test here:** test the external behaviour of each module (given this word list + these words, produce this question structure or this file), not internal implementation details like which dict keys were accessed.

| Module | What to test |
|--------|-------------|
| **Word store** | Sorting is correctly ascending by page; slicing gives the right 15-word window for quiz N; off-list words are included and not dropped. |
| **Question generator — template** | All four section types are produced; Section B hints are meaning/synonym clues (not CEFR labels); Section C uses a plausible wrong word; Section D prompt names the target word. |
| **Question generator — Claude API** | (Integration test, opt-in) Response parses into the expected section-keyed shape; fallback triggers correctly on a malformed response. |
| **Quiz builder** | Output contains exactly 15 words distributed across sections A–D per the defined split; answer key covers all sections. |
| **CLI** | `--list` prints the right number of quiz groups; `--quiz N` out of range prints a clear error; missing API key triggers fallback warning, not a crash. |

No existing test suite in the repo; new tests use `pytest` with plain `assert` statements.

---

## Out of Scope

- A student-facing UI or web interface (teacher-only tool).
- Score tracking, gradebook, or any form of persistent student data.
- Automatic PDF export (DOCX covers the print-ready requirement; PDF conversion is left to the OS print dialog).
- Randomising word order within a quiz (page-ascending order is a deliberate pedagogical choice).

---

## Further Notes

- **Milestones:**
  - **v1 (done):** Static template questions, Markdown output, GW2 only — `quiz_generator.py` + `words_gw2.json`.
  - **v2 (next milestone / stretch goal):** Claude API question generation, DOCX export, GW3 support (`words_gw3.json`), `--book` flag, `--no-ai` fallback, `pytest` test suite.
- **Cost estimate:** At ~800 tokens/quiz (15 words × 4 sections), `claude-haiku-4-5-20251001` costs approximately $0.001–0.002 per quiz — negligible.
- **Offline use:** `--no-ai` flag (or missing `ANTHROPIC_API_KEY`) silently falls back to v1 template behaviour, so the tool remains usable without internet access.
