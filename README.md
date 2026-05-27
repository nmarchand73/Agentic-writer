# Agentic Writer

Automated **story pipeline** (Writer → Editor → markdown → **docx/pdf**). **CLI** runs it headlessly; **Studio** adds [CopilotKit](https://www.copilotkit.ai/) v2 + [AG-UI](https://docs.ag-ui.com/) generative UI (pipeline state, manuscript, PDF) over the same `run_pipeline()`.

**Site:** [nmarchand73.github.io/Agentic-writer](https://nmarchand73.github.io/Agentic-writer/) · **Repo diagrams:** [`docs/diagrams/`](docs/diagrams/)

---

## Architecture

One pipeline, two entry points: **CLI** (`generate`) and **Studio** (Next.js + FastAPI `/agui`). C4 views below render on [GitHub](https://github.com/nmarchand73/Agentic-writer); sources live in [`docs/diagrams/`](docs/diagrams/).

### System context

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

### Containers

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

Labels match `pipeline_steps.py` (CLI, Studio, BDD).

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

| Step | Output in `output/<slug>/` |
|------|----------------------------|
| Writer | `twist_sheet.json`, `draft_manuscript.md` |
| Editor | `review.md`, `manuscript_final.md` |
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
| `skills/` | story-writer, manuscript-editor, print-layout |
| `specs/bdd/`, `tests/bdd/` | Gherkin + pytest-bdd |
| `NewBooks/output/` | Generated stories (gitignored) |
| `.data/studio-threads/` | Studio chat history (gitignored) |

---

## Why this stack

**CopilotKit + AG-UI** — Standard SSE agent wire; generative UI via `StudioState` (`STATE_SNAPSHOT` / `STATE_DELTA`); Python agent + Next.js UI; persisted threads; progress streaming during long tools.

**BDD** — Executable specs in [`specs/bdd/`](specs/bdd/); CI markers (`bootstrap`, `unit`, `integration`, `ui`) run without OpenAI; one feature file per slice.

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
| `.env` | `OPENAI_API_KEY`, `OPENAI_MODEL`, `AGENTIC_WRITER_OUTPUT`, `AGENTIC_WRITER_THREADS_DIR` |
| `config.toml` | Default `format`, `lang`; `output.root` → `NewBooks/output/` |
| `web/.env.local` | `NEXT_PUBLIC_AGENTIC_WRITER_API`, `AGENTIC_WRITER_AGUI_URL` (default `http://127.0.0.1:8000`) |

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
| `--brief path.yaml` | YAML brief |
| `--md-only` | Skip docx/pdf |
| `-v` / `-q` | DEBUG / WARNING logs |

**Output:** `NewBooks/output/<slug>/` — markdown artefacts plus optional docx/pdf.

```bash
uv run agentic-writer generate --brief examples/briefs/flash-smoke.yaml --md-only
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

Open [http://localhost:3000](http://localhost:3000). **History** resumes chats from `.data/studio-threads/`.

---

## Tests

```bash
uv run pytest -m "bootstrap or unit or integration or ui"   # CI, no OpenAI
uv run pytest tests/bdd/                                    # all Gherkin
uv run pytest -m e2e                                        # live API
cd web && npm run build                                     # optional
```

Details: [`specs/bdd/README.md`](specs/bdd/README.md).

---

## Troubleshooting

| Issue | Check |
|-------|--------|
| `doctor` fails | `skills/story-writer/SKILL.md`, root `npm install` |
| No docx/pdf | Node + `docx`; or `--md-only` |
| No PDF | LibreOffice / `soffice` |
| Studio errors | `serve` up, `OPENAI_API_KEY`, `web/.env.local` |

Design notes: [`../doc/agentic-writer/plan.md`](../doc/agentic-writer/plan.md).
