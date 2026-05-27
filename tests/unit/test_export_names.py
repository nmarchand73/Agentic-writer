"""Export file naming."""

from pathlib import Path

from agentic_writer.export_names import (
    export_base_name,
    export_pdf_path,
    resolve_export_pdf_path,
)


def test_export_base_name_includes_format():
    assert export_base_name("signal-77", "flash") == "signal-77-flash"


def test_resolve_export_pdf_prefers_format_suffix(tmp_path):
    work = tmp_path / "signal-77"
    work.mkdir()
    (work / "signal-77.pdf").write_bytes(b"legacy")
    (work / "signal-77-flash.pdf").write_bytes(b"new")

    assert resolve_export_pdf_path(work, "signal-77", "flash") == export_pdf_path(
        work, "signal-77", "flash"
    )


def test_resolve_export_pdf_legacy_fallback(tmp_path):
    work = tmp_path / "hangar"
    work.mkdir()
    legacy = work / "hangar.pdf"
    legacy.write_bytes(b"legacy")

    assert resolve_export_pdf_path(work, "hangar", "nouvelle") == legacy
    assert resolve_export_pdf_path(work, "hangar", None) == legacy
