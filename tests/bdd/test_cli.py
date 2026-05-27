"""BDD slice 2 — CLI."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from agentic_writer.brief_io import load_brief
from agentic_writer.models import Brief

scenarios("../../specs/bdd/02_cli_generate.feature")


@pytest.fixture
def context():
    return {"brief": None, "exit_code": 0}


@given(parsers.parse("le slug {slug}"))
def set_slug(context, slug):
    context["slug"] = slug.strip('"')


@given(parsers.parse("le pitch {pitch}"))
def set_pitch(context, pitch):
    context["pitch"] = pitch.strip('"')


@given(parsers.parse('les options generate "{opts}"'))
def set_opts(context, opts):
    context["extra_opts"] = opts.strip('"')


@when("je parse la commande generate")
def parse_generate(context, project_root):
    slug = context.get("slug")
    pitch = context.get("pitch")
    opts = context.get("extra_opts", "")
    fmt = None
    lang = None
    if "--format" in opts:
        fmt = opts.split("--format")[1].split()[0]
    if "--lang" in opts:
        lang = opts.split("--lang")[1].split()[0]
    context["brief"] = load_brief(
        slug, pitch=pitch, brief_path=None, format=fmt, lang=lang
    )


@when("je parse generate avec le fichier brief")
def parse_brief_file(context, project_root):
    path = context.get("brief_path") or (
        project_root / "examples/briefs/flash-smoke.yaml"
    )
    context["brief"] = load_brief(None, pitch=None, brief_path=path)


@given(parsers.parse('le fichier brief "{path}"'))
def brief_file(context, path, project_root):
    context["brief_path"] = project_root / path


@when(parsers.re(r"^j'invoque la commande generate (?P<args>.*)$"))
def invoke_cli(context, args):
    from typer.testing import CliRunner

    from agentic_writer.cli import app

    runner = CliRunner()
    argv = ["generate"] + args.split()
    result = runner.invoke(app, argv)
    context["exit_code"] = result.exit_code


@then(parsers.parse("le brief a le slug {slug}"))
def brief_slug(context, slug):
    assert context["brief"].slug == slug.strip('"')


@then(parsers.parse("le brief a le pitch {pitch}"))
def brief_pitch(context, pitch):
    assert context["brief"].pitch == pitch.strip('"')


@then(parsers.parse('le brief a le format "{fmt}"'))
def brief_format(context, fmt):
    assert context["brief"].format == fmt


@then(parsers.parse('le brief a la langue "{lang}"'))
def brief_lang(context, lang):
    assert context["brief"].lang == lang


@then(parsers.parse("le titre résolu est {title}"))
def brief_title(context, title):
    assert context["brief"].resolved_title() == title.strip('"')


@then(parsers.parse("le brief a le theme {theme}"))
def brief_theme(context, theme):
    assert context["brief"].theme == theme.strip('"')


@then("le code de sortie CLI est 2")
def exit_two(context):
    assert context["exit_code"] == 2


@when("je résous le dossier de sortie")
def resolve_output(context, tmp_path, monkeypatch):
    out_root = tmp_path / "output"

    def _output_dir(slug: str):
        path = out_root / slug
        path.mkdir(parents=True, exist_ok=True)
        return path

    monkeypatch.setattr("agentic_writer.config.output_dir", _output_dir)
    context["out"] = str(_output_dir("ma-nouvelle"))


@then(parsers.parse('le dossier se termine par "{suffix}"'))
def output_suffix(context, suffix):
    assert context["out"].endswith(suffix.replace("/", str(Path("/"))))


@given("des agents simulés")
def mock_agents(context):
    context["mock_pipeline"] = True


@given(parsers.parse('une commande "{cmd}"'))
def set_cmd(context, cmd):
    context["cli_cmd"] = cmd


@given("build_docx simulé")
def mock_docx(context):
    context["mock_docx"] = True


@when("j'exécute generate via la CLI")
def run_generate_mocked(context):
    from typer.testing import CliRunner

    from agentic_writer.cli import app

    runner = CliRunner()
    parts = context["cli_cmd"].split()
    args = ["generate"] + parts[1:]
    md_only = "--md-only" in args
    context["md_only_called"] = md_only

    with patch("agentic_writer.cli.run_pipeline", new_callable=AsyncMock) as mock:
        mock.return_value = type("R", (), {"output_dir": "/tmp/x"})()
        result = runner.invoke(app, args)
        context["exit_code"] = result.exit_code
        context["pipeline_called"] = mock.called
        context["pipeline_md_only"] = mock.call_args.kwargs.get("md_only")


@then("le pipeline a été appelé sans export imprimable")
def pipeline_md_only(context):
    assert context["pipeline_called"]
    assert context["pipeline_md_only"] is True


@then("le pipeline a été appelé avec export imprimable")
def pipeline_with_docx(context):
    assert context["pipeline_called"]
    assert context["pipeline_md_only"] is False
