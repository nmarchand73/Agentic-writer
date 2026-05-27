"""Inject skill files into pipeline prompts (deterministic — no load_skill required)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from agentic_writer.config import (
    ARCHITECT_SKILL_DIR,
    AUDITOR_SKILL_DIR,
    EDITOR_SKILL_DIR,
    WRITER_SKILL_DIR,
)

REVIEW_RUBRIC = EDITOR_SKILL_DIR / "references" / "review_rubric.md"
NARRATIVE_STYLE_GUIDE = WRITER_SKILL_DIR / "references" / "narrative_style_guide.md"


def strip_yaml_frontmatter(text: str) -> str:
    """Return markdown body after optional YAML frontmatter."""
    if not text.startswith("---"):
        return text.strip()
    end = text.find("\n---", 3)
    if end == -1:
        return text.strip()
    return text[end + 4 :].lstrip("\n").strip()


def read_skill_body(skill_dir: Path) -> str:
    path = skill_dir / "SKILL.md"
    if not path.is_file():
        msg = f"Missing skill: {path}"
        raise FileNotFoundError(msg)
    return strip_yaml_frontmatter(path.read_text(encoding="utf-8"))


def read_skill_file(path: Path) -> str:
    if not path.is_file():
        msg = f"Missing skill resource: {path}"
        raise FileNotFoundError(msg)
    return path.read_text(encoding="utf-8").strip()


def format_injected_skill(title: str, body: str) -> str:
    return f"## Skill injectée — {title}\n\n{body.strip()}\n\n"


@lru_cache
def architect_skill_context() -> str:
    """Primary: story-architect; secondary: narrative style guide for McFadden structure."""
    parts = [
        format_injected_skill("story-architect", read_skill_body(ARCHITECT_SKILL_DIR)),
    ]
    if NARRATIVE_STYLE_GUIDE.is_file():
        parts.append(
            format_injected_skill(
                "story-writer / narrative_style_guide",
                read_skill_file(NARRATIVE_STYLE_GUIDE),
            )
        )
    return "".join(parts)


@lru_cache
def writer_skill_context() -> str:
    return format_injected_skill("story-writer", read_skill_body(WRITER_SKILL_DIR))


@lru_cache
def editor_skill_context() -> str:
    parts = [
        format_injected_skill(
            "manuscript-editor", read_skill_body(EDITOR_SKILL_DIR)
        ),
        format_injected_skill(
            "manuscript-editor / review_rubric", read_skill_file(REVIEW_RUBRIC)
        ),
    ]
    return "".join(parts)


@lru_cache
def auditor_skill_context() -> str:
    parts = [
        format_injected_skill("story-auditor", read_skill_body(AUDITOR_SKILL_DIR)),
        format_injected_skill(
            "manuscript-editor / review_rubric", read_skill_file(REVIEW_RUBRIC)
        ),
    ]
    return "".join(parts)
