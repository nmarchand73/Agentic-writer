"""Story architect agent — blueprint before prose (v2)."""

from __future__ import annotations

from pydantic_ai import Agent

from agentic_writer.agent_instructions import ARCHITECT_INSTRUCTIONS
from agentic_writer.config import load_settings
from agentic_writer.editorial_models import ArchitectResult


def create_architect_agent() -> Agent[None, ArchitectResult]:
    settings = load_settings()
    return Agent(
        settings["model_architect"],
        instructions=ARCHITECT_INSTRUCTIONS,
        output_type=ArchitectResult,
    )
