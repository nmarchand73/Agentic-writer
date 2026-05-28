"""Manuscript editor agent."""

from __future__ import annotations

from pydantic_ai import Agent

from agentic_writer.agent_instructions import EDITOR_INSTRUCTIONS
from agentic_writer.config import load_settings
from agentic_writer.models import EditorResult


def create_editor_agent() -> Agent[None, EditorResult]:
    settings = load_settings()
    return Agent(
        settings["model_editor"],
        instructions=EDITOR_INSTRUCTIONS,
        output_type=EditorResult,
    )
