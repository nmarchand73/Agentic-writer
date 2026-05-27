"""Libellés d'étapes pipeline (CLI logs + UI Studio)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PipelineStepDef:
    description: str


def pipeline_step_defs(*, include_export: bool) -> list[PipelineStepDef]:
    steps = [
        PipelineStepDef("Valider le brief (slug, pitch, format)"),
        PipelineStepDef("Writer — fiche twist + brouillon"),
        PipelineStepDef("Editor — relecture et manuscrit corrigé"),
    ]
    steps.append(PipelineStepDef("Artefacts markdown — twist, brouillon, relecture"))
    if include_export:
        steps.append(
            PipelineStepDef("Print layout — docx & pdf (A5 Palatino, skill print-layout)")
        )
    steps.append(PipelineStepDef("Livraison terminée"))
    return steps


def pipeline_step_labels(*, include_export: bool) -> list[str]:
    return [s.description for s in pipeline_step_defs(include_export=include_export)]
