# Architecture diagrams (Mermaid C4)

Source files for the README architecture section. The **rendered** diagrams live in the root [`README.md`](../../README.md) as fenced `mermaid` blocks — GitHub renders those automatically.

| File | C4 level |
|------|----------|
| `01-system-context.mmd` | Context |
| `02-containers.mmd` | Container |
| `03-studio-api-components.mmd` | Component |
| `04-pipeline-components.mmd` | Component |
| `05-studio-dynamic.mmd` | Dynamic |
| `06-pipeline-steps-dynamic.mmd` | Dynamic |
| `07-deployment.mmd` | Deployment |

After editing a `.mmd` file, copy its contents into the matching mermaid fenced block in `README.md` (keep the first line, e.g. `C4Context`, unchanged).

Validate locally (optional): `npx @mermaid-js/mermaid-cli@11 -i 01-system-context.mmd -o /tmp/test.png`
