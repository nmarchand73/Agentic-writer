# Agentic Writer — agent instructions

- Skills live under `skills/` (`story-writer`, `manuscript-editor`, `story-architect`, `story-auditor`, `print-layout`).
- Pipeline : Architecte → chapitres → Editor → Auditeur → export.
- `WriterResult` / `EditorResult` ; pas de changement de plot en relecture.
- CLI : `generate SLUG --pitch` ou `--brief` YAML ; défauts dans `config.toml`.
- Docx/pdf via `docx_build` + `skills/print-layout/scripts/build_story.sh` (patch FR, folios, validate, LibreOffice PDF). Agent optionnel : `agents/formatter.py`.
- Run `uv run pytest -m bootstrap` before calling the live API.
