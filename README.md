# Agentic Writer

Automated **story pipeline** (Writer → Editor → markdown → **docx/pdf**). The **Studio** uses **[CopilotKit](https://www.copilotkit.ai/) v2** + **[AG-UI](https://docs.ag-ui.com/)**: **Pydantic AI** serves `/agui`, **Next.js** runs the CopilotKit runtime (`HttpAgent`, persisted threads). **Generative UI** syncs pipeline steps, manuscript, and errors via shared agent state (`STATE_SNAPSHOT` / `STATE_DELTA`)—not chat-only. **CLI** runs the same pipeline headlessly.

**Site:** [nmarchand73.github.io/Agentic-writer](https://nmarchand73.github.io/Agentic-writer/) (overview) · full Studio runs locally.

---

## Architecture

Agentic Writer is **one story pipeline** with **two entry points**: the **CLI** (headless) and the **Studio** (browser + generative UI). Both call the same `run_pipeline()` in Python; only the Studio adds AG-UI state, CopilotKit threads, and REST helpers for manuscript/PDF.

Diagrams use the [C4 model](https://c4model.com/) in [Mermaid](https://mermaid.ai/open-source/syntax/c4.html) fenced blocks below. **They render on GitHub** when you view this README on the repo ([creating diagrams](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)). Editable copies: [`docs/diagrams/`](docs/diagrams/).

### Level 1 — System context (C4Context)

```mermaid
C4Context
  title Agentic Writer - system context

  Person(author, "Author", "Generates fiction via CLI or Studio")
  System(aw, "Agentic Writer", "Writer to Editor pipeline, docx and pdf export, optional Studio UI")
  System_Ext(openai, "OpenAI", "LLM for writer and editor agents")
  SystemDb_Ext(pages, "GitHub Pages", "Static project landing in docs")
  SystemDb(output, "Output store", "Manuscripts and exports per slug")

  Rel(author, aw, "Runs generate and Studio chat")
  Rel(aw, openai, "Calls", "HTTPS API")
  Rel(aw, output, "Reads and writes artefacts")
  Rel(author, pages, "Reads overview", "HTTPS")
```

### Level 2 — Containers (C4Container)

```mermaid
C4Container
  title Agentic Writer - containers

  Person(author, "Author", "CLI user or Studio user")

  System_Boundary(aw, "Agentic Writer") {
    Container(cli, "CLI", "Python Typer", "generate serve doctor")
    Container(studio_web, "Studio Web", "Next.js", "React UI CopilotKit threads")
    Container(studio_api, "Studio API", "FastAPI", "agui REST manuscript pdf")
    Container(pipeline, "Story Pipeline", "Python", "run_pipeline writer editor export")
    ContainerDb(artifacts, "Artifacts store", "filesystem", "output per slug")
    ContainerDb(threads, "Thread store", "filesystem", "studio-threads folder")
  }

  System_Ext(openai, "OpenAI", "Chat completions API")

  Rel(author, cli, "Runs", "shell")
  Rel(author, studio_web, "Uses", "HTTPS")
  Rel(cli, pipeline, "Invokes")
  Rel(studio_web, studio_api, "AG-UI and REST", "HTTP SSE")
  Rel(studio_api, pipeline, "run_story_generation tool")
  Rel(pipeline, openai, "Writer and Editor agents")
  Rel(pipeline, artifacts, "Writes twist md docx pdf")
  Rel(studio_api, artifacts, "Serves manuscript and pdf")
  Rel(studio_web, threads, "Persists threads")
```

### Level 3 — Components (C4Component)

**Studio API** (`src/agentic_writer/api/`)

```mermaid
C4Component
  title Studio API - components

  Container(studio_web, "Studio Web", "Next.js", "Browser and CopilotKit client")
  ContainerDb(artifacts, "Artifacts store", "filesystem", "output per slug")

  Container_Boundary(api, "Studio API") {
    Component(agui_ep, "AG-UI endpoint", "FastAPI", "POST agui AGUIAdapter stream")
    Component(studio_agent, "Studio agent", "Pydantic AI", "create_pipeline_plan run_story_generation")
    Component(progress, "Progress bridge", "Python", "STATE_DELTA during tools")
    Component(rest, "REST handlers", "FastAPI", "health manuscript pdf")
  }

  Rel(studio_web, agui_ep, "HttpAgent SSE")
  Rel(agui_ep, studio_agent, "Runs agent")
  Rel(agui_ep, progress, "Merged stream")
  Rel(studio_agent, progress, "Emits snapshots and deltas")
  Rel(studio_web, rest, "Fetches manuscript and pdf")
  Rel(rest, artifacts, "Reads files")
```

**Story pipeline** (`src/agentic_writer/`)

```mermaid
C4Component
  title Story pipeline - components

  Container(cli, "CLI", "Typer", "Headless entry")
  Container(studio_agent, "Studio agent", "Pydantic AI", "Studio entry via tools")
  System_Ext(openai, "OpenAI", "LLM")
  ContainerDb(artifacts, "Artifacts store", "filesystem", "Per-slug folder")

  Container_Boundary(pipe, "Story Pipeline") {
    Component(orchestrator, "Pipeline orchestrator", "pipeline.py", "run_pipeline step hooks")
    Component(writer, "Writer agent", "Pydantic AI", "story-writer skill")
    Component(editor, "Editor agent", "Pydantic AI", "manuscript-editor skill")
    Component(io, "Artifacts IO", "io.py", "Save twist draft review final md")
    Component(export, "Print export", "docx_build", "print-layout docx and pdf")
  }

  Rel(cli, orchestrator, "generate command")
  Rel(studio_agent, orchestrator, "run_story_generation tool")
  Rel(orchestrator, writer, "Step 1")
  Rel(writer, editor, "Step 2")
  Rel(editor, io, "Step 3")
  Rel(io, export, "Step 4 optional")
  Rel(writer, openai, "LLM")
  Rel(editor, openai, "LLM")
  Rel(io, artifacts, "Writes")
  Rel(export, artifacts, "Writes docx and pdf")
```

### Dynamic — Studio generate (C4Dynamic)

Numbered `Rel` order = runtime sequence.

```mermaid
C4Dynamic
  title Studio - generate story dynamic

  Person(author, "Author")
  Container(studio_web, "Studio Web", "Next.js", "StudioChat TaskProgress")
  ContainerDb(artifacts, "Artifacts store", "filesystem", "output per slug")

  Container_Boundary(api, "Studio API") {
    Component(ck_route, "CopilotKit route", "Hono", "copilotkit HttpAgent")
    Component(agui, "AG-UI adapter", "FastAPI", "POST agui")
    Component(tools, "Studio tools", "Pydantic AI", "plan and run_story_generation")
    Component(rest, "REST", "FastAPI", "manuscript pdf")
  }

  Container(pipeline, "Story Pipeline", "Python", "run_pipeline")

  Rel(author, studio_web, "1 Sends chat")
  Rel(studio_web, ck_route, "2 POST agent run")
  Rel(ck_route, agui, "3 AG-UI SSE")
  Rel(agui, tools, "4 create_pipeline_plan")
  Rel(tools, agui, "5 STATE_SNAPSHOT")
  Rel(agui, tools, "6 run_story_generation")
  Rel(tools, pipeline, "7 Async pipeline")
  Rel(pipeline, artifacts, "8 Writes artefacts")
  Rel(tools, agui, "9 STATE_DELTA progress")
  Rel(agui, ck_route, "10 SSE to client")
  Rel(studio_web, rest, "11 GET manuscript pdf")
  Rel(rest, artifacts, "12 Reads files")
```

- **Generative UI:** `StudioState` (slug, steps, errors) via AG-UI `STATE_SNAPSHOT` / `STATE_DELTA`; manuscript body loaded from REST, not stuffed into state.
- **Threads:** `StudioAgentRunner` persists CopilotKit threads under `.data/studio-threads/` (`AGENTIC_WRITER_THREADS_DIR`).
- **Long runs:** `StudioProgressBridge` streams step updates while `run_story_generation` is still running.

### Dynamic — Pipeline steps (C4Dynamic)

Same labels as `pipeline_steps.py` (CLI logs, Studio checklist, BDD).

```mermaid
C4Dynamic
  title Story pipeline - steps dynamic

  Container_Boundary(pipe, "Story Pipeline") {
    Component(orchestrator, "Orchestrator", "Python", "run_pipeline")
    Component(brief, "Brief", "models.Brief", "slug pitch format lang")
    Component(writer, "Writer", "Pydantic AI", "twist_sheet and draft")
    Component(editor, "Editor", "Pydantic AI", "review and final md")
    Component(io, "Artifacts IO", "io.py", "persist markdown")
    Component(export, "Print export", "docx_build", "docx and pdf")
  }
  ContainerDb(artifacts, "Artifacts store", "filesystem", "output per slug")

  Rel(orchestrator, brief, "1 Validate brief")
  Rel(brief, writer, "2 Writer agent")
  Rel(writer, editor, "3 Editor agent")
  Rel(editor, io, "4 Save artefacts")
  Rel(io, export, "5 Print layout optional")
  Rel(export, artifacts, "6 Deliver docx and pdf")
  Rel(io, artifacts, "Writes md and json")
```

| Step | Code | Output (under `output/<slug>/`) |
|------|------|----------------------------------|
| Brief | `models.Brief`, `brief_io` | — |
| Writer | `agents/writer` + `skills/story-writer/` | `twist_sheet.json`, `draft_manuscript.md` |
| Editor | `agents/editor` + `skills/manuscript-editor/` | `review.md`, `manuscript_final.md` |
| Artefacts | `io.save_artifacts` | all markdown + JSON |
| Print | `docx_build` + `skills/print-layout/` | `<slug>.docx`, `<slug>.pdf` (skip with `--md-only`) |

### Repository map

| Path | Role |
|------|------|
| `src/agentic_writer/cli.py` | Typer commands (`generate`, `serve`, `doctor`) |
| `src/agentic_writer/pipeline.py` | Orchestrates Writer → Editor → export |
| `src/agentic_writer/agents/` | Pydantic AI writer & editor agents |
| `src/agentic_writer/api/app.py` | FastAPI app, CORS, REST + `/agui` |
| `src/agentic_writer/api/studio.py` | Studio agent + tools (`run_story_generation`) |
| `skills/story-writer/`, `skills/manuscript-editor/`, `skills/print-layout/` | Prompt/skill packs loaded by agents & docx |
| `web/components/` | Studio UI (chat, progress, manuscript, PDF tabs) |
| `web/lib/copilotkit-runtime.ts` | CopilotKit v2 handler → `HttpAgent` → `/agui` |
| `web/lib/studio-agent-runner.ts` | Thread list/messages + disk persistence |
| `specs/bdd/`, `tests/bdd/` | Gherkin scenarios + pytest-bdd |
| `NewBooks/output/` | Generated stories (gitignored) |
| `.data/studio-threads/` | Studio chat history (gitignored) |
| `docs/` | Static GitHub Pages landing |

### Deployment (C4Deployment)

GitHub Pages hosts static content only; the live Studio needs Node + Python hosts (or containers).

```mermaid
C4Deployment
  title Agentic Writer - deployment

  Deployment_Node(local, "Developer machine", "macOS or Linux") {
    Container(cli_local, "CLI", "uv", "agentic-writer generate")
    Container(web_local, "Studio Web", "Next.js dev", "localhost 3000")
    Container(api_local, "Studio API", "uvicorn", "localhost 8000")
    ContainerDb(disk_local, "Local disk", "filesystem", "output and studio-threads")
  }

  Deployment_Node(github, "GitHub") {
    Container(pages, "Project site", "GitHub Pages", "docs static landing")
  }

  Deployment_Node(cloud, "Cloud optional", "Vercel Render Fly") {
    Container(web_cloud, "Studio Web", "Node container", "CopilotKit API routes")
    Container(api_cloud, "Studio API", "Python container", "FastAPI and pipeline")
    ContainerDb(disk_cloud, "Persistent volume", "filesystem", "artefacts and threads")
  }

  System_Ext(openai, "OpenAI", "API")

  Rel(api_local, openai, "HTTPS")
  Rel(api_cloud, openai, "HTTPS")
  Rel(web_local, api_local, "HTTP")
  Rel(web_cloud, api_cloud, "HTTPS")
  Rel(api_local, disk_local, "read and write")
  Rel(api_cloud, disk_cloud, "read and write")
```

| Surface | Host | Notes |
|---------|------|--------|
| Landing | **GitHub Pages** (`docs/`) | Static overview only |
| Studio UI | **Node host** (local `npm run dev`, or Vercel/Netlify) | Needs `/api/copilotkit` API routes |
| Agent API | **Python host** (local `serve`, or container on Render/Fly/etc.) | `OPENAI_API_KEY` stays server-side |
| Full stack on Pages alone | Not supported | Pages cannot run FastAPI or Next.js server routes |

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

See [Architecture](#architecture) for the full component map. Top level:

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
