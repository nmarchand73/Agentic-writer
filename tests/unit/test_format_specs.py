"""Unit tests — repères formats récit."""

from agentic_writer.format_specs import (
    FORMAT_OPTION_HELP,
    FORMATS_HELP_TEXT,
    SUPPORTED_FORMAT_KEYS,
)


def test_supported_formats():
    assert SUPPORTED_FORMAT_KEYS == ("flash", "nouvelle", "novella")


def test_formats_help_lists_all_keys():
    for key in ("flash", "nouvelle", "novella", "roman"):
        assert key in FORMATS_HELP_TEXT
    assert "8 000–15 000" in FORMATS_HELP_TEXT
    assert "docx + pdf" in FORMATS_HELP_TEXT


def test_format_option_help():
    assert "nouvelle" in FORMAT_OPTION_HELP
    assert "formats" in FORMAT_OPTION_HELP
