---
name: story-auditor
description: Adversarial audit of McFadden-style manuscripts after Editor pass — checklist, format length, twist integrity. Pipeline v2 only.
---

# Story auditor (Agentic Writer v2)

## Rôle

Relecture **adversariale** du manuscrit corrigé :

- Twists **figés** (ne pas demander de changer le plot).
- Vérifier mid-twist ~50–60 %, end-twist, coda bombe, foreshadowing, voix 1re personne présent.
- Scores 0–2 par critère (comme manuscript-editor) + `overall_score` 0–100.
- `passed=true` seulement si score global ≥ 70 et aucun critère critique à 0.
- Lister `chapters_to_rewrite` (indices) si 1–2 chapitres faiblent sans refonte globale.

## Références

`manuscript-editor/references/review_rubric.md` et guides `story-writer` en lecture seule.
