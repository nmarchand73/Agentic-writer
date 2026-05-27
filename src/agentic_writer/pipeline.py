"""Pipeline récit — architecte → chapitres → editor → auditeur."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any, Union

from agentic_writer.cleanup import cleanup_work_dir
from agentic_writer.export_names import export_base_name
from agentic_writer.editorial_guards import (
    check_manuscript_length,
    check_twist_sheet,
    merge_guard_issues,
)
from agentic_writer.editorial_io import (
    assemble_manuscript,
    build_architect_prompt,
    build_auditor_prompt,
    build_chapter_prompt,
    build_prologue_prompt,
    normalize_blueprint_chapters,
    prior_text_before_chapter,
    save_chapter_artifacts,
)
from agentic_writer.editorial_models import (
    AuditorVerdict,
    ChapterDraft,
    StoryBlueprint,
)
from agentic_writer.editorial_plan import chapter_plan_for
from agentic_writer.io import build_edit_prompt, save_artifacts
from agentic_writer.log_config import get_logger
from agentic_writer.models import Brief, EditorResult, PipelineResult, WriterResult
from agentic_writer.pipeline_progress import (
    log_pipeline_complete,
    log_pipeline_plan,
    log_step_done,
    log_step_start,
)
from agentic_writer.pipeline_agents import run_agent_tracked
from agentic_writer.pipeline_steps import pipeline_step_labels
from agentic_writer.usage_cost import UsageLedger

if TYPE_CHECKING:
    from pydantic_ai import Agent

    from agentic_writer.agents.chapter_writer import ChapterWriterResult
    from agentic_writer.editorial_models import ArchitectResult

log = get_logger("pipeline")

StepHook = Callable[[int, str], Awaitable[None] | None]
UsageHook = Callable[[UsageLedger], Awaitable[None] | None]
DoneDetail = Union[str, Callable[[], str | None], None]

class PipelineError(Exception):
    """Pipeline step failed."""


def _step_index(labels: list[str], needle: str) -> int:
    key = needle.lower()
    for i, label in enumerate(labels):
        if key in label.lower():
            return i
    raise PipelineError(f"Étape introuvable dans le pipeline : {needle!r}")


async def _maybe_await(result: Awaitable[None] | None) -> None:
    if result is not None:
        await result


async def _run_step(
    index: int,
    total: int,
    label: str,
    *,
    on_step_start: StepHook | None,
    on_step_complete: StepHook | None,
    work: Callable[[], Awaitable[None] | None],
    done_detail: DoneDetail = None,
) -> None:
    log_step_start(index, total, label)
    await _maybe_await(on_step_start(index, "running") if on_step_start else None)
    await _maybe_await(work())
    detail = done_detail() if callable(done_detail) else done_detail
    log_step_done(index, total, label, detail=detail)
    await _maybe_await(on_step_complete(index, "completed") if on_step_complete else None)


async def _write_chapters(
    brief: Brief,
    blueprint: StoryBlueprint,
    chapter_agent: Agent[None, ChapterWriterResult],
    *,
    ledger: UsageLedger,
    chapter_model: str,
    on_usage: UsageHook | None = None,
    rewrite_indices: set[int] | None = None,
    existing_drafts: list[ChapterDraft] | None = None,
    existing_prologue: str | None = None,
    auditor_verdict: AuditorVerdict | None = None,
) -> tuple[list[ChapterDraft], str | None]:
    from agentic_writer.agents.chapter_writer import ChapterWriterResult

    drafts_by_index: dict[int, ChapterDraft] = {}
    existing_by_index = {d.index: d for d in (existing_drafts or [])}
    partial = rewrite_indices is not None
    previous: str | None = existing_prologue if partial else None
    prologue_text: str | None = existing_prologue if partial else None
    plan = chapter_plan_for(brief.format)

    total = len(blueprint.chapters)

    if plan.include_prologue and blueprint.prologue_beat and not partial:
        prologue_result = await run_agent_tracked(
            chapter_agent,
            build_prologue_prompt(brief, blueprint),
            ledger=ledger,
            label="prologue",
            model=chapter_model,
            on_usage=on_usage,
        )
        prologue_text = prologue_result.output.content
        previous = prologue_text

    for chapter in blueprint.chapters:
        if partial and chapter.index not in rewrite_indices:
            continue
        if partial:
            merged = {**existing_by_index, **drafts_by_index}
            excerpt = prior_text_before_chapter(
                blueprint,
                merged,
                before_index=chapter.index,
                prologue_text=prologue_text,
            )
        else:
            excerpt = previous
        prompt = build_chapter_prompt(
            brief,
            blueprint,
            chapter,
            previous_excerpt=excerpt,
            total_chapters=total,
            auditor_verdict=auditor_verdict if partial else None,
        )
        chapter_result = await run_agent_tracked(
            chapter_agent,
            prompt,
            ledger=ledger,
            label=f"chapitre {chapter.index}",
            model=chapter_model,
            on_usage=on_usage,
        )
        content = chapter_result.output.content
        draft = ChapterDraft.from_outline(chapter, content)
        drafts_by_index[chapter.index] = draft
        previous = content

    ordered = [drafts_by_index[i] for i in sorted(drafts_by_index)]
    return ordered, prologue_text


async def run_pipeline(
    brief: Brief,
    *,
    md_only: bool = False,
    architect: Agent[None, ArchitectResult] | None = None,
    chapter_writer: Agent[None, ChapterWriterResult] | None = None,
    editor: Agent[None, EditorResult] | None = None,
    auditor: Agent[None, AuditorVerdict] | None = None,
    on_step_start: StepHook | None = None,
    on_step_complete: StepHook | None = None,
    on_usage: UsageHook | None = None,
) -> PipelineResult:
    from agentic_writer.agents import create_editor_agent
    from agentic_writer.agents.architect import create_architect_agent
    from agentic_writer.agents.auditor import create_auditor_agent
    from agentic_writer.agents.chapter_writer import (
        ChapterWriterResult,
        create_chapter_writer_agent,
    )
    from agentic_writer.config import load_settings
    from agentic_writer.docx_build import build_docx
    from agentic_writer.editorial_models import ArchitectResult

    settings = load_settings()
    max_retries = settings["max_audit_retries"]
    labels = pipeline_step_labels(include_export=not md_only)
    total = len(labels)
    idx_brief = _step_index(labels, "valider le brief")
    idx_architect = _step_index(labels, "architecte")
    idx_chapters = _step_index(labels, "writer")
    idx_editor = _step_index(labels, "editor")
    idx_auditor = _step_index(labels, "auditeur")
    idx_artifacts = _step_index(labels, "artefacts")
    idx_print = _step_index(labels, "print layout") if not md_only else None
    idx_delivery = total - 1

    log_pipeline_plan(brief.slug, labels, md_only=md_only)

    architect_agent = architect or create_architect_agent()
    chapter_agent = chapter_writer or create_chapter_writer_agent()
    editor_agent = editor or create_editor_agent()
    auditor_agent = auditor or create_auditor_agent()

    ledger = UsageLedger()
    chapter_model = settings.get("model_chapter") or settings["model_writer"]

    plan = chapter_plan_for(brief.format)
    blueprint_holder: dict[str, StoryBlueprint] = {}
    drafts_holder: dict[str, list[ChapterDraft]] = {}
    prologue_holder: dict[str, str | None] = {"text": None}
    written_holder: dict[str, WriterResult] = {}
    edited_holder: dict[str, EditorResult] = {}
    audit_holder: dict[str, AuditorVerdict] = {}
    work_holder: dict[str, Path] = {}

    async def _brief() -> None:
        log.debug(
            "brief slug={} format={} chapters={}",
            brief.slug,
            brief.format,
            plan.chapter_count,
        )

    await _run_step(
        idx_brief,
        total,
        labels[idx_brief],
        on_step_start=on_step_start,
        on_step_complete=on_step_complete,
        work=_brief,
        done_detail=f"{brief.format} / {brief.lang}",
    )

    async def _architect() -> None:
        arch_result = await run_agent_tracked(
            architect_agent,
            build_architect_prompt(brief, plan),
            ledger=ledger,
            label="architecte",
            model=settings["model_architect"],
            on_usage=on_usage,
        )
        blueprint_holder["bp"] = normalize_blueprint_chapters(
            arch_result.output.blueprint, plan
        )

    await _run_step(
        idx_architect,
        total,
        labels[idx_architect],
        on_step_start=on_step_start,
        on_step_complete=on_step_complete,
        work=_architect,
        done_detail=lambda: (
            f"{plan.chapter_count} chapitres planifiés · {ledger.summary()}"
        ),
    )
    blueprint = blueprint_holder["bp"]

    async def _chapters() -> None:
        drafts, prologue = await _write_chapters(
            brief,
            blueprint,
            chapter_agent,
            ledger=ledger,
            chapter_model=chapter_model,
            on_usage=on_usage,
        )
        drafts_holder["drafts"] = drafts
        prologue_holder["text"] = prologue

    await _run_step(
        idx_chapters,
        total,
        labels[idx_chapters],
        on_step_start=on_step_start,
        on_step_complete=on_step_complete,
        work=_chapters,
        done_detail=lambda: (
            f"{len(drafts_holder['drafts'])} chapitres rédigés · {ledger.summary()}"
        ),
    )

    def _manuscript() -> str:
        return assemble_manuscript(
            blueprint,
            drafts_holder["drafts"],
            prologue_text=prologue_holder["text"],
        )

    manuscript = _manuscript()
    written_holder["out"] = WriterResult(
        twist_sheet=blueprint.twist_sheet,
        manuscript=manuscript,
    )

    async def _editor() -> None:
        edit_result = await run_agent_tracked(
            editor_agent,
            build_edit_prompt(written_holder["out"], brief),
            ledger=ledger,
            label="éditeur",
            model=settings["model_editor"],
            on_usage=on_usage,
        )
        edited_holder["out"] = edit_result.output

    await _run_step(
        idx_editor,
        total,
        labels[idx_editor],
        on_step_start=on_step_start,
        on_step_complete=on_step_complete,
        work=_editor,
        done_detail=lambda: ledger.summary(),
    )

    async def _audit_loop() -> None:
        retries = 0
        while True:
            corrected = edited_holder["out"].manuscript_corrected
            guards = merge_guard_issues(
                check_twist_sheet(blueprint.twist_sheet),
                check_manuscript_length(brief, corrected),
            )
            audit_result = await run_agent_tracked(
                auditor_agent,
                build_auditor_prompt(
                    brief,
                    blueprint.twist_sheet,
                    corrected,
                    guards,
                ),
                ledger=ledger,
                label=f"auditeur (tour {retries + 1})",
                model=settings["model_auditor"],
                on_usage=on_usage,
            )
            verdict = audit_result.output
            audit_holder["v"] = verdict

            rewrite = set(verdict.chapters_to_rewrite)
            if verdict.passed or not rewrite or retries >= max_retries:
                break

            retries += 1
            log.info("Réécriture chapitres {} (retours auditeur)", sorted(rewrite))
            prior_edit = edited_holder["out"]
            new_drafts, _ = await _write_chapters(
                brief,
                blueprint,
                chapter_agent,
                ledger=ledger,
                chapter_model=chapter_model,
                on_usage=on_usage,
                rewrite_indices=rewrite,
                existing_drafts=drafts_holder["drafts"],
                existing_prologue=prologue_holder["text"],
                auditor_verdict=verdict,
            )
            by_idx = {d.index: d for d in drafts_holder["drafts"]}
            for d in new_drafts:
                by_idx[d.index] = d
            drafts_holder["drafts"] = [by_idx[i] for i in sorted(by_idx)]
            manuscript = _manuscript()
            written_holder["out"] = WriterResult(
                twist_sheet=blueprint.twist_sheet,
                manuscript=manuscript,
            )
            edit_result = await run_agent_tracked(
                editor_agent,
                build_edit_prompt(
                    written_holder["out"],
                    brief,
                    auditor_verdict=verdict,
                    prior_editor=prior_edit,
                ),
                ledger=ledger,
                label="éditeur (post-réécriture)",
                model=settings["model_editor"],
                on_usage=on_usage,
            )
            edited_holder["out"] = edit_result.output

    await _run_step(
        idx_auditor,
        total,
        labels[idx_auditor],
        on_step_start=on_step_start,
        on_step_complete=on_step_complete,
        work=_audit_loop,
        done_detail=lambda: (
            (
                "OK"
                if audit_holder.get("v") and audit_holder["v"].passed
                else f"score {audit_holder['v'].overall_score}"
            )
            + f" · {ledger.summary()}"
            if audit_holder.get("v")
            else ledger.summary()
        ),
    )

    async def _save() -> None:
        edited = edited_holder["out"]
        work = save_artifacts(brief, written_holder["out"], edited)
        save_chapter_artifacts(work, blueprint, drafts_holder["drafts"])
        verdict = audit_holder.get("v")
        if verdict:
            (work / "audit_report.md").write_text(
                verdict.review_markdown, encoding="utf-8"
            )
        work_holder["path"] = work

    await _run_step(
        idx_artifacts,
        total,
        labels[idx_artifacts],
        on_step_start=on_step_start,
        on_step_complete=on_step_complete,
        work=_save,
    )
    work = work_holder["path"]

    if not md_only:

        export_base = export_base_name(brief.slug, brief.format)

        async def _print() -> None:
            await asyncio.to_thread(
                build_docx,
                brief.slug,
                work,
                edited_holder["out"].manuscript_corrected,
                format=brief.format,
            )

        assert idx_print is not None
        await _run_step(
            idx_print,
            total,
            labels[idx_print],
            on_step_start=on_step_start,
            on_step_complete=on_step_complete,
            work=_print,
            done_detail=f"{work}/{export_base}.docx + .pdf",
        )

    async def _done() -> None:
        base = (
            export_base_name(brief.slug, brief.format)
            if not md_only
            else brief.slug
        )
        cleanup_work_dir(base, work)

    await _run_step(
        idx_delivery,
        total,
        labels[idx_delivery],
        on_step_start=on_step_start,
        on_step_complete=on_step_complete,
        work=_done,
        done_detail=str(work),
    )

    usage_summary = ledger.summary()
    log_pipeline_complete(str(work), usage_summary=usage_summary)
    return PipelineResult(
        brief=brief,
        written=written_holder["out"],
        edited=edited_holder["out"],
        output_dir=str(work),
        blueprint=blueprint,
        audit=audit_holder.get("v"),
        usage_summary=usage_summary,
    )
