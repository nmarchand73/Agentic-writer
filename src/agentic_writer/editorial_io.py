"""Prompts et assemblage manuscrit — pipeline v2."""

from __future__ import annotations

import json
from pathlib import Path
from agentic_writer.editorial_models import (
    AuditorVerdict,
    ChapterDraft,
    ChapterOutline,
    StoryBlueprint,
)
from agentic_writer.editorial_plan import FormatChapterPlan
from agentic_writer.models import Brief, EditorResult, TwistSheet
from agentic_writer.rewrite_feedback import (
    format_auditor_rewrite_section,
    format_editor_rewrite_section,
)
from agentic_writer.skill_content import (
    architect_skill_context,
    auditor_skill_context,
    writer_skill_context,
)

_CHECKLIST_KEYS = (
    "voice, twists_intact, foreshadowing, chapter_hooks, "
    "pitch_booktok, format_length, continuity"
)


def build_architect_prompt(brief: Brief, plan: FormatChapterPlan) -> str:
    prologue_line = (
        f"Prologue : oui — remplir `prologue_beat` (scène choc 200–400 mots, sans rédiger le texte)."
        if plan.include_prologue
        else "Prologue : non — laisser `prologue_beat` vide ou null."
    )
    return (
        architect_skill_context()
        + f"## Brief\n"
        f"- Titre : {brief.resolved_title()}\n"
        f"- Slug : {brief.slug}\n"
        f"- Format : {brief.format}\n"
        f"- Langue : {brief.lang}\n"
        f"- Pitch : {brief.pitch}\n\n"
        f"## Contraintes plan\n"
        f"- Chapitres narratifs : **exactement {plan.chapter_count}** entrées dans `chapters` "
        f"(index 1…{plan.chapter_count}).\n"
        f"- ~{plan.words_per_chapter} mots cible par chapitre (`target_words`).\n"
        f"- Longueur totale visée : {plan.min_total_words}–{plan.max_total_words} mots.\n"
        f"- {prologue_line}\n\n"
        "## Livrable\n"
        "Retourne un `ArchitectResult` :\n"
        "- `blueprint.title` aligné sur le titre ci-dessus.\n"
        "- `blueprint.twist_sheet` complet (tous les champs Pydantic).\n"
        "- `blueprint.chapters[]` : title, beat, hook, target_words pour chaque index.\n"
        "- Mid-twist narratif ~50–60 % de l'arc ; indices de foreshadowing en première moitié.\n"
        "Pas de prose de roman — plan uniquement."
    )


def build_prologue_prompt(brief: Brief, blueprint: StoryBlueprint) -> str:
    twist = blueprint.twist_sheet
    return (
        writer_skill_context()
        + f"## Prologue choc\n"
        f"- Langue : {brief.lang}\n"
        f"- Cible : 200–400 mots dans `content`.\n"
        f"- Beat : {blueprint.prologue_beat}\n\n"
        "## Twists (figés — ne pas tout révéler)\n"
        f"- Twist final (à ménager) : {twist.twist_final}\n"
        f"- Mensonge / omission : {twist.mensonge_omission}\n\n"
        "Accroche immédiate, voix 1re personne présent, terminer sur une tension ou question.\n"
        "Retourne un `ChapterWriterResult` JSON : {\"content\": \"...\"} (pas de texte hors JSON).\n"
        "Corps markdown dans `content` (pas de titre `#` du livre)."
    )


def prior_text_before_chapter(
    blueprint: StoryBlueprint,
    drafts_by_index: dict[int, ChapterDraft],
    *,
    before_index: int,
    prologue_text: str | None,
) -> str | None:
    """Concatenate prologue + prior chapters for continuity on partial rewrites."""
    parts: list[str] = []
    if prologue_text and prologue_text.strip():
        parts.append(prologue_text.strip())
    for ch in sorted(blueprint.chapters, key=lambda c: c.index):
        if ch.index >= before_index:
            break
        draft = drafts_by_index.get(ch.index)
        if draft and draft.content.strip():
            parts.append(draft.content.strip())
    if not parts:
        return None
    combined = "\n\n".join(parts)
    return combined[-800:]


def build_chapter_prompt(
    brief: Brief,
    blueprint: StoryBlueprint,
    chapter: ChapterOutline,
    *,
    previous_excerpt: str | None,
    total_chapters: int,
    auditor_verdict: AuditorVerdict | None = None,
) -> str:
    twist = blueprint.twist_sheet
    prev = ""
    if previous_excerpt:
        prev = (
            "\n## Continuité (fin du bloc précédent)\n"
            f"{previous_excerpt[-800:]}\n"
        )
    feedback = ""
    if auditor_verdict is not None:
        feedback = format_auditor_rewrite_section(
            auditor_verdict,
            chapter_index=chapter.index,
        )
    return (
        writer_skill_context()
        + feedback
        + f"## Chapitre {chapter.index} / {total_chapters} : « {chapter.title} »\n"
        f"- Langue : {brief.lang}\n"
        f"- Cible : ~{chapter.target_words} mots (±15 %)\n"
        f"- Beat : {chapter.beat}\n"
        f"- Hook de fin (obligatoire) : {chapter.hook}\n"
        f"{prev}\n"
        "## Twists figés (cohérence — ne pas contredire)\n"
        f"- Twist final : {twist.twist_final}\n"
        f"- Mid-twist : {twist.mid_twist}\n"
        f"- Coda : {twist.coda_bombe}\n\n"
        "Retourne un `ChapterWriterResult` JSON : {\"content\": \"...\"} (pas de texte hors JSON).\n"
        "Rédige **ce chapitre seul** dans `content` (markdown, pas de récap des autres chapitres)."
    )


def build_auditor_prompt(
    brief: Brief,
    twist: TwistSheet,
    manuscript: str,
    guard_issues: list[str],
) -> str:
    guards = "\n".join(f"- {g}" for g in guard_issues) or "- (aucune alerte programmatique)"
    return (
        auditor_skill_context()
        + f"## Contexte\n"
        f"- Format : {brief.format}\n"
        f"- Langue : {brief.lang}\n"
        f"- Titre : {brief.resolved_title()}\n\n"
        f"## Alertes programmatiques (à intégrer dans ton verdict)\n"
        f"{guards}\n\n"
        "## Twists de référence (figés)\n"
        f"- Twist final : {twist.twist_final}\n"
        f"- Mid-twist : {twist.mid_twist}\n"
        f"- Coda : {twist.coda_bombe}\n"
        f"- Pitch BookTok : {twist.pitch_booktok}\n\n"
        "## Livrable\n"
        "Retourne un `AuditorVerdict` :\n"
        f"- `checklist_scores` avec clés : {_CHECKLIST_KEYS}\n"
        "- `passed=true` si `overall_score` ≥ 70 et aucun critère à 0.\n"
        "- `chapters_to_rewrite` : [] ou 1–2 index de chapitres faibles seulement.\n"
        "- `issues` et `review_markdown` : concrets — ils seront injectés dans les prompts "
        "de réécriture des chapitres concernés et dans la passe éditeur suivante.\n\n"
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
