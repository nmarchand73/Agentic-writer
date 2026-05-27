"""Environment checks for agentic-writer doctor."""

from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

from agentic_writer.config import (
    ARCHITECT_SKILL_DIR,
    AUDITOR_SKILL_DIR,
    BUILD_STORY_SCRIPT,
    EDITOR_SKILL_DIR,
    GENERATE_FROM_MD_SCRIPT,
    PRINT_LAYOUT_SKILL_DIR,
    PROJECT_ROOT,
    WRITER_SKILL_DIR,
)


@dataclass
class DoctorReport:
    ok: bool = True
    messages: list[str] = field(default_factory=list)

    def fail(self, msg: str) -> None:
        self.ok = False
        self.messages.append(f"FAIL: {msg}")

    def warn(self, msg: str) -> None:
        self.messages.append(f"WARN: {msg}")

    def info(self, msg: str) -> None:
        self.messages.append(f"OK: {msg}")


def run_doctor(*, require_writer_skill: bool = True) -> DoctorReport:
    report = DoctorReport()
    if sys.version_info < (3, 10):
        report.fail(f"Python 3.10+ required (got {sys.version})")
    else:
        report.info(f"Python {sys.version_info.major}.{sys.version_info.minor}")

    skill_md = WRITER_SKILL_DIR / "SKILL.md"
    if require_writer_skill and not skill_md.exists():
        report.fail(f"Missing writer skill: {skill_md} (story-writer)")
    elif skill_md.exists():
        report.info("Skill story-writer present")

    editor_md = EDITOR_SKILL_DIR / "SKILL.md"
    if not editor_md.exists():
        report.warn("Editor skill manuscript-editor not found")
    else:
        report.info("Skill manuscript-editor present")

    layout_md = PRINT_LAYOUT_SKILL_DIR / "SKILL.md"
    if not layout_md.exists():
        report.warn("Print layout skill not found (print-layout)")
    else:
        report.info("Skill print-layout present")

    architect_md = ARCHITECT_SKILL_DIR / "SKILL.md"
    if not architect_md.exists():
        report.warn("Architect skill story-architect not found")
    else:
        report.info("Skill story-architect present")

    auditor_md = AUDITOR_SKILL_DIR / "SKILL.md"
    if not auditor_md.exists():
        report.warn("Auditor skill story-auditor not found")
    else:
        report.info("Skill story-auditor present")

    if BUILD_STORY_SCRIPT.exists() and GENERATE_FROM_MD_SCRIPT.exists():
        report.info("Print pipeline scripts present")
    else:
        report.warn("Missing print-layout build_story.sh or generate_from_md.js")

    if shutil.which("node"):
        report.info("Node.js available")
    else:
        report.warn("Node.js not found (required for docx export)")

    node_modules = PROJECT_ROOT / "node_modules" / "docx"
    if node_modules.exists():
        report.info("npm package docx installed")
    else:
        report.warn("Run npm install in Agentic-writer/ for docx export")

    if shutil.which("soffice") or shutil.which("libreoffice"):
        report.info("LibreOffice available for PDF")
    else:
        report.warn("LibreOffice not found (PDF export may fail)")

    return report


def doctor_exit_code(report: DoctorReport) -> int:
    return 0 if report.ok else 1
