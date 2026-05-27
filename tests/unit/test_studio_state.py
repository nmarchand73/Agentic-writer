"""Studio AG-UI state."""

from agentic_writer.api.studio_state import (
    default_pipeline_steps,
    patch_step_status,
)


def test_default_steps_with_export():
    steps = default_pipeline_steps(include_export=True)
    assert len(steps) == 6
    assert steps[0].status == "pending"
    assert any("Print layout" in s.description for s in steps)


def test_default_steps_md_only():
    steps = default_pipeline_steps(include_export=False)
    assert len(steps) == 5
    assert not any("Print layout" in s.description for s in steps)


def test_patch_step_status():
    op = patch_step_status(1, "running")
    assert op["path"] == "/steps/1/status"
    assert op["value"] == "running"
