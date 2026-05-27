# Agentic Writer

Automated **editorial story pipeline**: plan twists and chapters, write **chapter by chapter**, edit, adversarial audit, then **docx/pdf**. Same `run_pipeline()` for **CLI** (`generate`) and **Studio** ([CopilotKit](https://www.copilotkit.ai/) + [AG-UI](https://docs.ag-ui.com/) — live steps, manuscript preview, thread history).

**Site:** [nmarchand73.github.io/Agentic-writer](https://nmarchand73.github.io/Agentic-writer/) · **Design notes:** [`../doc/agentic-writer/plan.md`](../doc/agentic-writer/plan.md) · **Diagram sources:** [`docs/diagrams/`](docs/diagrams/)

### Pipeline (single path)

```text
Brief → Architecte (twist + plan) → Chapitres (story-writer) → Editor → Auditeur → artefacts → docx/pdf
```

| Format | Chapitres planifiés | Mots cibles (garde-fous) |
|--------|---------------------|---------------------------|
| `flash` | 1 + prologue | 600–2 500 |
| `nouvelle` | 7 + prologue | 7 000–16 000 |
| `novella` | 16 + prologue | 28 000–52 000 |

```bash
uv run agentic-writer formats   # full table (A5 pages, CLI hints)
```

---

## Architecture

One pipeline, two entry points: **CLI** (`generate`) and **Studio** (Next.js + FastAPI `/agui`). C4 views below render on [GitHub](https://github.com/nmarchand73/Agentic-writer); sources live in [`docs/diagrams/`](docs/diagrams/).

### System context

```mermaid
C4Context
  title Agentic Writer - system context

  Person(author, "Author", "Generates fiction via CLI or Studio")
  System(aw, "Agentic Writer", "Editorial pipeline, docx and pdf export, optional Studio UI")
  System_Ext(openai, "OpenAI", "LLM for architect chapter writer editor auditor")
  SystemDb_Ext(pages, "GitHub Pages", "Static project landing in docs")
  SystemDb(output, "Output store", "Manuscripts and exports per slug")

  Rel(author, aw, "Runs generate and Studio chat")
  Rel(aw, openai, "Calls", "HTTPS API")
  Rel(aw, output, "Reads and writes artefacts")
  Rel(author, pages, "Reads overview", "HTTPS")
```

### Containers

```mermaid
C4Container
  title Agentic Writer - containers

  Person(author, "Author", "CLI user or Studio user")

  System_Boundary(aw, "Agentic Writer") {
    Container(cli, "CLI", "Python Typer", "generate serve doctor")
    Container(studio_web, "Studio Web", "Next.js", "React UI CopilotKit threads")
    Container(studio_api, "Studio API", "FastAPI", "agui REST manuscript pdf")
    Container(pipeline, "Story Pipeline", "Python", "run_pipeline architect chapters editor auditor export")
    ContainerDb(artifacts, "Artifacts store", "filesystem", "output per slug")
    ContainerDb(threads, "Thread store", "filesystem", "studio-threads folder")
  }

  System_Ext(openai, "OpenAI", "Chat completions API")

  Rel(author, cli, "Runs", "shell")
  Rel(author, studio_web, "Uses", "HTTPS")
  Rel(cli, pipeline, "Invokes")
  Rel(studio_web, studio_api, "AG-UI and REST", "HTTP SSE")
  Rel(studio_api, pipeline, "run_story_generation tool")
  Rel(pipeline, openai, "Architect chapter writer editor auditor agents")
  Rel(pipeline, artifacts, "Writes twist md docx pdf")
  Rel(studio_api, artifacts, "Serves manuscript and pdf")
  Rel(studio_web, threads, "Persists threads")
```

<details>
<summary>More diagrams (components, flows, deployment)</summary>

### Studio API components

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

### Story pipeline components

```mermaid
C4Component
  title Story pipeline - components

  Container(cli, "CLI", "Typer", "Headless entry")
  Container(studio_agent, "Studio agent", "Pydantic AI", "Studio entry via tools")
  System_Ext(openai, "OpenAI", "LLM")
  ContainerDb(artifacts, "Artifacts store", "filesystem", "Per-slug folder")

  Container_Boundary(pipe, "Story Pipeline") {
    Component(orchestrator, "Pipeline orchestrator", "pipeline.py", "run_pipeline step hooks")
    Component(architect, "Architect agent", "Pydantic AI", "story-architect skill")
    Component(chapters, "Chapter writer", "Pydantic AI", "story-writer per chapter")
    Component(editor, "Editor agent", "Pydantic AI", "manuscript-editor skill")
    Component(auditor, "Auditor agent", "Pydantic AI", "story-auditor skill")
    Component(io, "Artifacts IO", "io.py", "Save twist blueprint chapters audit md")
    Component(export, "Print export", "docx_build", "print-layout docx and pdf")
  }

  Rel(cli, orchestrator, "generate command")
  Rel(studio_agent, orchestrator, "run_story_generation tool")
  Rel(orchestrator, architect, "Plan")
  Rel(architect, chapters, "Write chapters")
  Rel(chapters, editor, "Assemble and edit")
  Rel(editor, auditor, "Audit and optional rewrite")
  Rel(auditor, io, "Persist")
  Rel(io, export, "Print optional")
  Rel(architect, openai, "LLM")
  Rel(chapters, openai, "LLM")
  Rel(editor, openai, "LLM")
  Rel(auditor, openai, "LLM")
  Rel(io, artifacts, "Writes")
  Rel(export, artifacts, "Writes docx and pdf")
```

### Studio generate (runtime)

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

### Pipeline steps

Labels match `pipeline_steps.py` (CLI logs, Studio `TaskProgress`, BDD).

```mermaid
C4Dynamic
  title Story pipeline - steps dynamic

  Container_Boundary(pipe, "Story Pipeline") {
    Component(orchestrator, "Orchestrator", "Python", "run_pipeline")
    Component(brief, "Brief", "models.Brief", "slug pitch format lang")
    Component(architect, "Architect", "Pydantic AI", "blueprint and twist_sheet")
    Component(chapters, "Chapter writer", "Pydantic AI", "one LLM call per chapter")
    Component(editor, "Editor", "Pydantic AI", "review and final md")
    Component(auditor, "Auditor", "Pydantic AI", "audit optional chapter rewrite")
    Component(io, "Artifacts IO", "io.py", "persist markdown json")
    Component(export, "Print export", "docx_build", "docx and pdf")
  }
  ContainerDb(artifacts, "Artifacts store", "filesystem", "output per slug")

  Rel(orchestrator, brief, "1 Validate brief")
  Rel(brief, architect, "2 Architect")
  Rel(architect, chapters, "3 Chapters")
  Rel(chapters, editor, "4 Editor")
  Rel(editor, auditor, "5 Auditor")
  Rel(auditor, io, "6 Save artefacts")
  Rel(io, export, "7 Print layout optional")
  Rel(export, artifacts, "8 Deliver docx and pdf")
  Rel(io, artifacts, "Writes md and json")
```

| Phase | Output in `output/<slug>/` |
|-------|----------------------------|
| Architecte | `blueprint.json`, `twist_sheet.json` |
| Chapitres | `chapters/*.md`, `draft_manuscript.md` (assemblé) |
| Editor | `review.md`, `manuscript_final.md` |
| Auditeur | `audit_report.md` |
| Print | `<slug>.docx`, `<slug>.pdf` (omit with `--md-only`) |

### Deployment

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

GitHub Pages = static `docs/` only. Live Studio needs **Node** (web) + **Python** (API); `OPENAI_API_KEY` stays on the API host.

</details>

### Key paths

| Path | Role |
|------|------|
| `src/agentic_writer/` | CLI, pipeline, agents, FastAPI studio |
| `web/` | Next.js Studio, CopilotKit runtime |
| `skills/` | story-architect, story-writer, manuscript-editor, story-auditor, print-layout |
| `specs/bdd/`, `tests/bdd/` | Gherkin + pytest-bdd |
| `NewBooks/output/` | Generated stories (gitignored) |
| `.data/studio-threads/` | Studio chat history (gitignored) |

---

## Why this stack

**Editorial pipeline** — Twist and chapter plan before prose; one LLM call per chapter (length targets per format); adversarial audit with optional targeted rewrite; programmatic guards on word count and `TwistSheet`.

**CopilotKit + AG-UI** — SSE agent wire; generative UI via `StudioState` (`STATE_SNAPSHOT` / `STATE_DELTA`); live `TaskProgress`; **thread persistence** and **state hydration** when reopening History (pipeline steps restored from disk).

**BDD** — Executable specs in [`specs/bdd/`](specs/bdd/); CI (`bootstrap`, `unit`, `integration`, `ui`) without OpenAI; **e2e** live runs use **`format=flash`** and `--md-only` only.

---

## Prerequisites

- **uv** + Python ≥ 3.10
- **Node.js** ≥ 18
- **OpenAI API key** (generate / Studio; not for mocked tests)
- **LibreOffice** (`soffice`) — PDF only (or `--md-only`)

---

## Install

```bash
cd Agentic-writer
uv sync --all-extras
npm install && cd web && npm install && cd ..
cp .env.example .env     # set OPENAI_API_KEY
uv run agentic-writer doctor
```

---

## Configuration

| File | Purpose |
|------|---------|
| `.env` | `OPENAI_API_KEY`, default `OPENAI_MODEL`, optional `OPENAI_MODEL_*` per role (see below) |
| `.env` | `AGENTIC_WRITER_OUTPUT`, `AGENTIC_WRITER_THREADS_DIR`, `AGENTIC_WRITER_MAX_AUDIT_RETRIES` |
| `config.toml` | Default `format`, `lang`; `output.root`; `[pipeline] max_audit_retries`; optional `[models]` |
| `web/.env.local` | `NEXT_PUBLIC_AGENTIC_WRITER_API` (default `http://127.0.0.1:8000`) |

**Models per role** (all fall back to `OPENAI_MODEL` if unset):

| Variable | Agent |
|----------|--------|
| `OPENAI_MODEL_ARCHITECT` | Plan + `twist_sheet` |
| `OPENAI_MODEL_CHAPTER` | Chapter prose (`story-writer`) |
| `OPENAI_MODEL_EDITOR` | Review |
| `OPENAI_MODEL_AUDITOR` | Adversarial audit |

Tip: use a stronger model for Architect/Chapter and a cheaper one for Auditor (e.g. `gpt-4.1-mini` + `gpt-4.1-nano`).

---

## Run — CLI

| Command | Purpose |
|---------|---------|
| `doctor` | Python, Node, skills (incl. architect + auditor), docx toolchain |
| `formats` | Word counts and A5 page targets per format |
| `generate` | Full editorial pipeline |
| `serve` | FastAPI Studio API (`/agui`, `/manuscript`, `/pdf`) |
| `eval` | Regression hook (`AGENTIC_WRITER_EVAL_MODE=mock` in CI) |

```bash
uv run agentic-writer generate <slug> \
  --pitch "Your pitch." \
  --format nouvelle \
  --lang fr
```

| `generate` flag | Purpose |
|-----------------|---------|
| `--format` | `flash` \| `nouvelle` \| `novella` |
| `--brief path.yaml` | YAML brief (overrides slug/pitch argv) |
| `--md-only` | Skip docx/pdf |
| `-v` / `-q` | DEBUG / WARNING logs |

**Output:** `NewBooks/output/<slug>/` (or `AGENTIC_WRITER_OUTPUT`).

```bash
# Quick smoke (fewer LLM calls)
uv run agentic-writer generate smoke --pitch "…" --format flash --md-only

uv run agentic-writer generate --brief examples/briefs/flash-smoke.yaml
```

---

## Run — Studio

One script starts the API and the Next.js UI (Ctrl+C stops both):

```bash
./scripts/run.sh
# or: npm run studio
# first time: ./scripts/run.sh --install
```

Manual split (two terminals):

```bash
uv run agentic-writer serve --port 8000
cd web && npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

- **History** — persisted under `.data/studio-threads/`; pipeline step state rehydrated when you reopen a thread.
- **Formats livre** — collapsible table (`flash` / `nouvelle` / `novella`) above the chat.
- Chat: describe slug, pitch, format, and lang; the studio agent calls `create_pipeline_plan` then `run_story_generation`.

---

## Tests

```bash
uv run pytest -m "bootstrap or unit or integration or ui"   # CI, no OpenAI
uv run pytest tests/bdd/                                    # all Gherkin
uv run pytest -m e2e                                        # live API, format flash, --md-only
cd web && npm run build                                     # optional
```

Details: [`specs/bdd/README.md`](specs/bdd/README.md).

---

## Troubleshooting

| Issue | Check |
|-------|--------|
| `doctor` fails | `skills/story-writer`, `story-architect`, `story-auditor`, `print-layout`; root `npm install` |
| Pipeline steps empty in History | Reopen thread after a completed run; check `GET /api/copilotkit/threads/:id/state` |
| No docx/pdf | Node + `docx`; or `--md-only` |
| No PDF | LibreOffice / `soffice` |
| Studio errors | `serve` up, `OPENAI_API_KEY`, `web/.env.local` |
| High API cost | Prefer `--format flash`; tune per-role models in `.env` |
