"""Load Brief from CLI args or YAML file."""

from __future__ import annotations

from pathlib import Path

import typer
import yaml

from agentic_writer.config import load_settings
from agentic_writer.models import Brief, StoryFormat, StoryLang


def load_brief(
    slug: str | None,
    *,
    pitch: str | None,
    brief_path: Path | None,
    format: str | None = None,
    lang: str | None = None,
) -> Brief:
    settings = load_settings()
    if brief_path:
        data = yaml.safe_load(brief_path.read_text(encoding="utf-8"))
        return Brief.model_validate(data)

    if not slug or not pitch:
        raise typer.Exit(2)

    fmt: StoryFormat = (format or settings["default_format"])  # type: ignore[assignment]
    lng: StoryLang = (lang or settings["default_lang"])  # type: ignore[assignment]
    return Brief(slug=slug, pitch=pitch, format=fmt, lang=lng)
