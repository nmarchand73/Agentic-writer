"use client";

import type { StudioAgentState } from "./types";

function formatK(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(2)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}k`;
  return String(n);
}

type UsageCostBarProps = {
  state: StudioAgentState;
  isRunning?: boolean;
};

export function UsageCostBar({ state, isRunning = false }: UsageCostBarProps) {
  const inTok = state.usage_input_tokens ?? 0;
  const outTok = state.usage_output_tokens ?? 0;
  const req = state.usage_requests ?? 0;
  const hasUsage = inTok > 0 || outTok > 0;
  const showPipelineUsage =
    isRunning || hasUsage || (state.steps?.some((s) => s.status === "running") ?? false);

  if (!showPipelineUsage) return null;

  const costUsd = state.estimated_cost_usd;
  const waiting = !hasUsage && isRunning;

  return (
    <section
      className="studio-card studio-usage-bar px-4 py-3"
      data-testid="usage-cost-bar"
      aria-live="polite"
      aria-label="Usage et coût LLM cumulés"
    >
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div>
          <p className="text-[10px] font-semibold uppercase tracking-widest text-[var(--studio-accent)]">
            Tokens &amp; coût
          </p>
          <p className="text-sm font-medium text-[var(--studio-fg)] mt-0.5">
            {waiting ? "Comptage en cours…" : "Cumul pipeline"}
          </p>
        </div>
        {costUsd != null && (
          <p className="text-lg font-bold tabular-nums text-[var(--studio-fg)]">
            ≈ ${costUsd.toFixed(4)}
          </p>
        )}
      </div>

      <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-xs font-mono text-[var(--studio-muted)]">
        <span>
          <span className="text-[var(--studio-fg)] font-semibold">{formatK(inTok)}</span>{" "}
          tokens entrée
        </span>
        <span>
          <span className="text-[var(--studio-fg)] font-semibold">{formatK(outTok)}</span>{" "}
          tokens sortie
        </span>
        {req > 0 && <span>{req} appel{req > 1 ? "s" : ""} LLM</span>}
        {costUsd == null && hasUsage && (
          <span className="text-amber-700 dark:text-amber-400">prix non estimé</span>
        )}
        {costUsd != null && (
          <span className="text-[var(--studio-muted)]">tarifs OpenAI (docs)</span>
        )}
      </div>

      {hasUsage && inTok + outTok > 0 && (
        <div className="mt-2.5 h-1.5 rounded-full bg-[var(--studio-elevated)] overflow-hidden">
          <div
            className="h-full rounded-full studio-progress-bar transition-all duration-500 ease-out"
            style={{
              width: `${Math.min(100, Math.round((outTok / (inTok + outTok)) * 100))}%`,
            }}
            title="Part des tokens en sortie"
          />
        </div>
      )}
    </section>
  );
}
