"""Repères éditoriaux des formats récit (CLI, prompts, doc)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StoryFormatSpec:
    key: str
    label: str
    words: str
    pages_a5: str
    description: str
    supported: bool = True


STORY_FORMAT_SPECS: tuple[StoryFormatSpec, ...] = (
    StoryFormatSpec(
        "flash",
        "Flash",
        "~800–2 500 mots",
        "~3–10 p. (A5)",
        "Micro-fiction, un arc court (smoke test, idée forte).",
    ),
    StoryFormatSpec(
        "nouvelle",
        "Nouvelle",
        "8 000–15 000 mots",
        "~30–55 p. (A5)",
        "Nouvelle de genre — format par défaut (config.toml).",
    ),
    StoryFormatSpec(
        "novella",
        "Novella",
        "30 000–50 000 mots",
        "~100–200 p. (A5)",
        "Roman court, chapitres courts, structure complète.",
    ),
    StoryFormatSpec(
        "roman",
        "Roman",
        "70 000–90 000 mots",
        "~250–350 p. (A5)",
        "Roman long — repère skill, pas encore exposé au pipeline.",
        supported=False,
    ),
)

SUPPORTED_FORMAT_KEYS: tuple[str, ...] = tuple(
    s.key for s in STORY_FORMAT_SPECS if s.supported
)


def _table_lines() -> list[str]:
    lines = [
        "Formats récit (standards livre, skill story-writer)",
        "",
        f"  {'Format':<10} {'Mots':<22} {'Pages A5':<14} Description",
        f"  {'-' * 10} {'-' * 22} {'-' * 14} {'-' * 20}",
    ]
    for spec in STORY_FORMAT_SPECS:
        mark = "" if spec.supported else " (bientôt)"
        lines.append(
            f"  {spec.key:<10} {spec.words:<22} {spec.pages_a5:<14} "
            f"{spec.description}{mark}"
        )
    lines.extend(
        [
            "",
            "  Langues : fr | en  (--lang)",
            "  Export  : docx + pdf A5 Palatino (sauf --md-only)",
            "  Exemple : agentic-writer generate mon-slug --pitch \"…\" --format nouvelle",
        ]
    )
    return lines


FORMATS_HELP_TEXT: str = "\n".join(_table_lines())

FORMAT_OPTION_HELP: str = (
    f"Format récit : {' | '.join(SUPPORTED_FORMAT_KEYS)} "
    "(voir agentic-writer formats)"
)

GENERATE_EPILOG: str = (
    "Indique le format via --format ou dans un brief YAML (champ format). "
    "Liste détaillée : agentic-writer formats"
)
