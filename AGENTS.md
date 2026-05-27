# Agentic Writer — agent instructions

- Skills live under `skills/` (`story-writer`, `manuscript-editor`, `print-layout` pour docx/pdf).
- Writer returns `WriterResult`; Editor returns `EditorResult`; no plot changes in edit pass.
- CLI: `generate SLUG --pitch` or `--brief` YAML; defaults in `config.toml`.
- Docx/pdf via `docx_build` + `skills/print-layout/scripts/build_story.sh` (patch FR, folios, validate, LibreOffice PDF). Agent optionnel : `agents/formatter.py`.
- Run `uv run pytest -m bootstrap` before calling the live API.
