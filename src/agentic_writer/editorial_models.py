"""Modèles structurés — pipeline éditorial v2."""

from __future__ import annotations

from pydantic import BaseModel, Field

from agentic_writer.models import TwistSheet


class ChapterOutline(BaseModel):
    index: int = Field(ge=0)
    title: str
    beat: str
    hook: str = ""
    target_words: int = Field(ge=200, le=3_500)


class StoryBlueprint(BaseModel):
    title: str
    twist_sheet: TwistSheet
    chapters: list[ChapterOutline] = Field(min_length=1)
    prologue_beat: str | None = None


class ArchitectResult(BaseModel):
    blueprint: StoryBlueprint


class ChapterDraft(BaseModel):
    index: int
    title: str
    content: str

    @classmethod
    def from_outline(cls, outline: ChapterOutline, content: str) -> ChapterDraft:
        return cls(index=outline.index, title=outline.title, content=content)


class AuditorVerdict(BaseModel):
    passed: bool
    overall_score: int = Field(ge=0, le=100)
    checklist_scores: dict[str, int]
    issues: list[str] = Field(default_factory=list)
    chapters_to_rewrite: list[int] = Field(default_factory=list)
    review_markdown: str
