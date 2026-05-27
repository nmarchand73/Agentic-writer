"""io helpers."""

import json
from pathlib import Path

from agentic_writer.io import build_edit_prompt, save_artifacts
from agentic_writer.models import Brief, EditorResult, WriterResult, TwistSheet


def _writer() -> WriterResult:
    sheet = TwistSheet(
        twist_final="TWIST_FINAL_X",
        mid_twist="m",
        coda_bombe="c",
        mensonge_omission="l",
        scenes_recontextualisees=["a", "b", "c"],
        indices_foreshadowing=["i", "j"],
        pitch_booktok="pitch ok here",
    )
    return WriterResult(twist_sheet=sheet, manuscript="# Draft\n\nBody.")


def test_build_edit_prompt_includes_twist(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "agentic_writer.io.output_dir",
        lambda slug: tmp_path / slug,
    )
    brief = Brief(slug="art", pitch="p", format="flash", lang="fr")
    written = _writer()
    prompt = build_edit_prompt(written, brief)
    assert "TWIST_FINAL_X" in prompt
    assert "flash" in prompt
    assert "Skill injectée" in prompt
    assert "# Draft" in prompt


def test_save_artifacts(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "agentic_writer.io.output_dir",
        lambda slug: tmp_path / slug,
    )
    brief = Brief(slug="art", pitch="p")
    written = _writer()
    edited = EditorResult(
        review_markdown="rev",
        checklist_scores={"voice": 2},
        manuscript_corrected="final",
    )
    work = save_artifacts(brief, written, edited)
    assert (work / "twist_sheet.json").exists()
    data = json.loads((work / "twist_sheet.json").read_text())
    assert data["twist_final"] == "TWIST_FINAL_X"
