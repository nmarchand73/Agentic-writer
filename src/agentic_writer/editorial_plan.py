"""Plan chapitres v2 — cibles par format (skill story-writer)."""

from __future__ import annotations

from dataclasses import dataclass

from agentic_writer.models import StoryFormat


@dataclass(frozen=True, slots=True)
class FormatChapterPlan:
    chapter_count: int
    words_per_chapter: int
    min_total_words: int
    max_total_words: int
    include_prologue: bool


FORMAT_CHAPTER_PLANS: dict[StoryFormat, FormatChapterPlan] = {
    "flash": FormatChapterPlan(
        chapter_count=1,
        words_per_chapter=1_500,
        min_total_words=600,
        max_total_words=2_500,
        include_prologue=True,
    ),
    "nouvelle": FormatChapterPlan(
        chapter_count=7,
        words_per_chapter=1_200,
        min_total_words=7_000,
        max_total_words=16_000,
        include_prologue=True,
    ),
    "novella": FormatChapterPlan(
        chapter_count=16,
        words_per_chapter=2_000,
        min_total_words=28_000,
        max_total_words=52_000,
        include_prologue=True,
    ),
}


def chapter_plan_for(format: StoryFormat) -> FormatChapterPlan:
    return FORMAT_CHAPTER_PLANS[format]
