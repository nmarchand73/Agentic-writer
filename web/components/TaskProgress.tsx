"use client";

import type { PipelineStepState } from "./types";
import {
  pipelineHeadline,
  stepEmoji,
  stepStatusLabel,
} from "../lib/studio-ui";

export function TaskProgress({ steps }: { steps: PipelineStepState[] }) {
  if (!steps.length) return null;

  const completedCount = steps.filter((s) => s.status === "completed").length;
  const progressPct = Math.round((completedCount / steps.length) * 100);
  const runningIndex = steps.findIndex((s) => s.status === "running");
  const currentIndex =
    runningIndex >= 0
      ? runningIndex
      : steps.findIndex((s) => s.status === "pending");
  const allDone = completedCount === steps.length;

  return (
    <section
      data-testid="task-progress"
      className="studio-card overflow-hidden"
      aria-label="Progression du pipeline"
    >
      <div className="px-4 py-3 border-b border-[var(--studio-border)] flex flex-wrap items-end justify-between gap-2">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-[var(--studio-accent)]">
            Pipeline récit
          </p>
          <h2 className="text-base font-semibold text-[var(--studio-fg)] mt-0.5">
            {pipelineHeadline(completedCount, steps.length)}
          </h2>
        </div>
        <div className="text-right">
          <span className="text-2xl font-bold tabular-nums text-[var(--studio-fg)]">
            {progressPct}%
          </span>
          <p className="text-xs text-[var(--studio-muted)]">
            {completedCount}/{steps.length} étapes
          </p>
        </div>
      </div>

      <div className="px-4 pt-3 pb-1">
        <div className="h-2 rounded-full bg-[var(--studio-elevated)] overflow-hidden">
          <div
            className="h-full rounded-full studio-progress-bar transition-all duration-700 ease-out"
            style={{ width: `${progressPct}%` }}
          />
        </div>
      </div>

      <ol className="p-3 space-y-1.5">
        {steps.map((step, index) => {
          const isCompleted = step.status === "completed";
          const isRunning = step.status === "running";
          const isCurrent =
            step.status === "pending" && index === currentIndex;
          const statusHint = stepStatusLabel(step.status);

          return (
            <li
              key={`${index}-${step.description}`}
              className={`studio-step ${isRunning || isCurrent ? "studio-step-active" : ""} ${isCompleted ? "studio-step-done" : ""}`}
            >
              <span
                className={`studio-step-icon ${isRunning ? "studio-step-icon-pulse" : ""}`}
                aria-hidden
              >
                {isCompleted ? "✓" : stepEmoji(step.description)}
              </span>
              <div className="flex-1 min-w-0">
                <p
                  data-testid="task-step-text"
                  className={`text-sm font-medium leading-snug ${isCompleted ? "text-[var(--studio-muted)] line-through decoration-[var(--studio-border)]" : "text-[var(--studio-fg)]"}`}
                >
                  {step.description}
                </p>
                {statusHint && (isRunning || isCurrent) && (
                  <p className="text-xs text-[var(--studio-accent)] mt-0.5 font-medium">
                    {statusHint}
                  </p>
                )}
              </div>
              {isCompleted && (
                <span className="text-xs font-medium text-emerald-600 dark:text-emerald-400 shrink-0">
                  ✓
                </span>
              )}
            </li>
          );
        })}
      </ol>

      {allDone && (
        <p className="px-4 pb-3 text-center text-xs text-[var(--studio-muted)]">
          Tu peux respirer — la suite, c&apos;est la lecture ↓
        </p>
      )}
    </section>
  );
}
