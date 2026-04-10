"""Tests for CLI behaviour (quiz_generator.py main())."""

import sys
import subprocess
from pathlib import Path

import pytest

CLI = str(Path(__file__).parent.parent / "quiz_generator.py")


def run(*args):
    result = subprocess.run(
        [sys.executable, CLI, *args],
        capture_output=True,
        text=True,
    )
    return result


# ── --list ───────────────────────────────────────────────────────────────────

def test_list_gw2_shows_quiz_count():
    r = run("--list")
    assert r.returncode == 0
    assert "12 quizzes" in r.stdout


def test_list_gw3_shows_quiz_count():
    r = run("--list", "--book", "gw3")
    assert r.returncode == 0
    assert "quizzes" in r.stdout


def test_list_shows_ascending_pages():
    r = run("--list")
    assert r.returncode == 0
    # Quiz 01 should start at a lower page than Quiz 02
    lines = [l for l in r.stdout.splitlines() if l.startswith("Quiz")]
    assert len(lines) >= 2
    # Each line contains "pp. X–Y"; X for quiz 01 should be < X for quiz 02
    import re
    pages = [int(re.search(r"pp\. (\d+)", l).group(1)) for l in lines[:2]]
    assert pages[0] < pages[1]


# ── --quiz N ─────────────────────────────────────────────────────────────────

def test_quiz_generates_markdown(tmp_path):
    r = run("--quiz", "1", "--no-ai")
    assert r.returncode == 0
    assert "Markdown saved to" in r.stdout


def test_quiz_out_of_range_prints_error():
    r = run("--quiz", "999")
    assert r.returncode == 0
    assert "Error" in r.stdout


def test_quiz_zero_prints_error():
    r = run("--quiz", "0")
    assert r.returncode == 0
    assert "Error" in r.stdout


def test_quiz_gw3_generates_markdown():
    r = run("--quiz", "1", "--book", "gw3", "--no-ai")
    assert r.returncode == 0
    assert "Markdown saved to" in r.stdout


# ── --no-ai fallback ─────────────────────────────────────────────────────────

def test_no_ai_flag_produces_output():
    r = run("--quiz", "1", "--no-ai")
    assert r.returncode == 0
    assert "Markdown saved to" in r.stdout
    # Should NOT emit a Claude API warning
    assert "Warning: ANTHROPIC_API_KEY" not in r.stdout


def test_missing_api_key_falls_back_gracefully(monkeypatch):
    """When ANTHROPIC_API_KEY is unset and --no-ai is NOT passed, tool warns and continues."""
    import os
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    result = subprocess.run(
        [sys.executable, CLI, "--quiz", "2"],
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0
    assert "Warning" in result.stdout or "Markdown saved to" in result.stdout
