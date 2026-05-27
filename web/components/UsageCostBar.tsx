"use client";

import type { StudioAgentState } from "./types";

function formatK(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(2)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}k`;
  return String(n);
}

export function UsageCostBar({ state }: { state: StudioAgentState }) {
  const inTok = state.usage_input_tokens ?? 0;
  const outTok = state.usage_output_tokens ?? 0;
  if (inTok === 0 && outTok === 0) return null;

  const cost =
    state.estimated_cost_usd != null
      ? ` · ≈ $${state.estimated_cost_usd.toFixed(4)}`
      : "";

  return (
    <p
      className="text-xs font-mono text-[var(--studio-muted)] px-1"
      data-testid="usage-cost-bar"
    >
      Coût LLM cumulé : {formatK(inTok)} in / {formatK(outTok)} out
      {state.usage_requests ? ` · ${state.usage_requests} req` : ""}
      {cost}
    </p>
  );
}
