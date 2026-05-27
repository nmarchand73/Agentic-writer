"""Noms de fichiers docx/pdf — incluent le format récit pour éviter les collisions."""

from __future__ import annotations

from pathlib import Path

from agentic_writer.models import StoryFormat


def export_base_name(slug: str, format: StoryFormat) -> str:
    """Base name for print exports, e.g. signal-77-flash."""
    return f"{slug}-{format}"


def export_docx_path(work_dir: Path, slug: str, format: StoryFormat) -> Path:
    return work_dir / f"{export_base_name(slug, format)}.docx"


def export_pdf_path(work_dir: Path, slug: str, format: StoryFormat) -> Path:
    return work_dir / f"{export_base_name(slug, format)}.pdf"


def resolve_export_pdf_path(
    work_dir: Path,
    slug: str,
    format: StoryFormat | None = None,
) -> Path | None:
    """Find PDF on disk: prefer {slug}-{format}.pdf, then legacy {slug}.pdf."""
    if format is not None:
        path = export_pdf_path(work_dir, slug, format)
        if path.is_file():
            return path
    legacy = work_dir / f"{slug}.pdf"
    if legacy.is_file():
        return legacy
    if format is None:
        matches = sorted(work_dir.glob(f"{slug}-*.pdf"))
        if matches:
            return matches[0]
    return None
