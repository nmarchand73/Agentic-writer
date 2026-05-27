"""Studio simulates on_step_start/on_step_complete for every pipeline index."""

from __future__ import annotations

import pytest

from agentic_writer.api.studio_state import (
    StudioState,
    ensure_pipeline_steps,
    mark_all_pipeline_steps_completed,
    reset_pipeline_step_statuses,
)
from agentic_writer.pipeline_steps import pipeline_step_labels


@pytest.mark.parametrize("include_export", [True, False])
def test_push_step_cycle_matches_pipeline(include_export: bool):
    labels = pipeline_step_labels(include_export=include_export)
    state = StudioState(slug="sync", pitch="p", md_only=not include_export)
    ensure_pipeline_steps(state, include_export=include_export)
    reset_pipeline_step_statuses(state)

    statuses: list[list[str]] = []

    def record(index: int, status: str) -> None:
        if index < len(state.steps):
            state.steps[index].status = status  # type: ignore[assignment]
        statuses.append([s.status for s in state.steps])

    for i in range(len(labels)):
        record(i, "running")
        assert state.steps[i].status == "running"
        assert all(
            state.steps[j].status == "completed" for j in range(i)
        ), f"step {i}: prior steps should be completed"
        record(i, "completed")

    mark_all_pipeline_steps_completed(state)
    assert all(s.status == "completed" for s in state.steps)
