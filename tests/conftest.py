"""Shared pytest fixtures."""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

import pytest

from agentic_writer.log_config import setup_logging

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).parent / "fixtures"

# Slugs pouvant apparaître dans output/ lors de tests ou d'anciennes runs — retirés en fin de session.
TEST_OUTPUT_SLUGS = frozenset(
    {
        "e2e-flash",
        "pipeline-integ",
        "artefacts-test",
        "twist-persist",
        "export-integ",
        "test",
        "ma-nouvelle",
        "studio-integ",
        "hangar-scelle",
    }
)


@pytest.fixture
def project_root() -> Path:
    return PROJECT_ROOT


@pytest.fixture
def writer_flash_data() -> dict:
    return json.loads((FIXTURES / "writer_flash.json").read_text(encoding="utf-8"))


@pytest.fixture
def editor_flash_data() -> dict:
    return json.loads((FIXTURES / "editor_flash.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="session", autouse=True)
def _configure_test_logging() -> None:
    """Loguru sur stderr (voir pyproject addopts -s) pour toute la session pytest."""
    level = os.environ.get("TEST_LOG_LEVEL") or os.environ.get("LOG_LEVEL", "INFO")
    setup_logging(level=level)


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_output_artifacts():
    """Supprime les dossiers de sortie créés par d'anciens tests ou runs manuels ciblés."""
    yield
    from agentic_writer.config import load_settings

    root = load_settings()["output_root"]
    for slug in TEST_OUTPUT_SLUGS:
        path = root / slug
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
