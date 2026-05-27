"""Chapter writer agent — one chapter per call (v2)."""

from __future__ import annotations

from pydantic import BaseModel, Field

from pydantic_ai import Agent

from agentic_writer.agent_instructions import CHAPTER_WRITER_INSTRUCTIONS
from agentic_writer.config import load_settings
from agentic_writer.skills import writer_capability


class ChapterWriterResult(BaseModel):
    content: str = Field(min_length=50)


def create_chapter_writer_agent() -> Agent[None, ChapterWriterResult]:
    settings = load_settings()
    model = settings.get("model_chapter") or settings["model_writer"]
    return Agent(
        model,
        instructions=CHAPTER_WRITER_INSTRUCTIONS,
        output_type=ChapterWriterResult,
        capabilities=[writer_capability()],
    )
