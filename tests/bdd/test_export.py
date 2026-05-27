"""BDD slice 3 — export."""

from unittest.mock import MagicMock, patch

import pytest
from pytest_bdd import given, scenarios, then, when

from agentic_writer.docx_build import build_docx
from agentic_writer.pipeline import PipelineError

scenarios("../../specs/bdd/04_export_imprimable.feature")


@pytest.fixture
def context():
    return {}


@given("manuscript_final.md dans le dossier de travail")
def manuscript(context, tmp_path):
    context["work"] = tmp_path / "work"
    context["work"].mkdir()
    (context["work"] / "manuscript_final.md").write_text("# T\n\nBody", encoding="utf-8")


@given("build_story.sh simulé avec succès")
def mock_ok(context):
    context["returncode"] = 0


@given("build_story.sh simulé en échec")
def mock_fail(context):
    context["returncode"] = 1


@when('j\'exécute build_docx pour le slug "export-integ"')
def run_build_export_integ(context):
    _run_build_docx(context, "export-integ")


@when("j'exécute build_docx")
def run_build_default(context):
    _run_build_docx(context, "export-integ")


def _run_build_docx(context, slug: str):
    with patch("agentic_writer.docx_build.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            returncode=context.get("returncode", 0),
            stdout="",
            stderr="",
        )
        try:
            build_docx(slug, context["work"], "body")
            context["error"] = None
            context["mock_run"] = mock_run
        except PipelineError as e:
            context["error"] = e
            context["mock_run"] = mock_run


@then("les fichiers temporaires d'export sont absents du dossier de travail")
def no_temp_export_files(context):
    work = context["work"]
    assert not (work / "generate.js").exists()
    assert not (work / "export-integ_unpacked").exists()
    assert not (work / "export-integ_print.html").exists()


@then('build_story.sh a été invoqué avec le slug "export-integ"')
def slug_in_call(context):
    args = context["mock_run"].call_args[0][0]
    assert "export-integ" in args


@then("une erreur pipeline est levée")
def error_raised(context):
    assert context["error"] is not None
