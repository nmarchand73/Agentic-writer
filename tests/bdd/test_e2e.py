"""BDD slice 5 — génération réelle (nightly, OPENAI_API_KEY).

Toujours format **flash** : 1 chapitre planifié, coût API maîtrisé (pipeline Architecte → chapitres → Auditeur).
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

from agentic_writer.editorial_plan import chapter_plan_for

scenarios("../../specs/bdd/05_e2e_live.feature")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_SLUG = "e2e-flash"
E2E_FORMAT = "flash"
E2E_PITCH = (
    "Formation lumineuse non cataloguée ; voix de secours avec le prénom de sa mère morte."
)


@pytest.fixture
def context():
    return {}


@given("OPENAI_API_KEY est défini")
def require_api_key():
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY requis pour les scénarios @e2e")
    if os.getenv("AGENTIC_WRITER_RUN_E2E") not in {"1", "true", "TRUE", "yes", "YES"}:
        pytest.skip("E2E live désactivé (set AGENTIC_WRITER_RUN_E2E=1 pour l'activer)")


@given("Node est disponible pour l'export docx")
def require_node():
    if not shutil.which("node"):
        pytest.skip("Node.js requis pour l'export docx")


@when("j'exécute la CLI generate e2e-flash avec pitch court et format flash")
def run_generate_e2e(context, tmp_path, monkeypatch):
    out_root = tmp_path / "output"
    monkeypatch.setenv("AGENTIC_WRITER_OUTPUT", str(out_root))
    result = subprocess.run(
        [
            "uv",
            "run",
            "agentic-writer",
            "generate",
            OUTPUT_SLUG,
            "--pitch",
            E2E_PITCH,
            "--format",
            E2E_FORMAT,
            "--md-only",
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=600,
    )
    context["exit_code"] = result.returncode
    context["stderr"] = result.stderr
    context["work"] = out_root / OUTPUT_SLUG


@then("la génération se termine avec succès")
def generation_ok(context):
    assert context["exit_code"] == 0, context.get("stderr", "")


@then("le manuscrit final existe et fait plus de 500 octets")
def manuscript_size(context):
    path = context["work"] / "manuscript_final.md"
    assert path.is_file(), f"manquant: {path}"
    assert path.stat().st_size > 500


@then("le plan chapitres correspond au format flash")
def blueprint_matches_flash(context):
    path = context["work"] / "blueprint.json"
    assert path.is_file(), f"manquant: {path}"
    data = json.loads(path.read_text(encoding="utf-8"))
    expected = chapter_plan_for(E2E_FORMAT).chapter_count
    assert len(data["chapters"]) == expected
