"""Golden JSON fixtures validate against models."""

import json
from pathlib import Path

import pytest

from agentic_writer.models import EditorResult, WriterResult

GOLDEN = Path(__file__).parent.parent / "fixtures" / "golden"


@pytest.mark.regression
def test_golden_writer_schema():
    data = json.loads((GOLDEN / "writer_flash.json").read_text())
    WriterResult.model_validate(data)


@pytest.mark.regression
def test_golden_editor_schema():
    data = json.loads((GOLDEN / "editor_flash.json").read_text())
    with pytest.raises(ValueError, match="checklist_scores"):
        EditorResult.model_validate(data)
    data["checklist_scores"] = {
        "voice": 2,
        "twists_intact": 2,
        "foreshadowing": 2,
        "chapter_hooks": 2,
        "pitch_booktok": 2,
        "format_length": 2,
        "continuity": 2,
    }
    EditorResult.model_validate(data)
