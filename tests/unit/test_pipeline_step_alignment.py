"""Pipeline step labels must align 1:1 with run_pipeline indices (Studio UI)."""

from __future__ import annotations

import pytest

from agentic_writer.pipeline import PipelineError, _step_index
from agentic_writer.pipeline_steps import pipeline_step_defs, pipeline_step_labels


def _indices(*, include_export: bool) -> dict[str, int]:
    labels = pipeline_step_labels(include_export=include_export)
    out = {
        "brief": _step_index(labels, "valider le brief"),
        "architect": _step_index(labels, "architecte"),
        "chapters": _step_index(labels, "writer"),
        "editor": _step_index(labels, "editor"),
        "auditor": _step_index(labels, "auditeur"),
        "artifacts": _step_index(labels, "artefacts"),
        "delivery": len(labels) - 1,
    }
    if include_export:
        out["print"] = _step_index(labels, "print layout")
    return out


def test_step_indices_with_export():
    labels = pipeline_step_labels(include_export=True)
    defs = pipeline_step_defs(include_export=True)
    assert len(labels) == len(defs) == 8

    idx = _indices(include_export=True)
    assert idx == {
        "brief": 0,
        "architect": 1,
        "chapters": 2,
        "editor": 3,
        "auditor": 4,
        "artifacts": 5,
        "print": 6,
        "delivery": 7,
    }
    assert labels[idx["print"]].startswith("Print layout")
    assert labels[idx["delivery"]] == "Livraison terminée"


def test_step_indices_md_only():
    labels = pipeline_step_labels(include_export=False)
    assert len(labels) == 7

    idx = _indices(include_export=False)
    assert idx == {
        "brief": 0,
        "architect": 1,
        "chapters": 2,
        "editor": 3,
        "auditor": 4,
        "artifacts": 5,
        "delivery": 6,
    }
    assert not any("Print layout" in label for label in labels)
    assert labels[idx["delivery"]] == "Livraison terminée"


def test_step_index_unique_needles():
    labels = pipeline_step_labels(include_export=True)
    needles = [
        "valider le brief",
        "architecte",
        "writer",
        "editor",
        "auditeur",
        "artefacts",
        "print layout",
        "livraison",
    ]
    found = [_step_index(labels, n) for n in needles]
    assert len(found) == len(set(found)), f"duplicate indices: {found}"


def test_step_index_unknown_raises():
    with pytest.raises(PipelineError, match="introuvable"):
        _step_index(["Only step"], "writer")
