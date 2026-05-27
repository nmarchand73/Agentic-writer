"""Chapter writer agent — one chapter per call (v2)."""

from __future__ import annotations

from pydantic import BaseModel, Field

from pydantic_ai import Agent

from agentic_writer.config import load_settings
from agentic_writer.skills import writer_capability


class ChapterWriterResult(BaseModel):
    content: str = Field(min_length=50)


def create_chapter_writer_agent() -> Agent[None, ChapterWriterResult]:
    settings = load_settings()
    model = settings.get("model_chapter") or settings["model_writer"]
    return Agent(
        model,
        instructions=(
            "Tu es l'écrivain chapitre (skill story-writer). "
            "Rédige UN seul chapitre en markdown, voix McFadden, sans résumer les autres chapitres. "
            "Ne change pas les twists fournis."
        ),
        output_type=ChapterWriterResult,
        capabilities=[writer_capability()],
    )
