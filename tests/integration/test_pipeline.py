"""Pipeline integration with mocked agents."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pytest

from agentic_writer.models import Brief, EditorResult, WriterResult
from agentic_writer.pipeline import run_pipeline

FIXTURES = Path(__file__).parent.parent / "fixtures"


@dataclass
class MockRunResult:
    output: WriterResult | EditorResult


class MockAgent:
    def __init__(self, output: WriterResult | EditorResult) -> None:
        self._output = output
        self.calls: list[str] = []

    async def run(self, prompt: str) -> MockRunResult:
        self.calls.append(prompt)
        return MockRunResult(self._output)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_pipeline_writer_then_editor(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "agentic_writer.io.output_dir",
        lambda slug: tmp_path / slug,
    )
    writer_data = json.loads((FIXTURES / "writer_flash.json").read_text())
    editor_data = json.loads((FIXTURES / "editor_flash.json").read_text())
    writer = MockAgent(WriterResult.model_validate(writer_data))
    editor = MockAgent(EditorResult.model_validate(editor_data))
    brief = Brief(slug="pipeline-integ", pitch="p", format="flash")

    result = await run_pipeline(brief, md_only=True, writer=writer, editor=editor)

    assert isinstance(result.written, WriterResult)
    assert isinstance(result.edited, EditorResult)
    assert len(writer.calls) == 1
    assert len(editor.calls) == 1
    assert editor.calls[0].count("TWIST") or "prédateur" in editor.calls[0]


@pytest.mark.integration
@pytest.mark.asyncio
async def test_pipeline_saves_artifacts(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "agentic_writer.io.output_dir",
        lambda slug: tmp_path / slug,
    )
    writer_data = json.loads((FIXTURES / "writer_flash.json").read_text())
    editor_data = json.loads((FIXTURES / "editor_flash.json").read_text())
    writer = MockAgent(WriterResult.model_validate(writer_data))
    editor = MockAgent(EditorResult.model_validate(editor_data))
    brief = Brief(slug="artefacts-test", pitch="p")

    await run_pipeline(brief, md_only=True, writer=writer, editor=editor)
    work = tmp_path / "artefacts-test"
    assert (work / "twist_sheet.json").exists()
    assert (work / "manuscript_final.md").exists()
