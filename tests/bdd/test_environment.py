"""BDD slice 1 — environment."""

from __future__ import annotations

from pathlib import Path

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from agentic_writer.config import PROJECT_ROOT, WRITER_SKILL_DIR
from agentic_writer.doctor import doctor_exit_code, run_doctor
from agentic_writer.skills import list_editor_skill_names, list_writer_skill_names

scenarios("../../specs/bdd/01_environment.feature")


@pytest.fixture
def context():
    return {}


@when("j'exécute la commande doctor")
def run_doctor_cmd(context):
    report = run_doctor(require_writer_skill=context.get("require_writer_skill", True))
    context["exit_code"] = doctor_exit_code(report)
    context["output"] = "\n".join(report.messages)


@given("le fichier skills/story-writer/SKILL.md est absent")
def hide_writer_skill(monkeypatch):
    missing = PROJECT_ROOT / "skills" / "__missing_story_writer__"
    monkeypatch.setattr("agentic_writer.doctor.WRITER_SKILL_DIR", missing)


@then("le code de sortie est 0")
def exit_zero(context):
    assert context["exit_code"] == 0


@then("le code de sortie est différent de 0")
def exit_nonzero(context):
    assert context["exit_code"] != 0


@then(parsers.parse('la sortie mentionne "{text}"'))
def output_mentions(context, text):
    assert text in context.get("output", "")


@when("je liste les skills exposées à l'agent d'écriture")
def list_writer(context):
    context["skills"] = list_writer_skill_names()


@when("je liste les skills exposées à l'agent de relecture")
def list_editor(context):
    context["skills"] = list_editor_skill_names()


@then(parsers.parse('la liste contient "{name}"'))
def list_contains(context, name):
    assert name in context["skills"]


@then(parsers.parse('la liste ne contient pas "{name}"'))
def list_not_contains(context, name):
    assert name not in context["skills"]
