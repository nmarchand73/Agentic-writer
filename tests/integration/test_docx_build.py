"""docx_build subprocess integration."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agentic_writer.docx_build import build_docx
from agentic_writer.pipeline import PipelineError


@pytest.mark.integration
def test_build_docx_invokes_build_story(tmp_path):
    work = tmp_path / "export-integ"
    work.mkdir()
    (work / "manuscript_final.md").write_text("# Hi\n\nText.", encoding="utf-8")

    with patch("agentic_writer.docx_build.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        build_docx("export-integ", work, "# Hi\n\nText.", format="flash")
        assert mock_run.called
        args = mock_run.call_args[0][0]
        assert "export-integ-flash" in args


@pytest.mark.integration
def test_build_docx_failure_raises(tmp_path):
    work = tmp_path / "fail"
    work.mkdir()

    (work / "manuscript_final.md").write_text("x", encoding="utf-8")
    with patch("agentic_writer.docx_build.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="boom")
        with pytest.raises(PipelineError):
            build_docx("fail", work, "text")
