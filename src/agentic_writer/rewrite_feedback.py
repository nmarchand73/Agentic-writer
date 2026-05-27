"""Format agent verdicts for chapter rewrites and editor passes."""

from __future__ import annotations

from agentic_writer.editorial_models import AuditorVerdict
from agentic_writer.models import EditorResult

_MAX_REVIEW_CHARS = 6_000


def _truncate(text: str, limit: int = _MAX_REVIEW_CHARS) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def format_auditor_rewrite_section(
    verdict: AuditorVerdict,
    *,
    chapter_index: int,
) -> str:
    """Turn auditor output into mandatory rewrite instructions for one chapter."""
    lines = [
        "## Réécriture — retours auditeur (obligatoire)",
        f"- Score global : {verdict.overall_score}/100",
        f"- Chapitre ciblé : **{chapter_index}** (signalé dans `chapters_to_rewrite`)",
    ]
    weak = [k for k, v in verdict.checklist_scores.items() if v < 2]
    if weak:
        lines.append(f"- Critères faibles : {', '.join(weak)}")
    if verdict.issues:
        lines.append("\n### Problèmes listés")
        lines.extend(f"- {issue}" for issue in verdict.issues)
    if verdict.review_markdown.strip():
        lines.append(
            f"\n### Analyse détaillée\n{_truncate(verdict.review_markdown)}\n"
        )
    lines.append(
        "\nCorrige **ce chapitre** en tenant compte de ces retours. "
        "Twists figés inchangés ; prose et structure du chapitre ajustées."
    )
    return "\n".join(lines) + "\n"


def format_auditor_manuscript_rewrite_section(verdict: AuditorVerdict) -> str:
    """Auditor feedback for a full-manuscript editor pass after chapter rewrites."""
    lines = [
        "## Réécriture — retours auditeur sur le manuscrit (obligatoire)",
        f"- Score global : {verdict.overall_score}/100",
    ]
    if verdict.chapters_to_rewrite:
        idxs = ", ".join(str(i) for i in sorted(verdict.chapters_to_rewrite))
        lines.append(f"- Chapitres réécrits depuis le dernier tour : {idxs}")
    weak = [k for k, v in verdict.checklist_scores.items() if v < 2]
    if weak:
        lines.append(f"- Critères faibles : {', '.join(weak)}")
    if verdict.issues:
        lines.append("\n### Problèmes listés")
        lines.extend(f"- {issue}" for issue in verdict.issues)
    if verdict.review_markdown.strip():
        lines.append(
            f"\n### Analyse détaillée\n{_truncate(verdict.review_markdown)}\n"
        )
    lines.append(
        "\nIntègre ces retours dans `manuscript_corrected` (manuscrit entier, cohérence globale)."
    )
    return "\n".join(lines) + "\n"


def format_editor_rewrite_section(prior: EditorResult) -> str:
    """Prior editor review for a post-audit edit pass."""
    weak = [k for k, v in prior.checklist_scores.items() if v < 2]
    lines = [
        "## Réécriture — retours éditeur du tour précédent (à intégrer)",
    ]
    if weak:
        lines.append(f"- Critères sous la barre : {', '.join(weak)}")
    if prior.review_markdown.strip():
        lines.append(f"\n{_truncate(prior.review_markdown)}\n")
    lines.append(
        "Harmonise le manuscrit complet : chapitres réécrits + reste du texte."
    )
    return "\n".join(lines) + "\n"
