"""Print layout agent — skill print-layout only (no plot edits)."""

from __future__ import annotations

from pathlib import Path

from pydantic_ai import Agent, RunContext
from pydantic_ai_skills import SkillsCapability

from agentic_writer.agent_instructions import FORMATTER_INSTRUCTIONS
from agentic_writer.config import PRINT_LAYOUT_SKILL_DIR, load_settings
from agentic_writer.docx_build import build_docx
from agentic_writer.export_names import export_base_name
from agentic_writer.models import StoryFormat
from agentic_writer.pipeline import PipelineError


class FormatterDeps:
    """Runtime paths for a print pass."""

    slug: str
    work_dir: Path
    manuscript_md: str
    format: StoryFormat = "nouvelle"


def create_formatter_agent() -> Agent[FormatterDeps, str]:
    settings = load_settings()
    agent: Agent[FormatterDeps, str] = Agent(
        settings["openai_model"],
        instructions=FORMATTER_INSTRUCTIONS,
        deps_type=FormatterDeps,
        capabilities=[SkillsCapability(directories=[str(PRINT_LAYOUT_SKILL_DIR)])],
    )

    @agent.tool
    async def format_for_print(ctx: RunContext[FormatterDeps]) -> str:
        """Génère docx + pdf via build_story.sh (mise en page A5 Palatino)."""
        base = export_base_name(ctx.deps.slug, ctx.deps.format)
        try:
            build_docx(
                ctx.deps.slug,
                ctx.deps.work_dir,
                ctx.deps.manuscript_md,
                format=ctx.deps.format,
            )
        except PipelineError as exc:
            return f"Échec export : {exc}"
        return f"Export OK → {ctx.deps.work_dir}/{base}.docx et {base}.pdf"

    return agent
