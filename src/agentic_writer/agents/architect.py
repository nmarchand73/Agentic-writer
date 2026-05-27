"""Story architect agent — blueprint before prose (v2)."""

from __future__ import annotations

from pydantic_ai import Agent

from agentic_writer.config import load_settings
from agentic_writer.editorial_models import ArchitectResult
from agentic_writer.skills import architect_capability


def create_architect_agent() -> Agent[None, ArchitectResult]:
    settings = load_settings()
    return Agent(
        settings["model_architect"],
        instructions=(
            "Tu es l'architecte narratif (skill story-architect). "
            "Conçois twist_sheet + plan de chapitres AVANT toute prose. "
            "Charge story-architect et lis story-writer si besoin."
        ),
        output_type=ArchitectResult,
        capabilities=[architect_capability()],
    )
