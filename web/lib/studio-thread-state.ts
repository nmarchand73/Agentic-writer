import type { PipelineStepState, StudioAgentState } from "../components/types";

const COPILOT_BASE = "/api/copilotkit";

function isStepStatus(v: unknown): v is PipelineStepState["status"] {
  return v === "pending" || v === "running" || v === "completed";
}

function parseSteps(raw: unknown): PipelineStepState[] | undefined {
  if (!Array.isArray(raw)) return undefined;
  const steps: PipelineStepState[] = [];
  for (const item of raw) {
    if (!item || typeof item !== "object") continue;
    const row = item as Record<string, unknown>;
    if (typeof row.description !== "string") continue;
    const status = row.status;
    steps.push({
      description: row.description,
      status: isStepStatus(status) ? status : "pending",
    });
  }
  return steps.length > 0 ? steps : undefined;
}

/** Parse runner GET /threads/:id/state payload into StudioAgentState. */
export function parseStudioAgentState(raw: unknown): StudioAgentState | null {
  if (!raw || typeof raw !== "object") return null;
  const o = raw as Record<string, unknown>;
  const steps = parseSteps(o.steps);
  const state: StudioAgentState = {};
  if (typeof o.slug === "string") state.slug = o.slug;
  if (typeof o.pitch === "string") state.pitch = o.pitch;
  if (typeof o.format === "string") state.format = o.format;
  if (typeof o.lang === "string") state.lang = o.lang;
  if (typeof o.md_only === "boolean") state.md_only = o.md_only;
  if (steps) state.steps = steps;
  if (typeof o.output_dir === "string") state.output_dir = o.output_dir;
  if (o.output_dir === null) state.output_dir = null;
  if (typeof o.manuscript_preview === "string") state.manuscript_preview = o.manuscript_preview;
  if (typeof o.manuscript_md === "string") state.manuscript_md = o.manuscript_md;
  if (typeof o.error === "string") state.error = o.error;
  if (o.error === null) state.error = null;
  if (typeof o.usage_input_tokens === "number") {
    state.usage_input_tokens = o.usage_input_tokens;
  }
  if (typeof o.usage_output_tokens === "number") {
    state.usage_output_tokens = o.usage_output_tokens;
  }
  if (typeof o.usage_requests === "number") {
    state.usage_requests = o.usage_requests;
  }
  if (typeof o.estimated_cost_usd === "number") {
    state.estimated_cost_usd = o.estimated_cost_usd;
  }
  if (o.estimated_cost_usd === null) state.estimated_cost_usd = null;
  if (Object.keys(state).length === 0 && !steps) return null;
  return state;
}

export async function fetchThreadStudioState(
  threadId: string,
): Promise<StudioAgentState | null> {
  try {
    const res = await fetch(
      `${COPILOT_BASE}/threads/${encodeURIComponent(threadId)}/state`,
    );
    if (!res.ok) return null;
    const data = (await res.json()) as { state?: unknown };
    return parseStudioAgentState(data.state);
  } catch {
    return null;
  }
}

/** Prefer live agent state while running; otherwise fill gaps from persisted snapshot. */
export function mergeStudioState(
  live: StudioAgentState,
  persisted: StudioAgentState | null,
  isRunning: boolean,
): StudioAgentState {
  if (isRunning) return live;
  if (live.steps?.length) return live;
  if (!persisted) return live;
  return {
    ...persisted,
    ...live,
    steps: persisted.steps?.length ? persisted.steps : live.steps,
    slug: live.slug ?? persisted.slug,
    pitch: live.pitch ?? persisted.pitch,
    output_dir: live.output_dir ?? persisted.output_dir,
    error: live.error ?? persisted.error,
    usage_input_tokens: live.usage_input_tokens ?? persisted.usage_input_tokens,
    usage_output_tokens: live.usage_output_tokens ?? persisted.usage_output_tokens,
    usage_requests: live.usage_requests ?? persisted.usage_requests,
    estimated_cost_usd: live.estimated_cost_usd ?? persisted.estimated_cost_usd,
  };
}
