"""Manuscript editor agent."""

from __future__ import annotations

from pydantic_ai import Agent

from agentic_writer.config import load_settings
from agentic_writer.models import EditorResult
from agentic_writer.skills import editor_capability


def create_editor_agent() -> Agent[None, EditorResult]:
    settings = load_settings()
    return Agent(
        settings["openai_model"],
        instructions=(
            "Tu es l'agent de relecture (skill manuscript-editor). "
            "Utilise manuscript-editor et lis les guides story-writer via read_skill_resource si besoin. "
            "Corrige style et continuité sans changer les twists."
        ),
        output_type=EditorResult,
        capabilities=[editor_capability()],
    )
