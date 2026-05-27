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

## Workflow

1. `load_skill` sur `story-auditor`.
2. `read_skill_resource` pour `manuscript-editor/references/review_rubric.md` (ou équivalent listé par `load_skill`).
3. Évaluer le manuscrit fourni dans le prompt ; retourner `AuditorVerdict` (scores, `passed`, `chapters_to_rewrite` optionnel).

**Pas de scripts** — ne pas appeler `run_skill_script` (aucun script n’est attaché à ce skill).

## Références

`manuscript-editor/references/review_rubric.md` et guides `story-writer` en lecture seule via `read_skill_resource`.
