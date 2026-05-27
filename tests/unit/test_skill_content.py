"""Skill injection into pipeline prompts."""

from agentic_writer.editorial_io import build_architect_prompt, build_chapter_prompt
from agentic_writer.editorial_plan import chapter_plan_for
from agentic_writer.io import build_edit_prompt
from agentic_writer.models import Brief, TwistSheet, WriterResult
from agentic_writer.skill_content import (
    architect_skill_context,
    strip_yaml_frontmatter,
    writer_skill_context,
)


def test_strip_yaml_frontmatter():
    raw = "---\nname: x\n---\n\n# Body\n"
    assert strip_yaml_frontmatter(raw) == "# Body"


def test_architect_context_includes_story_architect():
    ctx = architect_skill_context()
    assert "story-architect" in ctx
    assert "Story architect" in ctx or "architecte" in ctx.lower()


def test_writer_context_includes_story_writer():
    ctx = writer_skill_context()
    assert "story-writer" in ctx


def test_build_architect_prompt_injects_skill():
    brief = Brief(slug="s", pitch="p", format="flash", lang="fr")
    plan = chapter_plan_for("flash")
    prompt = build_architect_prompt(brief, plan)
    assert "Skill injectée" in prompt
    assert "ArchitectResult" in prompt


def test_build_edit_prompt_injects_editor_skill():
    brief = Brief(slug="s", pitch="p", format="flash", lang="fr")
    sheet = TwistSheet(
        twist_final="t",
        mid_twist="m",
        coda_bombe="c",
        mensonge_omission="l",
        scenes_recontextualisees=["a", "b", "c"],
        indices_foreshadowing=["i", "j"],
        pitch_booktok="short pitch",
    )
    written = WriterResult(twist_sheet=sheet, manuscript="# Hi\n")
    prompt = build_edit_prompt(written, brief)
    assert "review_rubric" in prompt
    assert "EditorResult" in prompt
