# Architecture diagrams (Mermaid C4)

Editable sources for the [README](../../README.md) architecture section. Copy changes into the matching fenced `mermaid` block after editing.

| File | Diagram |
|------|---------|
| `01-system-context.mmd` | System context |
| `02-containers.mmd` | Containers |
| `03-studio-api-components.mmd` | Studio API components |
| `04-pipeline-components.mmd` | Story pipeline components |
| `05-studio-dynamic.mmd` | Studio generate flow |
| `06-pipeline-steps-dynamic.mmd` | Pipeline steps |
| `07-deployment.mmd` | Deployment |

Validate: `npx @mermaid-js/mermaid-cli@11 -i 01-system-context.mmd -o /tmp/test.png`
