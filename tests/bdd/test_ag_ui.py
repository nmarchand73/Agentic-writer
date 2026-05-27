"""BDD slice 5–6 — API Studio AG-UI."""

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from agentic_writer.api.app import create_app
from agentic_writer.api.studio_state import StudioState, default_pipeline_steps

scenarios("../../specs/bdd/06_ag_ui_studio.feature")


@pytest.fixture
def context():
    return {}


@given("le serveur FastAPI studio démarré en mode test")
def app_ready(context, tmp_path, monkeypatch):
    monkeypatch.setattr(
        "agentic_writer.api.app.output_dir",
        lambda slug: tmp_path / slug,
    )
    context["app"] = create_app()
    context["tmp"] = tmp_path


@when(parsers.parse('je GET sur "{path}"'))
def get_path(context, path):
    from starlette.testclient import TestClient

    client = TestClient(context["app"])
    context["response"] = client.get(path)


@then("le code de statut HTTP est 200")
def http_200(context):
    assert context["response"].status_code == 200


@then("le code de statut HTTP est 404")
def http_404(context):
    assert context["response"].status_code == 404


@then(parsers.parse('la réponse JSON contient status "{value}"'))
def json_status(context, value):
    assert context["response"].json()["status"] == value


@given(parsers.parse('un manuscrit final pour le slug "{slug}"'))
def manuscript_on_disk(context, slug):
    work = context["tmp"] / slug
    work.mkdir(parents=True, exist_ok=True)
    (work / "manuscript_final.md").write_text("# Titre\n\nCorps.", encoding="utf-8")


@given(parsers.parse('un pdf pour le slug "{slug}"'))
def pdf_on_disk(context, slug):
    work = context["tmp"] / slug
    work.mkdir(parents=True, exist_ok=True)
    (work / f"{slug}.pdf").write_bytes(b"%PDF-1.4 test")


@then(parsers.parse('le corps contient "{text}"'))
def body_contains(context, text):
    assert text in context["response"].text


@then("le type de contenu est application/pdf")
def pdf_content_type(context):
    assert context["response"].headers["content-type"].startswith("application/pdf")


@given(
    parsers.parse('un état studio initial pour slug "{slug}" et pitch "{pitch}"')
)
def studio_state(context, slug, pitch):
    context["state"] = StudioState(slug=slug, pitch=pitch)


@when("je construis les étapes pipeline avec export imprimable")
def build_steps(context):
    context["state"] = context["state"].model_copy(
        update={"steps": default_pipeline_steps(include_export=True)}
    )


@then(parsers.parse('l\'état studio contient le slug "{slug}"'))
def state_slug(context, slug):
    assert context["state"].slug == slug


@then(parsers.parse('l\'état studio contient le pitch "{pitch}"'))
def state_pitch(context, pitch):
    assert context["state"].pitch == pitch


@then(parsers.parse('les étapes pipeline contiennent "{label}"'))
def steps_contain(context, label):
    descriptions = [s.description for s in context["state"].steps]
    assert any(label in d for d in descriptions)
