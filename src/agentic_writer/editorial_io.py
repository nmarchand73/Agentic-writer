"""Prompts et assemblage manuscrit — pipeline v2."""

from __future__ import annotations

import json
from pathlib import Path

from agentic_writer.editorial_models import (
    ChapterDraft,
    ChapterOutline,
    StoryBlueprint,
)
from agentic_writer.editorial_plan import FormatChapterPlan, chapter_plan_for
from agentic_writer.models import Brief, TwistSheet


def build_architect_prompt(brief: Brief, plan: FormatChapterPlan) -> str:
    prologue = "avec prologue_beat (200–400 mots prévus)" if plan.include_prologue else "sans prologue"
    return (
        f"Conçois le plan complet d'une histoire de suspense psychologique domestique.\n"
        f"Titre : {brief.resolved_title()}\n"
        f"Slug : {brief.slug}\n"
        f"Format : {brief.format}\n"
        f"Langue : {brief.lang}\n"
        f"Pitch : {brief.pitch}\n"
        f"Chapitres narratifs : exactement {plan.chapter_count} entrées dans chapters "
        f"(index 1..{plan.chapter_count}), ~{plan.words_per_chapter} mots cible chacun.\n"
        f"Prologue : {prologue}.\n"
        f"Longueur totale visée : {plan.min_total_words}–{plan.max_total_words} mots.\n\n"
        "Retourne un ArchitectResult : twist_sheet complet + chapters avec title, beat, hook, "
        "target_words."
    )


def build_chapter_prompt(
    brief: Brief,
    blueprint: StoryBlueprint,
    chapter: ChapterOutline,
    *,
    previous_excerpt: str | None,
) -> str:
    twist = blueprint.twist_sheet
    prev = (
        f"\nFin du chapitre précédent (continuité) :\n{previous_excerpt[-800:]}\n"
        if previous_excerpt
        else ""
    )
    return (
        f"Rédige le chapitre {chapter.index} : « {chapter.title} ».\n"
        f"Langue : {brief.lang}. Cible : ~{chapter.target_words} mots.\n"
        f"Beat : {chapter.beat}\n"
        f"Hook de fin : {chapter.hook}\n"
        f"{prev}\n"
        f"TWIST FINAL (figé) : {twist.twist_final}\n"
        f"MID-TWIST (figé) : {twist.mid_twist}\n"
        f"CODA (figée) : {twist.coda_bombe}\n\n"
        "Corps en markdown (## optionnel). Pas de récap des autres chapitres."
    )


def build_auditor_prompt(
    brief: Brief,
    twist: TwistSheet,
    manuscript: str,
    guard_issues: list[str],
) -> str:
    guards = "\n".join(f"- {g}" for g in guard_issues) or "(aucun)"
    return (
        f"Audite ce manuscrit format {brief.format} / {brief.lang}.\n"
        f"Problèmes détectés programmatiquement :\n{guards}\n\n"
        f"TWIST FINAL : {twist.twist_final}\n"
        f"MID-TWIST : {twist.mid_twist}\n"
        f"CODA : {twist.coda_bombe}\n\n"
        f"--- MANUSCRIT ---\n{manuscript}\n"
    )


def assemble_manuscript(
    blueprint: StoryBlueprint,
    drafts: list[ChapterDraft],
    *,
    prologue_text: str | None = None,
) -> str:
    parts: list[str] = [f"# {blueprint.title}\n"]
    if prologue_text and prologue_text.strip():
        parts.append(f"## Prologue\n\n{prologue_text.strip()}\n")
    by_index = {d.index: d for d in drafts}
    for ch in blueprint.chapters:
        draft = by_index.get(ch.index)
        if not draft:
            continue
        parts.append(f"## {draft.title}\n\n{draft.content.strip()}\n")
    return "\n".join(parts)


def save_chapter_artifacts(
    work: Path,
    blueprint: StoryBlueprint,
    drafts: list[ChapterDraft],
) -> None:
    work.mkdir(parents=True, exist_ok=True)
    (work / "blueprint.json").write_text(
        json.dumps(blueprint.model_dump(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    chapters_dir = work / "chapters"
    chapters_dir.mkdir(exist_ok=True)
    for draft in drafts:
        safe = f"{draft.index:02d}-{draft.title[:40].replace('/', '-')}.md"
        (chapters_dir / safe).write_text(draft.content, encoding="utf-8")


def normalize_blueprint_chapters(
    blueprint: StoryBlueprint,
    plan: FormatChapterPlan,
) -> StoryBlueprint:
    """Trim or pad chapter list to expected count (keeps architect output usable)."""
    chapters = sorted(blueprint.chapters, key=lambda c: c.index)
    if len(chapters) > plan.chapter_count:
        chapters = chapters[: plan.chapter_count]
    while len(chapters) < plan.chapter_count:
        n = len(chapters) + 1
        chapters.append(
            ChapterOutline(
                index=n,
                title=f"Chapitre {n}",
                beat="À développer",
                hook="Question ouverte",
                target_words=plan.words_per_chapter,
            )
        )
    for i, ch in enumerate(chapters, start=1):
        ch.index = i
        if ch.target_words <= 0:
            ch.target_words = plan.words_per_chapter
    return blueprint.model_copy(update={"chapters": chapters})
