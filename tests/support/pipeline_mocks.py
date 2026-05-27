"""Agents simulés pour tests pipeline (sans API)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from agentic_writer.agents.chapter_writer import ChapterWriterResult
from agentic_writer.editorial_models import (
    ArchitectResult,
    AuditorVerdict,
    ChapterOutline,
    StoryBlueprint,
)
from agentic_writer.models import EditorResult, TwistSheet, WriterResult
from pydantic_ai.usage import RunUsage

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


@dataclass
class MockRunResult:
    output: object
    usage: RunUsage = field(
        default_factory=lambda: RunUsage(input_tokens=100, output_tokens=50, requests=1)
    )


class MockAgent:
    def __init__(self, output: object) -> None:
        self._output = output
        self.calls: list[str] = []

    async def run(self, prompt: str) -> MockRunResult:
        self.calls.append(prompt)
        return MockRunResult(self._output)


def blueprint_from_writer_fixture(fixture_name: str = "writer_flash.json") -> StoryBlueprint:
    data = json.loads((FIXTURES / fixture_name).read_text(encoding="utf-8"))
    twist = TwistSheet.model_validate(data["twist_sheet"])
    return StoryBlueprint(
        title="Flash test",
        twist_sheet=twist,
        prologue_beat="Scène choc anonyme.",
        chapters=[
            ChapterOutline(
                index=1,
                title="Signal",
                beat="La voix sur la fréquence.",
                hook="Réplique-bombe",
                target_words=1200,
            ),
        ],
    )


def editorial_mock_agents(
    *,
    chapter_body: str | None = None,
    writer_fixture: str = "writer_flash.json",
    editor_fixture: str = "editor_flash.json",
) -> dict[str, MockAgent]:
    body = chapter_body or " ".join(["mot"] * 700)
    editor_data = json.loads((FIXTURES / editor_fixture).read_text(encoding="utf-8"))
    return {
        "architect": MockAgent(
            ArchitectResult(blueprint=blueprint_from_writer_fixture(writer_fixture))
        ),
        "chapter_writer": MockAgent(ChapterWriterResult(content=body)),
        "editor": MockAgent(EditorResult.model_validate(editor_data)),
        "auditor": MockAgent(
            AuditorVerdict(
                passed=True,
                overall_score=82,
                checklist_scores={"format_length": 2, "voix": 2},
                issues=[],
                chapters_to_rewrite=[],
                review_markdown="Audit OK.",
            )
        ),
    }


def writer_result_from_fixture(fixture_name: str = "writer_flash.json") -> WriterResult:
    data = json.loads((FIXTURES / fixture_name).read_text(encoding="utf-8"))
    return WriterResult.model_validate(data)
