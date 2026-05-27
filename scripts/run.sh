#!/usr/bin/env bash
# Start Agentic Writer Studio: FastAPI (AG-UI) + Next.js dev server.
# Usage:
#   ./scripts/run.sh              # run Studio (doctor check first)
#   ./scripts/run.sh --install    # uv/npm install, then run
#   ./scripts/run.sh --no-doctor  # skip doctor
#   ./scripts/run.sh --port 8000

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

API_PORT="${API_PORT:-8000}"
API_HOST="${API_HOST:-127.0.0.1}"
WEB_PORT="${WEB_PORT:-3000}"
RUN_INSTALL=false
RUN_DOCTOR=true

usage() {
  sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'
  echo ""
  echo "Options:"
  echo "  --install       Run uv sync, npm install (root + web) before start"
  echo "  --no-doctor     Skip agentic-writer doctor"
  echo "  --port PORT     API port (default: 8000)"
  echo "  -h, --help      Show this help"
  echo ""
  echo "Env: API_PORT, API_HOST, WEB_PORT"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --install) RUN_INSTALL=true ;;
    --no-doctor) RUN_DOCTOR=false ;;
    --port)
      shift
      API_PORT="${1:?--port requires a value}"
      ;;
    -h | --help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
  shift
done

need_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

need_cmd uv
need_cmd npm

PIDS=()

cleanup() {
  local pid
  for pid in "${PIDS[@]}"; do
    if kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null || true
    fi
  done
  wait 2>/dev/null || true
}

trap cleanup EXIT INT TERM

if [[ "$RUN_INSTALL" == true ]]; then
  echo "==> Installing dependencies..."
  uv sync --all-extras
  npm install
  npm install --prefix web
fi

if [[ ! -f .env ]]; then
  echo "Warning: .env not found. Copy .env.example and set OPENAI_API_KEY." >&2
fi

if [[ "$RUN_DOCTOR" == true ]]; then
  echo "==> Running doctor..."
  uv run agentic-writer doctor
fi

if [[ ! -f web/.env.local ]]; then
  echo "Tip: create web/.env.local with NEXT_PUBLIC_AGENTIC_WRITER_API and AGENTIC_WRITER_AGUI_URL (see README)." >&2
fi

echo "==> Starting API on http://${API_HOST}:${API_PORT} (AG-UI /agui)"
uv run agentic-writer serve --host "$API_HOST" --port "$API_PORT" &
PIDS+=($!)

echo "==> Starting Studio on http://127.0.0.1:${WEB_PORT}"
npm run dev --prefix web -- --port "$WEB_PORT" &
PIDS+=($!)

echo ""
echo "  Studio UI:  http://127.0.0.1:${WEB_PORT}"
echo "  API health: http://${API_HOST}:${API_PORT}/health"
echo "  AG-UI:      http://${API_HOST}:${API_PORT}/agui"
echo ""
echo "Press Ctrl+C to stop both servers."
echo ""

# wait -n needs bash 4.3+; macOS ships bash 3.2
wait
