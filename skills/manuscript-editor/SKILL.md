---
name: manuscript-editor
description: Review and correct domestic psychological suspense manuscripts (post Writer pass). Use for editorial pass after Writer output — voice, continuity, foreshadowing, BookTok pitch, format length. Does not rewrite plot twists.
---

# Manuscript Editor

Relecture adversariale des manuscrits produits par `story-writer`. L'agent Writer a déjà figé la fiche twist ; tu **ne changes pas** les twists, seulement la prose et la cohérence.

## Sortie structurée (Agentic Writer)

Retourne un `EditorResult` :

- `review_markdown` — rapport de relecture (forces, faiblesses, actions)
- `checklist_scores` — dict nom → score 0–2 (voir `references/review_rubric.md`)
- `manuscript_corrected` — manuscrit corrigé en markdown

## Workflow

1. Lire `references/review_rubric.md`.
2. Optionnel : `read_skill_resource` sur les guides McFadden (`narrative_style_guide.md`, etc.) — **lecture seule**.
3. Vérifier que le twist final, mid-twist et coda du prompt restent intacts dans le sens narratif.
4. Corriger voix (présent, 1re personne, ironie), hooks de chapitre, foreshadowing, longueur selon format.
5. Produire le rapport et le manuscrit corrigé.

## Interdictions

- Réécrire la fiche twist ou inventer un nouveau twist final.
- Passer en 3e personne ou passé simple dominant.
- Allonger une flash au-delà du format.
