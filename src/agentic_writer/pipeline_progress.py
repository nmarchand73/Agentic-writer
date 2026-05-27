"""Logs de progression pipeline (loguru)."""

from __future__ import annotations

from agentic_writer.log_config import get_logger

log = get_logger("pipeline")


def log_pipeline_plan(slug: str, labels: list[str], *, md_only: bool) -> None:
    total = len(labels)
    log.info(
        "Pipeline récit — slug={} md_only={} ({} étapes)",
        slug,
        md_only,
        total,
    )
    for i, label in enumerate(labels, start=1):
        log.info("  {:>2}. {}", i, label)


def log_step_start(index: int, total: int, label: str) -> None:
    log.info("[{}/{}] ▶  {}", index + 1, total, label)


def log_step_done(index: int, total: int, label: str, *, detail: str | None = None) -> None:
    msg = f"[{index + 1}/{total}] ✓  {label}"
    if detail:
        msg = f"{msg} — {detail}"
    log.success(msg)


def log_step_skipped(index: int, total: int, label: str, reason: str) -> None:
    log.warning("[{}/{}] ⊘  {} ({})", index + 1, total, label, reason)


def log_pipeline_complete(output_dir: str) -> None:
    log.info("── Pipeline terminé ──")
    log.success("Sortie → {}", output_dir)
