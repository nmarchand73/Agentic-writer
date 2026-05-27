"""AG-UI shared state for the story studio (generative step UI)."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

from agentic_writer.pipeline_steps import pipeline_step_defs

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
    md_only: bool = False
    steps: list[PipelineStep] = Field(default_factory=list)
    output_dir: str | None = None
    manuscript_preview: str | None = None
    manuscript_md: str | None = None
    error: str | None = None
    usage_input_tokens: int = 0
    usage_output_tokens: int = 0
    usage_requests: int = 0
    estimated_cost_usd: float | None = None


def default_pipeline_steps(*, include_export: bool = True) -> list[PipelineStep]:
    return [
        PipelineStep(description=s.description)
        for s in pipeline_step_defs(include_export=include_export)
    ]


def ensure_pipeline_steps(
    state: StudioState, *, include_export: bool
) -> None:
    """Keep UI steps aligned with pipeline indices (same count and labels)."""
    expected = default_pipeline_steps(include_export=include_export)
    if len(state.steps) != len(expected) or any(
        s.description != e.description for s, e in zip(state.steps, expected)
    ):
        state.steps = expected


def patch_step_status(index: int, status: StepStatus) -> dict[str, Any]:
    return {"op": "replace", "path": f"/steps/{index}/status", "value": status}


def patch_usage_fields(
    *,
    usage_input_tokens: int,
    usage_output_tokens: int,
    usage_requests: int,
    estimated_cost_usd: float | None,
) -> list[dict[str, Any]]:
    delta: list[dict[str, Any]] = [
        {"op": "replace", "path": "/usage_input_tokens", "value": usage_input_tokens},
        {"op": "replace", "path": "/usage_output_tokens", "value": usage_output_tokens},
        {"op": "replace", "path": "/usage_requests", "value": usage_requests},
    ]
    if estimated_cost_usd is not None:
        delta.append(
            {
                "op": "replace",
                "path": "/estimated_cost_usd",
                "value": estimated_cost_usd,
            }
        )
    return delta
