"""Export manuscript to docx/pdf via build_story.sh."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from agentic_writer.cleanup import cleanup_work_dir
from agentic_writer.export_names import export_base_name
from agentic_writer.config import (
    BUILD_STORY_SCRIPT,
    GENERATE_FROM_MD_SCRIPT,
    OFFICE_SCRIPTS_DIR,
    PROJECT_ROOT,
)
from agentic_writer.log_config import get_logger
from agentic_writer.models import StoryFormat
from agentic_writer.pipeline import PipelineError

log = get_logger("docx")


def build_docx(
    slug: str,
    work_dir: Path,
    manuscript_md: str,
    *,
    format: StoryFormat = "nouvelle",
) -> str:
    """Write manuscript_final.md, copy print-layout generator, invoke build_story.sh.

    Returns the export base name used for .docx / .pdf (``{slug}-{format}``).
    """
    base_name = export_base_name(slug, format)
    work_dir.mkdir(parents=True, exist_ok=True)
    md_path = work_dir / "manuscript_final.md"
    md_path.write_text(manuscript_md, encoding="utf-8")

    if not GENERATE_FROM_MD_SCRIPT.exists():
        raise PipelineError(f"Missing print layout generator: {GENERATE_FROM_MD_SCRIPT}")

    generate_js = work_dir / "generate.js"
    shutil.copy(GENERATE_FROM_MD_SCRIPT, generate_js)

    if not BUILD_STORY_SCRIPT.exists():
        raise PipelineError(f"Missing build_story.sh: {BUILD_STORY_SCRIPT}")

    env = os.environ.copy()
    env["STORY_WORK_DIR"] = str(work_dir.resolve())
    if OFFICE_SCRIPTS_DIR.exists():
        env["DOCX_OFFICE_SCRIPTS"] = str(OFFICE_SCRIPTS_DIR.resolve())

    docx_modules = PROJECT_ROOT / "node_modules"
    if not (docx_modules / "docx").exists():
        raise PipelineError(
            "npm package 'docx' missing — run: cd Agentic-writer && npm install"
        )
    log.debug("NODE_PATH={}", docx_modules)
    node_path = str(docx_modules.resolve())
    env["NODE_PATH"] = (
        f"{node_path}{os.pathsep}{env['NODE_PATH']}"
        if env.get("NODE_PATH")
        else node_path
    )

    log.info("build_story.sh {} → {}", base_name, work_dir.resolve())
    result = subprocess.run(
        ["bash", str(BUILD_STORY_SCRIPT), base_name, str(generate_js)],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.stdout:
        for line in result.stdout.strip().splitlines():
            log.debug("build_story | {}", line)
    if result.returncode != 0:
        if result.stderr:
            for line in result.stderr.strip().splitlines():
                log.error("build_story | {}", line)
        raise PipelineError(
            f"build_story.sh failed ({result.returncode}): {result.stderr or result.stdout}"
        )
    log.debug("build_story.sh exit 0")
    cleanup_work_dir(base_name, work_dir)
    return base_name
