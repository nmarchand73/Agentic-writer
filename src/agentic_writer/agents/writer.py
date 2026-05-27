"""Story writer agent."""

from __future__ import annotations

from pydantic_ai import Agent

from agentic_writer.config import load_settings
from agentic_writer.models import WriterResult
from agentic_writer.skills import writer_capability


def create_writer_agent() -> Agent[None, WriterResult]:
    settings = load_settings()
    return Agent(
        settings["openai_model"],
        instructions=(
            "Tu es l'agent d'écriture (skill story-writer). "
            "Utilise uniquement la skill story-writer. Ne fais pas de relecture finale."
        ),
        output_type=WriterResult,
        capabilities=[writer_capability()],
    )
