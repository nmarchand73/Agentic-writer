"""Writer → Editor pipeline orchestration."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING

from agentic_writer.cleanup import cleanup_work_dir
from agentic_writer.io import build_edit_prompt, build_writer_prompt, save_artifacts
from agentic_writer.log_config import get_logger
from agentic_writer.models import Brief, PipelineResult
from agentic_writer.pipeline_progress import (
    log_pipeline_complete,
    log_pipeline_plan,
    log_step_done,
    log_step_start,
)
from agentic_writer.pipeline_steps import pipeline_step_labels

if TYPE_CHECKING:
    from pydantic_ai import Agent

    from agentic_writer.models import EditorResult, WriterResult

log = get_logger("pipeline")

StepHook = Callable[[int, str], Awaitable[None] | None]

# Indices alignés sur default_pipeline_steps / UI Studio
IDX_BRIEF = 0
IDX_WRITER = 1
IDX_EDITOR = 2
IDX_ARTIFACTS = 3
IDX_PRINT = 4  # présent seulement si include_export


class PipelineError(Exception):
    """Pipeline step failed."""


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
    done_detail: str | None = None,
) -> None:
    log_step_start(index, total, label)
    await _maybe_await(on_step_start(index, "running") if on_step_start else None)
    await _maybe_await(work())
    log_step_done(index, total, label, detail=done_detail)
    await _maybe_await(on_step_complete(index, "completed") if on_step_complete else None)


async def run_pipeline(
    brief: Brief,
    *,
    md_only: bool = False,
    writer: Agent[None, WriterResult] | None = None,
    editor: Agent[None, EditorResult] | None = None,
    on_step_start: StepHook | None = None,
    on_step_complete: StepHook | None = None,
) -> PipelineResult:
    from agentic_writer.agents import create_editor_agent, create_writer_agent
    from agentic_writer.docx_build import build_docx

    labels = pipeline_step_labels(include_export=not md_only)
    total = len(labels)
    idx_artifacts = total - 1

    log_pipeline_plan(brief.slug, labels, md_only=md_only)

    writer_agent = writer or create_writer_agent()
    editor_agent = editor or create_editor_agent()

    written_holder: dict[str, WriterResult] = {}
    edited_holder: dict[str, EditorResult] = {}
    work_holder: dict[str, object] = {}

    # ── 0. Brief ──
    async def _brief() -> None:
        log.debug(
            "brief slug={} format={} lang={} pitch={!r:.80}",
            brief.slug,
            brief.format,
            brief.lang,
            brief.pitch,
        )

    await _run_step(
        IDX_BRIEF,
        total,
        labels[IDX_BRIEF],
        on_step_start=on_step_start,
        on_step_complete=on_step_complete,
        work=_brief,
        done_detail=f"{brief.format} / {brief.lang}",
    )

    # ── 1. Writer ──
    async def _writer() -> None:
        written_holder["out"] = (await writer_agent.run(build_writer_prompt(brief))).output

    await _run_step(
        IDX_WRITER,
        total,
        labels[IDX_WRITER],
        on_step_start=on_step_start,
        on_step_complete=on_step_complete,
        work=_writer,
    )
    written = written_holder["out"]
    twist_preview = (written.twist_sheet.twist_final or "")[:60]
    log.info(
        "  └─ brouillon : {} car., twist={!r}",
        len(written.manuscript),
        twist_preview,
    )

    # ── 2. Editor ──
    async def _editor() -> None:
        edited_holder["out"] = (
            await editor_agent.run(build_edit_prompt(written))
        ).output

    await _run_step(
        IDX_EDITOR,
        total,
        labels[IDX_EDITOR],
        on_step_start=on_step_start,
        on_step_complete=on_step_complete,
        work=_editor,
    )
    edited = edited_holder["out"]
    log.info("  └─ corrigé : {} car.", len(edited.manuscript_corrected))

    # ── 3. Artefacts markdown ──
    async def _save_md() -> None:
        work_holder["path"] = save_artifacts(brief, written, edited)

    await _run_step(
        IDX_ARTIFACTS,
        total,
        labels[IDX_ARTIFACTS],
        on_step_start=on_step_start,
        on_step_complete=on_step_complete,
        work=_save_md,
    )
    work = work_holder["path"]  # type: ignore[assignment]
    log.info("  └─ markdown : {}", work)

    # ── 4. Print layout (optionnel) — skill print-layout / twilight-zone pipeline ──
    if not md_only:

        async def _print_layout() -> None:
            build_docx(brief.slug, work, edited.manuscript_corrected)

        await _run_step(
            IDX_PRINT,
            total,
            labels[IDX_PRINT],
            on_step_start=on_step_start,
            on_step_complete=on_step_complete,
            work=_print_layout,
            done_detail=f"{work}/{brief.slug}.docx + .pdf",
        )
    else:
        log.info("  └─ export docx/pdf ignoré (--md-only)")

    # ── Livraison ──
    async def _done() -> None:
        removed = cleanup_work_dir(brief.slug, work)
        log.debug(
            "fichiers livrés : twist_sheet.json, draft_manuscript.md, review.md, "
            "manuscript_final.md"
            + (f", {brief.slug}.docx, {brief.slug}.pdf" if not md_only else "")
            + (f" | temp supprimés : {', '.join(removed)}" if removed else "")
        )

    await _run_step(
        idx_artifacts,
        total,
        labels[idx_artifacts],
        on_step_start=on_step_start,
        on_step_complete=on_step_complete,
        work=_done,
        done_detail=str(work),
    )

    log_pipeline_complete(str(work))
    return PipelineResult(
        brief=brief,
        written=written,
        edited=edited,
        output_dir=str(work),
    )
