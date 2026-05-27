"""Remove print-pipeline temporaries from the output folder."""

from __future__ import annotations

import shutil
from pathlib import Path

from agentic_writer.log_config import get_logger

log = get_logger("cleanup")


def cleanup_work_dir(slug: str, work_dir: Path) -> list[str]:
    """Delete build leftovers; keep twist/draft/review/final md and docx/pdf.

    Removes:
    - generate.js (copy of the layout generator)
    - {slug}_unpacked/ (OOXML unpack dir if build_story aborted early)
    - {slug}_print.html
    - LibreOffice lock files (.~lock*)
    """
    work = Path(work_dir)
    if not work.is_dir():
        return []

    removed: list[str] = []
    targets: list[Path] = [
        work / "generate.js",
        work / f"{slug}_unpacked",
        work / f"{slug}_print.html",
        *work.glob(".~lock*"),
    ]

    for path in targets:
        if not path.exists():
            continue
        try:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            removed.append(path.name if path.name else str(path))
        except OSError as exc:
            log.warning("Impossible de supprimer {} : {}", path, exc)

    if removed:
        log.debug("Nettoyage {} : {}", work, ", ".join(removed))
    return removed
