"""Unit tests — plan chapitres v2."""

from agentic_writer.editorial_guards import check_manuscript_length, word_count
from agentic_writer.editorial_plan import chapter_plan_for
from agentic_writer.models import Brief


def test_flash_plan_one_chapter():
    plan = chapter_plan_for("flash")
    assert plan.chapter_count == 1
    assert plan.min_total_words < plan.max_total_words


def test_word_count_guard():
    brief = Brief(slug="x", pitch="p", format="flash")
    short = "mot " * 100
    issues = check_manuscript_length(brief, short)
    assert any("longueur" in i for i in issues)
    assert word_count(short) == 100
