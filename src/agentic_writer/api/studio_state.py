"""AG-UI shared state for the story studio (generative step UI)."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

StepStatus = Literal["pending", "completed", "running"]


class PipelineStep(BaseModel):
    description: str
    status: StepStatus = "pending"


class StudioState(BaseModel):
    """Synced with CopilotKit via useAgent / STATE_SNAPSHOT + STATE_DELTA."""

    slug: str = ""
    pitch: str = ""
    format: Literal["flash", "nouvelle", "novella"] = "nouvelle"
    lang: Literal["fr", "en"] = "fr"
    steps: list[PipelineStep] = Field(default_factory=list)
    output_dir: str | None = None
    manuscript_preview: str | None = None
    manuscript_md: str | None = None
    error: str | None = None


def default_pipeline_steps(*, include_export: bool = True) -> list[PipelineStep]:
    from agentic_writer.pipeline_steps import pipeline_step_defs

    return [
        PipelineStep(description=s.description)
        for s in pipeline_step_defs(include_export=include_export)
    ]


def patch_step_status(index: int, status: StepStatus) -> dict[str, Any]:
    return {"op": "replace", "path": f"/steps/{index}/status", "value": status}
