"""Artifact persistence and prompt building."""

from __future__ import annotations

import json
from pathlib import Path

from agentic_writer.config import output_dir
from agentic_writer.log_config import get_logger
from agentic_writer.models import Brief, EditorResult, WriterResult

log = get_logger("io")


def save_artifacts(brief: Brief, written: WriterResult, edited: EditorResult) -> Path:
    work = output_dir(brief.slug)
    work.mkdir(parents=True, exist_ok=True)
    (work / "twist_sheet.json").write_text(
        json.dumps(written.twist_sheet.model_dump(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (work / "draft_manuscript.md").write_text(written.manuscript, encoding="utf-8")
    (work / "review.md").write_text(edited.review_markdown, encoding="utf-8")
    (work / "manuscript_final.md").write_text(
        edited.manuscript_corrected, encoding="utf-8"
    )
    log.debug(
        "Artefacts écrits : twist_sheet.json, draft_manuscript.md, review.md, manuscript_final.md"
    )
    return work


def build_edit_prompt(written: WriterResult) -> str:
    twist = written.twist_sheet
    return (
        "Relis et corrige le manuscrit ci-dessous.\n"
        "Les twists sont FIGÉS — ne modifie pas twist_sheet, seulement style et continuité.\n\n"
        f"TWIST FINAL (figé) : {twist.twist_final}\n"
        f"MID-TWIST (figé) : {twist.mid_twist}\n"
        f"CODA (figée) : {twist.coda_bombe}\n\n"
        f"--- MANUSCRIT ---\n{written.manuscript}\n"
    )
