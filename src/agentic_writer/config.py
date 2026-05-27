"""Project paths, config.toml, and environment."""

from __future__ import annotations

import os
import tomllib
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
NEWBOOKS_ROOT = PROJECT_ROOT.parent
SKILLS_ROOT = PROJECT_ROOT / "skills"
WRITER_SKILL_DIR = SKILLS_ROOT / "story-writer"
EDITOR_SKILL_DIR = SKILLS_ROOT / "manuscript-editor"
ARCHITECT_SKILL_DIR = SKILLS_ROOT / "story-architect"
AUDITOR_SKILL_DIR = SKILLS_ROOT / "story-auditor"
PRINT_LAYOUT_SKILL_DIR = SKILLS_ROOT / "print-layout"
BUILD_STORY_SCRIPT = PRINT_LAYOUT_SKILL_DIR / "scripts/build_story.sh"
GENERATE_FROM_MD_SCRIPT = PRINT_LAYOUT_SKILL_DIR / "scripts/generate_from_md.js"
OFFICE_SCRIPTS_DIR = (
    NEWBOOKS_ROOT / ".cursor/skills/_shared/story-build/office"
)


def normalize_pydantic_ai_model(model: str) -> str:
    """Map legacy ``openai:`` to Chat Completions (avoids Pydantic AI v2 deprecation warning)."""
    if model.startswith("openai:") and not model.startswith(
        ("openai-chat:", "openai-responses:")
    ):
        return "openai-chat:" + model.removeprefix("openai:")
    return model


@lru_cache
def load_settings() -> dict:
    load_dotenv(PROJECT_ROOT / ".env")
    config_path = PROJECT_ROOT / "config.toml"
    data: dict = {}
    if config_path.exists():
        with config_path.open("rb") as f:
            data = tomllib.load(f)
    defaults = data.get("defaults", {})
    output = data.get("output", {})
    models_cfg = data.get("models", {})
    pipeline = data.get("pipeline", {})
    root = os.environ.get("AGENTIC_WRITER_OUTPUT") or output.get("root", "../output")
    output_root = (PROJECT_ROOT / root).resolve()
    base_model = normalize_pydantic_ai_model(
        os.environ.get("OPENAI_MODEL", "openai-chat:gpt-4o")
    )

    def _role_model(role: str) -> str:
        env_key = f"OPENAI_MODEL_{role.upper()}"
        raw = os.environ.get(env_key) or models_cfg.get(role) or base_model
        return normalize_pydantic_ai_model(raw)

    return {
        "default_format": defaults.get("format", "nouvelle"),
        "default_lang": defaults.get("lang", "fr"),
        "output_root": output_root,
        "openai_model": base_model,
        "openai_api_key": os.environ.get("OPENAI_API_KEY"),
        "max_audit_retries": int(
            os.environ.get("AGENTIC_WRITER_MAX_AUDIT_RETRIES")
            or pipeline.get("max_audit_retries", 1)
        ),
        "model_architect": _role_model("architect"),
        "model_writer": _role_model("writer"),
        "model_editor": _role_model("editor"),
        "model_auditor": _role_model("auditor"),
        "model_chapter": _role_model("chapter"),
    }


def output_dir(slug: str) -> Path:
    path = load_settings()["output_root"] / slug
    path.mkdir(parents=True, exist_ok=True)
    return path
