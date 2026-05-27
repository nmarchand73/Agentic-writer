"""Adversarial auditor agent — post-editor gate (v2)."""

from __future__ import annotations

from pydantic_ai import Agent

from agentic_writer.agent_instructions import AUDITOR_INSTRUCTIONS
from agentic_writer.config import load_settings
from agentic_writer.editorial_models import AuditorVerdict
from agentic_writer.skills import auditor_capability


def create_auditor_agent() -> Agent[None, AuditorVerdict]:
    settings = load_settings()
    return Agent(
        settings["model_auditor"],
        instructions=AUDITOR_INSTRUCTIONS,
        output_type=AuditorVerdict,
        capabilities=[auditor_capability()],
    )
