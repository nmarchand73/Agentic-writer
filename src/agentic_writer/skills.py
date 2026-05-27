"""SkillsCapability factories and skill discovery."""

from __future__ import annotations

import re
from pathlib import Path

from pydantic_ai_skills import SkillsCapability

from agentic_writer.config import (
    ARCHITECT_SKILL_DIR,
    AUDITOR_SKILL_DIR,
    EDITOR_SKILL_DIR,
    WRITER_SKILL_DIR,
)


def _skill_name_from_path(path: Path) -> str | None:
    skill_md = path / "SKILL.md"
    if not skill_md.exists():
        return None
    text = skill_md.read_text(encoding="utf-8")
    match = re.search(r"^name:\s*(.+)$", text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return path.name


def list_skill_names(directories: list[Path]) -> list[str]:
    names: list[str] = []
    for directory in directories:
        if not directory.exists():
            continue
        if (directory / "SKILL.md").exists():
            name = _skill_name_from_path(directory)
            if name:
                names.append(name)
        else:
            for child in sorted(directory.iterdir()):
                if child.is_dir():
                    name = _skill_name_from_path(child)
                    if name:
                        names.append(name)
    return sorted(set(names))


def writer_capability() -> SkillsCapability:
    return SkillsCapability(directories=[str(WRITER_SKILL_DIR)])


def editor_capability() -> SkillsCapability:
    return SkillsCapability(
        directories=[str(EDITOR_SKILL_DIR), str(WRITER_SKILL_DIR)]
    )


def architect_capability() -> SkillsCapability:
    return SkillsCapability(
        directories=[str(ARCHITECT_SKILL_DIR), str(WRITER_SKILL_DIR)]
    )


def auditor_capability() -> SkillsCapability:
    return SkillsCapability(
        directories=[str(AUDITOR_SKILL_DIR), str(EDITOR_SKILL_DIR), str(WRITER_SKILL_DIR)]
    )


def list_writer_skill_names() -> list[str]:
    return list_skill_names([WRITER_SKILL_DIR])


def list_editor_skill_names() -> list[str]:
    return list_skill_names([EDITOR_SKILL_DIR, WRITER_SKILL_DIR])
