"""Adversarial auditor agent — post-editor gate (v2)."""

from __future__ import annotations

from pydantic_ai import Agent

from agentic_writer.config import load_settings
from agentic_writer.editorial_models import AuditorVerdict
from agentic_writer.skills import auditor_capability


def create_auditor_agent() -> Agent[None, AuditorVerdict]:
    settings = load_settings()
    return Agent(
        settings["model_auditor"],
        instructions=(
            "Tu es l'auditeur adversarial (skill story-auditor). "
            "Évalue le manuscrit corrigé ; twists figés. "
            "Indique chapters_to_rewrite seulement si 1–2 chapitres sont faibles."
        ),
        output_type=AuditorVerdict,
        capabilities=[auditor_capability()],
    )
