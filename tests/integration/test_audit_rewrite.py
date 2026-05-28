"""Audit loop passes agent feedback into rewrite prompts."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import pytest

from agentic_writer.agents.chapter_writer import ChapterWriterResult
from agentic_writer.editorial_models import ArchitectResult, AuditorVerdict
from agentic_writer.models import Brief, EditorResult
from agentic_writer.pipeline import run_pipeline
from tests.support.pipeline_mocks import (
    MockAgent,
    MockRunResult,
    blueprint_from_writer_fixture,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


@dataclass
class AuditThenPassAgent:
    """First audit fails and requests ch.1 rewrite; second passes."""

    calls: list[str] = field(default_factory=list)
    _round: int = 0

    async def run(self, prompt: str) -> MockRunResult:
        self.calls.append(prompt)
        self._round += 1
        if self._round == 1:
            return MockRunResult(
                AuditorVerdict(
                    passed=False,
                    overall_score=50,
                    checklist_scores={"voice": 0, "twists_intact": 2},
                    issues=["Le hook du chapitre 1 n'accroche pas."],
                    chapters_to_rewrite=[1],
                    review_markdown="Réécrire l'ouverture avec plus de menace.",
                )
            )
        return MockRunResult(
            AuditorVerdict(
                passed=True,
                overall_score=85,
                checklist_scores={"voice": 2},
                issues=[],
                chapters_to_rewrite=[],
                review_markdown="OK après réécriture.",
            )
        )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_audit_rewrite_prompts_contain_verdict(tmp_path, monkeypatch):
    monkeypatch.setenv("AGENTIC_WRITER_OUTPUT", str(tmp_path))
    monkeypatch.setenv("AGENTIC_WRITER_MAX_AUDIT_RETRIES", "2")

    body = " ".join(["mot"] * 900)
    editor_data = json.loads((FIXTURES / "editor_flash.json").read_text(encoding="utf-8"))
    editor_agent = MockAgent(EditorResult.model_validate(editor_data))
    chapter_agent = MockAgent(ChapterWriterResult(content=body))
    audit_agent = AuditThenPassAgent()

    brief = Brief(slug="rewrite-fb", pitch="Test feedback.", format="flash", lang="fr")
    await run_pipeline(
        brief,
        md_only=True,
        architect=MockAgent(
            ArchitectResult(blueprint=blueprint_from_writer_fixture())
        ),
        chapter_writer=chapter_agent,
        editor=editor_agent,
        auditor=audit_agent,  # type: ignore[arg-type]
    )

    rewrite_chapter_prompts = [
        p for p in chapter_agent.calls if "retours auditeur" in p.lower()
    ]
    assert len(rewrite_chapter_prompts) >= 1
    assert "hook du chapitre 1" in rewrite_chapter_prompts[0].lower()

    assert len(audit_agent.calls) == 2
    assert len(editor_agent.calls) >= 2
    assert "retours auditeur" in editor_agent.calls[-1].lower()
    assert "réécrire l'ouverture" in editor_agent.calls[-1].lower()
