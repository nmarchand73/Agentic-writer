"""Agent feedback injection for rewrites."""

from agentic_writer.editorial_io import build_chapter_prompt
from agentic_writer.editorial_models import (
    AuditorVerdict,
    ChapterOutline,
    StoryBlueprint,
)
from agentic_writer.io import build_edit_prompt
from agentic_writer.models import Brief, EditorResult, TwistSheet, WriterResult
from agentic_writer.rewrite_feedback import (
    format_auditor_manuscript_rewrite_section,
    format_auditor_rewrite_section,
)


def _twist() -> TwistSheet:
    return TwistSheet(
        twist_final="t",
        mid_twist="m",
        coda_bombe="c",
        mensonge_omission="l",
        scenes_recontextualisees=["a", "b", "c"],
        indices_foreshadowing=["i", "j"],
        pitch_booktok="p",
    )


def _verdict() -> AuditorVerdict:
    return AuditorVerdict(
        passed=False,
        overall_score=55,
        checklist_scores={"voice": 1, "twists_intact": 2},
        issues=["Hook chapitre 1 trop faible"],
        chapters_to_rewrite=[1],
        review_markdown="Renforcer la tension dès l'ouverture.",
    )


def test_chapter_prompt_includes_auditor_feedback():
    brief = Brief(slug="s", pitch="p", format="flash", lang="fr")
    blueprint = StoryBlueprint(
        title="T",
        twist_sheet=_twist(),
        chapters=[
            ChapterOutline(
                index=1,
                title="Un",
                beat="b",
                hook="h",
                target_words=1200,
            )
        ],
    )
    prompt = build_chapter_prompt(
        brief,
        blueprint,
        blueprint.chapters[0],
        previous_excerpt=None,
        total_chapters=1,
        auditor_verdict=_verdict(),
    )
    assert "retours auditeur" in prompt.lower()
    assert "Hook chapitre 1 trop faible" in prompt
    assert "Renforcer la tension" in prompt


def test_edit_prompt_includes_auditor_and_prior_editor():
    brief = Brief(slug="s", pitch="p", format="flash", lang="fr")
    written = WriterResult(twist_sheet=_twist(), manuscript="# Hi\n")
    prior = EditorResult(
        review_markdown="Couper les adverbes inutiles.",
        checklist_scores={"voice": 1},
        manuscript_corrected="# Hi\n",
    )
    verdict = _verdict()
    prompt = build_edit_prompt(
        written,
        brief,
        auditor_verdict=verdict,
        prior_editor=prior,
    )
    assert format_auditor_manuscript_rewrite_section(verdict)[:40] in prompt
    assert "Couper les adverbes" in prompt
    assert "Hook chapitre 1" in prompt
