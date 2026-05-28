"""BDD slice 2 — pipeline."""

import json
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from agentic_writer.models import Brief, EditorResult, WriterResult
from agentic_writer.pipeline import run_pipeline
from tests.support.pipeline_mocks import (
    MockAgent,
    blueprint_from_writer_fixture,
    editorial_mock_agents,
    writer_result_from_fixture,
)
from agentic_writer.editorial_models import ArchitectResult
from agentic_writer.agents.chapter_writer import ChapterWriterResult

scenarios("../../specs/bdd/03_pipeline_text.feature")

FIXTURES = Path(__file__).parent.parent / "fixtures"


@pytest.fixture
def context():
    return {}


@given(parsers.parse("un Architecte simulé retournant {fixture}"))
def mock_architect(context, fixture):
    context["architect"] = MockAgent(
        ArchitectResult(blueprint=blueprint_from_writer_fixture(fixture))
    )


@given("un Writer chapitre simulé avec un corps long")
def mock_chapter_writer(context):
    context["chapter_writer"] = MockAgent(
        ChapterWriterResult(content=" ".join(["mot"] * 900))
    )


@given(parsers.parse("un Editor simulé retournant {fixture}"))
def mock_editor(context, fixture):
    data = json.loads((FIXTURES / fixture).read_text())
    context["editor"] = MockAgent(EditorResult.model_validate(data))


@given("un Editor simulé capturant le prompt")
def mock_editor_capture(context):
    data = json.loads((FIXTURES / "editor_flash.json").read_text())
    context["editor"] = MockAgent(EditorResult.model_validate(data))


@given(parsers.parse('un brief format "{fmt}" slug "{slug}"'))
def set_brief(context, fmt, slug):
    context["brief"] = Brief(slug=slug, pitch="p", format=fmt)


@given("des agents simulés")
def both_mocks(context):
    mocks = editorial_mock_agents()
    context.update(mocks)


@given("un Auditeur simulé avec succès")
def mock_auditor_ok(context):
    context["auditor"] = editorial_mock_agents()["auditor"]


@given(parsers.parse('le slug "{slug}"'))
def slug_only(context, slug):
    context["brief"] = Brief(slug=slug, pitch="p", format="flash")


@when("j'exécute le pipeline sans export imprimable")
def run_pipe(context, tmp_path, monkeypatch):
    import asyncio

    monkeypatch.setattr(
        "agentic_writer.io.output_dir",
        lambda slug: tmp_path / slug,
    )

    async def _run():
        return await run_pipeline(
            context["brief"],
            md_only=True,
            architect=context.get("architect"),
            chapter_writer=context.get("chapter_writer"),
            editor=context.get("editor"),
            auditor=context.get("auditor"),
        )

    context["result"] = asyncio.run(_run())
    context["work"] = tmp_path / context["brief"].slug


@then("le résultat contient un WriterResult valide")
def assert_writer(context):
    assert isinstance(context["result"].written, WriterResult)


@then("le résultat contient un EditorResult valide")
def assert_editor(context):
    assert isinstance(context["result"].edited, EditorResult)


@then("l'Editor est appelé après l'Architecte et les chapitres")
def assert_order(context):
    assert len(context["architect"].calls) == 1
    assert len(context["chapter_writer"].calls) >= 1
    assert len(context["editor"].calls) >= 1


@then("le prompt de relecture contient le twist_final du fixture")
def assert_twist_in_prompt(context):
    data = json.loads((FIXTURES / "writer_flash.json").read_text())
    twist = data["twist_sheet"]["twist_final"]
    assert twist in context["editor"].calls[0]


@then(parsers.parse('le fichier "{name}" existe dans le dossier de sortie'))
def file_exists(context, name):
    assert (context["work"] / name).exists()


@then("twist_sheet.json contient le twist_final du fixture")
def twist_sheet_has_twist(context):
    data = json.loads((context["work"] / "twist_sheet.json").read_text(encoding="utf-8"))
    expected = writer_result_from_fixture().twist_sheet
    assert data["twist_final"] == expected.twist_final
