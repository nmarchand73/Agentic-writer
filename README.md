# Agentic Writer

**Pipeline récit** : **Writer** (`story-writer`) → **Editor** (`manuscript-editor`) → artefacts markdown → **Print layout** (`print-layout`, calqué `twilight-zone-novelist`) → docx / pdf A5 Palatino.

Plan détaillé : [`../doc/agentic-writer/plan.md`](../doc/agentic-writer/plan.md)

## Setup

```bash
cd Agentic-writer
uv sync --all-extras
cp .env.example .env   # OPENAI_API_KEY, OPENAI_MODEL (ex. openai-chat:gpt-4o)
npm install            # dans Agentic-writer/ — requis pour l’export docx (package docx)
uv run agentic-writer doctor
```

## Logs (CLI)

Logging via [loguru](https://github.com/Delgan/loguru) sur stderr :

```bash
uv run agentic-writer -v generate ...    # DEBUG
uv run agentic-writer generate ...       # INFO (défaut)
uv run agentic-writer -q generate ...    # WARNING+
LOG_LEVEL=DEBUG uv run agentic-writer generate ...
```

Le pipeline affiche un plan numéroté puis chaque étape en direct, par ex. `[2/5] ▶ Writer — fiche twist + brouillon` puis `[2/5] ✓ …`.

## CLI — exemples (mystère / UAP)

### Vérifier l'environnement

```bash
uv run agentic-writer doctor
```

### Nouvelle — radar & disparition

```bash
uv run agentic-writer generate dossier-lumiere-noire \
  --pitch "Contrôleuse radar civile voit un blip UAP qui épouse sa route ; son mari jure qu'elle n'est jamais rentrée cette nuit-là." \
  --format nouvelle \
  --lang fr
```

Artefacts : `NewBooks/output/dossier-lumiere-noire/`

### Flash — signal satellite

```bash
uv run agentic-writer generate signal-77 \
  --pitch "Technicienne satellite capte une formation non cataloguée ; une voix de secours prononce le prénom de sa mère morte." \
  --format flash \
  --lang fr \
  --md-only
```

### Brief YAML (reproductible)

```bash
uv run agentic-writer generate --brief examples/briefs/dossier-lumiere-noire.yaml
uv run agentic-writer generate --brief examples/briefs/flash-smoke.yaml --md-only
```

Exemple de brief (`examples/briefs/dossier-lumiere-noire.yaml`) :

```yaml
slug: dossier-lumiere-noire
pitch: "Contrôleuse radar voit un blip UAP qui épouse sa route ; personne ne la voit rentrer."
format: nouvelle
lang: fr
theme: mystère / UAP
```

### Smoke test CI (sans appel API)

```bash
uv run pytest -m "bootstrap or unit or integration or ui"
# persistance threads Studio (BDD 07, nécessite Node/npx pour le runner TS)
uv run pytest tests/bdd/test_studio_threads.py -m ui
```

## Studio web — exemples

Interface CopilotKit avec **Task Progress** (étapes Writer → Editor → export en direct).

### Démarrage

```bash
# Terminal 1 — backend AG-UI (Pydantic AI)
export OPENAI_API_KEY=sk-...
uv run agentic-writer serve --port 8000

# Terminal 2 — frontend Next.js
cd web && npm install && npm run dev
# → http://localhost:3000
```

Le chat propose des **suggestions préconfigurées** (UAP, hangar scellé, archives, triangle noir, etc.).

### Messages types (équivalents CLI)

| Objectif | Message dans le chat |
|----------|----------------------|
| Flash UAP | `Génère une flash slug "signal-77" — pitch: formation lumineuse non cataloguée, voix de secours avec le prénom de sa mère morte.` |
| Nouvelle radar | `Génère slug "dossier-lumiere-noire", format nouvelle — pitch: blip UAP sur sa route ; personne ne la voit rentrer.` |
| Hangar scellé | `Génère slug "hangar-scelle" — pitch: base désaffectée, hangar de 1989 ouvert de l'intérieur, silhouette avec son badge actuel.` |
| Flash EN | `Generate flash "black-triangle" — pitch: black triangle over suburb; school says Mom already picked up her daughter.` |

L’agent crée d’abord le plan d’étapes (`STATE_SNAPSHOT`), puis lance le pipeline et met à jour chaque étape (`STATE_DELTA`) pendant l’exécution.

Configuration runtime : `useSingleEndpoint={false}` côté React (routes REST `/info`, `/threads`, `/agent/.../run`).

### Historique des conversations (mémoire niveau 2)

Les chats Studio sont **persistés sur disque** dans `.data/studio-threads/` (un fichier JSON par conversation). Ils survivent au redémarrage de `npm run dev`.

- Bouton **Historique** (en-tête) : reprendre une conversation passée ou en ouvrir une nouvelle.
- Variable optionnelle : `AGENTIC_WRITER_THREADS_DIR` (chemin absolu du dossier de stockage).

## Tests

```bash
uv run pytest -m "bootstrap or unit or integration or ui"
uv run pytest -m e2e   # requires OPENAI_API_KEY
```
