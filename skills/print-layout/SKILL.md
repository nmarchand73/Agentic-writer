---
name: print-layout
description: Format Agentic Writer manuscripts for print-ready docx and PDF (A5 Palatino, French hyphenation, folios). Use after Editor output — not for plot changes. Triggers include "docx", "pdf", "mise en page", "print layout", "export imprimable".
---

# Print Layout

Étape finale du pipeline Agentic Writer : transformer `manuscript_final.md` en **docx** puis **pdf** selon les standards livre (skill calquée sur `twilight-zone-novelist`).

## Rôle

- **Ne pas** réécrire le récit.
- Appliquer `references/modern_layout_guide.md` (A5, Palatino Linotype, corps justifié, chapitres en section impaire).
- Exécuter le pipeline `scripts/build_story.sh` (generate → unpack → patch FR → footers → validate → PDF).

## Conventions markdown attendues

| Syntaxe | Rendu docx |
|---------|------------|
| `# Titre` | Couverture |
| `## Titre chapitre` | Nouvelle section + en-tête chapitre (numéro romain) |
| Paragraphes | Corps justifié, alinéa |
| `> ligne` | Bloc narration encadré (italique) |
| `* * *` ou `---` | Séparateur de scène |

Le générateur canonique est `scripts/generate_from_md.js` (ne pas utiliser le template minimal racine).

## Pipeline shell

```bash
export STORY_WORK_DIR=output/{slug}
export STORY_BASE_NAME={slug}
bash skills/print-layout/scripts/build_story.sh {slug} skills/print-layout/scripts/generate_from_md.js
```

Variables : `DOCX_OFFICE_SCRIPTS` → `NewBooks/.cursor/skills/_shared/story-build/office/`.

## Fichiers livrés vs temporaires

**Conservés** dans `output/{slug}/` : `twist_sheet.json`, `draft_manuscript.md`, `review.md`, `manuscript_final.md`, `{slug}-{format}.docx`, `{slug}-{format}.pdf`.

**Supprimés automatiquement** en fin de pipeline : `generate.js`, `{slug}_unpacked/`, `{slug}_print.html`, `.~lock*`.

## Checklist livraison

- [ ] `references/modern_layout_guide.md` respecté
- [ ] `build_story.sh` terminé sans erreur (validate.py OK)
- [ ] `{slug}-{format}.docx` et `{slug}-{format}.pdf` dans le dossier de travail
- [ ] PDF relu visuellement (marges, veuves, folios)
