"""BDD slice 2 — pipeline."""

import json
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from agentic_writer.models import Brief, EditorResult, WriterResult
from agentic_writer.pipeline import run_pipeline

scenarios("../../specs/bdd/03_pipeline_text.feature")

FIXTURES = Path(__file__).parent.parent / "fixtures"


class MockAgent:
    def __init__(self, output, capture=False):
        self._output = output
        self.calls = []
        self.capture = capture

    async def run(self, prompt: str):
        self.calls.append(prompt)
        return type("R", (), {"output": self._output})()


@pytest.fixture
def context():
    return {}


@given(parsers.parse("un Writer simulé retournant {fixture}"))
def mock_writer(context, fixture):
    data = json.loads((FIXTURES / fixture).read_text())
    context["writer"] = MockAgent(WriterResult.model_validate(data))


@given(parsers.parse("un Editor simulé retournant {fixture}"))
def mock_editor(context, fixture):
    data = json.loads((FIXTURES / fixture).read_text())
    context["editor"] = MockAgent(EditorResult.model_validate(data))


@given("un Editor simulé capturant le prompt")
def mock_editor_capture(context):
    data = json.loads((FIXTURES / "editor_flash.json").read_text())
    context["editor"] = MockAgent(EditorResult.model_validate(data), capture=True)


@given(parsers.parse('un brief format "{fmt}" slug "{slug}"'))
def set_brief(context, fmt, slug):
    context["brief"] = Brief(slug=slug, pitch="p", format=fmt)


@given("des agents simulés")
def both_mocks(context):
    w = json.loads((FIXTURES / "writer_flash.json").read_text())
    e = json.loads((FIXTURES / "editor_flash.json").read_text())
    context["writer"] = MockAgent(WriterResult.model_validate(w))
    context["editor"] = MockAgent(EditorResult.model_validate(e))


@given(parsers.parse('le slug "{slug}"'))
def slug_only(context, slug):
    context["brief"] = Brief(slug=slug, pitch="p")


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
            writer=context.get("writer"),
            editor=context.get("editor"),
        )

    context["result"] = asyncio.run(_run())
    context["work"] = tmp_path / context["brief"].slug


@then("le résultat contient un WriterResult valide")
def assert_writer(context):
    assert isinstance(context["result"].written, WriterResult)


@then("le résultat contient un EditorResult valide")
def assert_editor(context):
    assert isinstance(context["result"].edited, EditorResult)


@then("l'Editor est appelé une fois après le Writer")
def assert_order(context):
    assert len(context["writer"].calls) == 1
    assert len(context["editor"].calls) == 1


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
    expected = json.loads((FIXTURES / "writer_flash.json").read_text(encoding="utf-8"))
    assert data["twist_final"] == expected["twist_sheet"]["twist_final"]
