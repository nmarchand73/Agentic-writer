"""Output folder cleanup after print layout."""

from pathlib import Path

import pytest

from agentic_writer.cleanup import cleanup_work_dir


@pytest.mark.unit
def test_cleanup_removes_generate_and_unpacked(tmp_path):
    work = tmp_path / "story"
    work.mkdir()
    (work / "manuscript_final.md").write_text("# T", encoding="utf-8")
    (work / "generate.js").write_text("// temp", encoding="utf-8")
    unpacked = work / "story_unpacked"
    unpacked.mkdir()
    (unpacked / "word").mkdir()

    removed = cleanup_work_dir("story", work)

    assert "generate.js" in removed
    assert not (work / "generate.js").exists()
    assert not unpacked.exists()
    assert (work / "manuscript_final.md").exists()
