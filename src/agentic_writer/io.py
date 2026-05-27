"""Artifact persistence and prompt building."""

from __future__ import annotations

import json
from pathlib import Path

from agentic_writer.config import output_dir
from agentic_writer.log_config import get_logger
from agentic_writer.models import Brief, EditorResult, WriterResult
from agentic_writer.skill_content import editor_skill_context

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


def build_edit_prompt(written: WriterResult, brief: Brief) -> str:
    twist = written.twist_sheet
    return (
        editor_skill_context()
        + f"## Brief\n"
        f"- Format : {brief.format}\n"
        f"- Langue : {brief.lang}\n"
        f"- Titre : {brief.resolved_title()}\n\n"
        "## Twists figés (sens inchangé — prose seulement)\n"
        f"- Twist final : {twist.twist_final}\n"
        f"- Mid-twist : {twist.mid_twist}\n"
        f"- Coda : {twist.coda_bombe}\n"
        f"- Mensonge / omission : {twist.mensonge_omission}\n"
        f"- Pitch BookTok : {twist.pitch_booktok}\n\n"
        "## Livrable\n"
        "Retourne un `EditorResult` :\n"
        "- `review_markdown` avec exemples concrets pour scores < 2.\n"
        "- `checklist_scores` : voice, twists_intact, foreshadowing, chapter_hooks, "
        "pitch_booktok, format_length, continuity (0–2).\n"
        "- `manuscript_corrected` : manuscrit entier, structure `#` / `##` conservée.\n\n"
        f"--- MANUSCRIT ---\n{written.manuscript}\n"
    )
