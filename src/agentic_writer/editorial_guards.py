"""Garde-fous programmatiques post-génération (v2)."""

from __future__ import annotations

import re

from agentic_writer.editorial_plan import chapter_plan_for
from agentic_writer.models import Brief, TwistSheet


def word_count(text: str) -> int:
    return len(re.findall(r"\S+", text))


def check_twist_sheet(sheet: TwistSheet) -> list[str]:
    issues: list[str] = []
    if len(sheet.scenes_recontextualisees) < 3:
        issues.append("twist_sheet: moins de 3 scènes à recontextualiser")
    if len(sheet.indices_foreshadowing) < 2:
        issues.append("twist_sheet: moins de 2 indices de foreshadowing")
    if len(re.findall(r"\S+", sheet.pitch_booktok)) > 15:
        issues.append("twist_sheet: pitch_booktok > 15 mots")
    return issues


def check_manuscript_length(brief: Brief, manuscript: str) -> list[str]:
    plan = chapter_plan_for(brief.format)
    n = word_count(manuscript)
    issues: list[str] = []
    if n < plan.min_total_words:
        issues.append(
            f"longueur: {n} mots < minimum {plan.min_total_words} pour format {brief.format}"
        )
    if n > plan.max_total_words:
        issues.append(
            f"longueur: {n} mots > maximum {plan.max_total_words} pour format {brief.format}"
        )
    return issues


def merge_guard_issues(*groups: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for group in groups:
        for item in group:
            if item not in seen:
                seen.add(item)
                out.append(item)
    return out
