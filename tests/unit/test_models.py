"""Pydantic model validation."""

import pytest
from pydantic import ValidationError

from agentic_writer.models import (
    Brief,
    EditorResult,
    TwistSheet,
    WriterResult,
    humanize_slug,
)


def test_humanize_slug():
    assert humanize_slug("la-domestique-du-lac") == "La domestique du lac"


def test_twist_sheet_pitch_too_long():
    with pytest.raises(ValidationError):
        TwistSheet(
            twist_final="a",
            mid_twist="b",
            coda_bombe="c",
            mensonge_omission="d",
            scenes_recontextualisees=["1", "2", "3"],
            indices_foreshadowing=["i1", "i2"],
            pitch_booktok=" ".join(["word"] * 20),
        )


def test_writer_result_empty_manuscript():
    sheet = TwistSheet(
        twist_final="a",
        mid_twist="b",
        coda_bombe="c",
        mensonge_omission="d",
        scenes_recontextualisees=["1", "2", "3"],
        indices_foreshadowing=["i1", "i2"],
        pitch_booktok="short pitch ok",
    )
    with pytest.raises(ValidationError):
        WriterResult(twist_sheet=sheet, manuscript="   ")


def test_editor_scores_invalid():
    with pytest.raises(ValidationError):
        EditorResult(
            review_markdown="x",
            checklist_scores={},
            manuscript_corrected="y",
        )
    with pytest.raises(ValidationError):
        EditorResult(
            review_markdown="x",
            checklist_scores={"voice": 5},
            manuscript_corrected="y",
        )


def test_brief_defaults():
    b = Brief(slug="s", pitch="p")
    assert b.format == "nouvelle"
    assert b.lang == "fr"
