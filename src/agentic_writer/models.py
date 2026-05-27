"""Structured outputs for Writer, Editor, and CLI brief."""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator


StoryFormat = Literal["flash", "nouvelle", "novella"]
StoryLang = Literal["fr", "en"]


def humanize_slug(slug: str) -> str:
    words = [p for p in slug.replace("_", "-").split("-") if p]
    if not words:
        return slug
    words[0] = words[0].capitalize()
    return " ".join(words)


class Brief(BaseModel):
    slug: str
    pitch: str
    title: str | None = None
    format: StoryFormat = "nouvelle"
    lang: StoryLang = "fr"
    theme: str | None = None

    def resolved_title(self) -> str:
        return self.title or humanize_slug(self.slug)


class TwistSheet(BaseModel):
    twist_final: str
    mid_twist: str
    coda_bombe: str
    mensonge_omission: str
    scenes_recontextualisees: list[str] = Field(min_length=3, max_length=3)
    indices_foreshadowing: list[str] = Field(min_length=2, max_length=2)
    pitch_booktok: str

    @field_validator("pitch_booktok")
    @classmethod
    def pitch_max_fifteen_words(cls, v: str) -> str:
        words = re.findall(r"\S+", v.strip())
        if len(words) > 15:
            raise ValueError("pitch_booktok must be at most 15 words")
        return v


class WriterResult(BaseModel):
    twist_sheet: TwistSheet
    manuscript: str

    @field_validator("manuscript")
    @classmethod
    def manuscript_non_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("manuscript must not be empty")
        return v


class EditorResult(BaseModel):
    review_markdown: str
    checklist_scores: dict[str, int]
    manuscript_corrected: str

    @field_validator("checklist_scores")
    @classmethod
    def scores_in_range(cls, v: dict[str, int]) -> dict[str, int]:
        if not v:
            raise ValueError("checklist_scores must not be empty")
        for score in v.values():
            if score not in (0, 1, 2):
                raise ValueError("checklist scores must be 0, 1, or 2")
        return v


class PipelineResult(BaseModel):
    brief: Brief
    written: WriterResult
    edited: EditorResult
    output_dir: str
    blueprint: object | None = None  # StoryBlueprint when editorial v2
    audit: object | None = None  # AuditorVerdict when editorial v2
    usage_summary: str | None = None
