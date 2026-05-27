"""Pipeline integration with mocked agents."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_writer.models import Brief, EditorResult, WriterResult
from agentic_writer.pipeline import run_pipeline
from tests.support.pipeline_mocks import editorial_mock_agents


@pytest.mark.integration
@pytest.mark.asyncio
async def test_pipeline_produces_structured_results(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "agentic_writer.io.output_dir",
        lambda slug: tmp_path / slug,
    )
    mocks = editorial_mock_agents()
    brief = Brief(slug="pipeline-integ", pitch="p", format="flash")

    result = await run_pipeline(
        brief,
        md_only=True,
        architect=mocks["architect"],
        chapter_writer=mocks["chapter_writer"],
        editor=mocks["editor"],
        auditor=mocks["auditor"],
    )

    assert isinstance(result.written, WriterResult)
    assert isinstance(result.edited, EditorResult)
    assert len(mocks["architect"].calls) == 1
    assert len(mocks["chapter_writer"].calls) >= 1
    assert len(mocks["editor"].calls) >= 1
    assert len(mocks["auditor"].calls) >= 1
    assert "prédateur" in mocks["editor"].calls[0] or "TWIST" in mocks["editor"].calls[0]


@pytest.mark.integration
@pytest.mark.asyncio
async def test_pipeline_saves_artifacts(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "agentic_writer.io.output_dir",
        lambda slug: tmp_path / slug,
    )
    mocks = editorial_mock_agents()
    brief = Brief(slug="artefacts-test", pitch="p", format="flash")

    await run_pipeline(
        brief,
        md_only=True,
        architect=mocks["architect"],
        chapter_writer=mocks["chapter_writer"],
        editor=mocks["editor"],
        auditor=mocks["auditor"],
    )
    work = tmp_path / "artefacts-test"
    assert (work / "twist_sheet.json").exists()
    assert (work / "blueprint.json").exists()
    assert (work / "chapters").is_dir()
    assert (work / "audit_report.md").exists()
    assert (work / "manuscript_final.md").exists()
