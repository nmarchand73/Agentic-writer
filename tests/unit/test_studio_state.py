"""Studio AG-UI state."""

from agentic_writer.api.studio_state import (
    StudioState,
    default_pipeline_steps,
    ensure_pipeline_steps,
    mark_all_pipeline_steps_completed,
    patch_step_status,
    reset_pipeline_step_statuses,
)


def test_default_steps_with_export():
    steps = default_pipeline_steps(include_export=True)
    assert len(steps) == 8
    assert steps[0].status == "pending"
    assert any("Print layout" in s.description for s in steps)


def test_default_steps_md_only():
    steps = default_pipeline_steps(include_export=False)
    assert len(steps) == 7
    assert not any("Print layout" in s.description for s in steps)


def test_patch_step_status():
    op = patch_step_status(1, "running")
    assert op["path"] == "/steps/1/status"
    assert op["value"] == "running"


def test_ensure_pipeline_steps_realigns_md_only_mismatch():
    state = StudioState(
        slug="x",
        pitch="y",
        md_only=True,
        steps=default_pipeline_steps(include_export=True),
    )
    assert len(state.steps) == 8
    ensure_pipeline_steps(state, include_export=False)
    assert len(state.steps) == 7
    assert not any("Print layout" in s.description for s in state.steps)


def test_reset_pipeline_step_statuses():
    state = StudioState(
        slug="x",
        pitch="y",
        steps=default_pipeline_steps(include_export=True),
    )
    state.steps[6].status = "running"
    reset_pipeline_step_statuses(state)
    assert all(s.status == "pending" for s in state.steps)


def test_mark_all_pipeline_steps_completed():
    state = StudioState(
        slug="x",
        pitch="y",
        steps=default_pipeline_steps(include_export=True),
    )
    state.steps[6].status = "running"
    mark_all_pipeline_steps_completed(state)
    assert all(s.status == "completed" for s in state.steps)
