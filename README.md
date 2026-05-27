# Agentic Writer

Automated **story pipeline** (Writer → Editor → markdown → **docx/pdf**). The **Studio** uses **[CopilotKit](https://www.copilotkit.ai/) v2** + **[AG-UI](https://docs.ag-ui.com/)**: **Pydantic AI** serves `/agui`, **Next.js** runs the CopilotKit runtime (`HttpAgent`, persisted threads). **Generative UI** syncs pipeline steps, manuscript, and errors via shared agent state (`STATE_SNAPSHOT` / `STATE_DELTA`)—not chat-only. **CLI** runs the same pipeline headlessly.

**Site:** [nmarchand73.github.io/Agentic-writer](https://nmarchand73.github.io/Agentic-writer/) (overview) · full Studio runs locally.

---

## Why this stack

### CopilotKit, AG-UI & generative UI

| Benefit | What you get |
|---------|----------------|
| **Standard agent ↔ UI wire** | AG-UI events (SSE) instead of ad-hoc WebSockets or custom JSON for every screen. |
| **Generative UI, not chat-only** | Pipeline steps, slug, errors, and deliverables live in **shared agent state**—the React tree reacts to `STATE_DELTA` while tools run. |
| **Backend freedom** | Python agent (Pydantic AI + skills) stays in FastAPI; the UI stays in Next.js via `HttpAgent`—clear split, same contract as other AG-UI clients. |
| **Threads & replay** | CopilotKit v2 multi-route API + on-disk persistence: resume conversations and reconnect without re-prompting from scratch. |
| **Progress on long tools** | `StudioProgressBridge` streams step updates during `run_story_generation`, so the UI does not freeze until the tool returns. |
| **Faster product iteration** | CopilotKit chat, suggestions, and runtime plumbing are off-the-shelf; you focus on story tools and `StudioState`. |

### BDD (Gherkin + pytest-bdd)

Specs live in [`specs/bdd/`](specs/bdd/)—executable contracts, not slide-ware.

| Benefit | What you get |
|---------|----------------|
| **Shared language** | Product-style scenarios (`Given` / `When` / `Then`) that devs, QA, and future-you can read without spelunking test code. |
| **CI without OpenAI** | Markers `bootstrap`, `unit`, `integration`, `ui` cover doctor, CLI, pipeline, export, API, and threads with **mocked agents**—cheap, deterministic PR checks. |
| **Slice-aligned coverage** | One feature file per concern (env, CLI, pipeline, export, Studio API, chat persistence, optional `e2e`). |
| **Regression safety** | Changes to brief parsing, artefact paths, print-layout cleanup, or AG-UI state break a named scenario—not a vague “tests failed”. |
| **Living documentation** | Scenarios document *observable* behaviour (files on disk, HTTP status, thread list); see [`specs/bdd/README.md`](specs/bdd/README.md). |

---

## Prerequisites

- **uv** + Python ≥ 3.10  
- **Node.js** ≥ 18 (docx export + Studio)  
- **OpenAI API key** (generate / Studio; not needed for mocked tests)  
- **LibreOffice** (`soffice`) — only for PDF export (skip with `--md-only`)

---

## Install

```bash
cd Agentic-writer
uv sync --all-extras
npm install              # docx export (repo root)
cd web && npm install && cd ..
cp .env.example .env     # set OPENAI_API_KEY
uv run agentic-writer doctor   # must exit 0
```

---

## Configuration

### Root `.env`

| Variable | Required | Default / notes |
|----------|----------|-----------------|
| `OPENAI_API_KEY` | yes (live runs) | — |
| `OPENAI_MODEL` | no | `openai-chat:gpt-4o` |
| `LOG_LEVEL` | no | `INFO` |
| `AGENTIC_WRITER_OUTPUT` | no | see `config.toml` → `NewBooks/output/` |
| `AGENTIC_WRITER_THREADS_DIR` | no | `.data/studio-threads/` (Studio chats) |

### `config.toml`

```toml
[defaults]
format = "nouvelle"   # flash | nouvelle | novella
lang = "fr"

[output]
root = "../output"
```

### Studio — `web/.env.local`

```bash
NEXT_PUBLIC_AGENTIC_WRITER_API=http://127.0.0.1:8000
AGENTIC_WRITER_AGUI_URL=http://127.0.0.1:8000/agui
```

---

## Run — CLI

```bash
uv run agentic-writer generate <slug> \
  --pitch "Your pitch." \
  --format nouvelle \
  --lang fr
```

| Flag | Purpose |
|------|---------|
| `--brief path.yaml` | YAML brief instead of inline slug/pitch |
| `--md-only` | Stop after markdown (no docx/pdf) |
| `-v` / `-q` | DEBUG / WARNING+ logs |

**Output:** `NewBooks/output/<slug>/` — `twist_sheet.json`, `draft_manuscript.md`, `review.md`, `manuscript_final.md`, optional `<slug>.docx` & `.pdf`.

```bash
uv run agentic-writer generate --brief examples/briefs/flash-smoke.yaml --md-only
```

---

## Run — Studio

**Terminal 1 — API**

```bash
uv run agentic-writer serve --port 8000
```

**Terminal 2 — UI**

```bash
cd web && npm run dev
```

Open [http://localhost:3000](http://localhost:3000). Use **History** in the header to resume past chats (stored under `.data/studio-threads/`).

---

## Run — tests

From `Agentic-writer/`:

```bash
# CI suite (no OpenAI)
uv run pytest -m "bootstrap or unit or integration or ui"

# All Gherkin BDD specs
uv run pytest tests/bdd/

# Studio thread persistence (needs npx)
uv run pytest tests/bdd/test_studio_threads.py -m ui

# Live API (needs OPENAI_API_KEY)
uv run pytest -m e2e
```

```bash
cd web && npm run build   # optional frontend check
```

BDD details: [`specs/bdd/README.md`](specs/bdd/README.md).

---

## Layout

```text
Agentic-writer/     CLI, pipeline, skills, tests
web/                Studio (Next.js)
NewBooks/output/    generated stories (gitignored)
.data/studio-threads/   Studio chat history (gitignored)
```

---

## Troubleshooting

| Issue | Check |
|-------|--------|
| `doctor` fails | `skills/story-writer/SKILL.md`, `npm install` at root |
| No docx/pdf | Node + `docx` package; or use `--md-only` |
| No PDF | LibreOffice / `soffice` |
| Studio empty / errors | `serve` running, `OPENAI_API_KEY`, `web/.env.local` URLs |

Further design notes: [`../doc/agentic-writer/plan.md`](../doc/agentic-writer/plan.md).
