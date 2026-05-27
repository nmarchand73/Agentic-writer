# BDD — Agentic Writer

Contrat SDD (Wasowski) : langage métier, valeurs concrètes, un `When` = une action, `Then` observable.

## Fichiers par slice

| Feature | Sujet métier |
|---------|----------------|
| `01_environment` | Doctor, skills Writer/Editor, print-layout |
| `02_cli_generate` | Brief minimal, YAML, md-only vs export |
| `03_pipeline_text` | Writer → Editor, artefacts, twist_sheet |
| `04_export_imprimable` | print-layout, nettoyage temporaires |
| `05_e2e_live` | Génération réelle (API, skip si pas de clé) |
| `06_ag_ui_studio` | Health, manuscrit, PDF, état pipeline UI |
| `07_studio_threads` | Persistance conversations Studio (disque) |

## Markers

- `@agentic-writer` — tag racine (toutes les features)
- `@bootstrap` `@cli` `@pipeline` `@export` — slices 1–4
- `@studio` `@ui` `@threads` — Studio web
- `@e2e` `@slow` `@requires_api` — nightly (`05`, skip sans `OPENAI_API_KEY`)

## Nettoyage après tests

| Zone | Comportement |
|------|----------------|
| Tests unitaires / intégration / BDD (sauf e2e) | `tmp_path` pytest → dossier temporaire **supprimé automatiquement** |
| BDD e2e | sortie sous `tmp_path` via `AGENTIC_WRITER_OUTPUT` → idem |
| BDD threads Studio | JSON sous `tmp_path` → idem |
| Pipeline réel (generate / Studio) | `cleanup_work_dir` retire `generate.js`, `{slug}_unpacked/`, `{slug}_print.html` après export print-layout |
| Fin de session pytest | `conftest` retire les slugs de test connus sous `output/` (ex. `e2e-flash`, `ma-nouvelle`) |

Les livrables utiles (`manuscript_final.md`, docx, pdf) ne sont **pas** effacés par le nettoyage pipeline.

## CI

```bash
uv run pytest -m "bootstrap or unit or integration or ui"
uv run pytest tests/bdd/test_studio_threads.py -m ui   # Node/npx requis
uv run pytest -m e2e                                   # OPENAI_API_KEY + réseau
```
