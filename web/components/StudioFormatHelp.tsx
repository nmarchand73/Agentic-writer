"use client";

import { FORMATS_UI_HINT, STORY_FORMAT_SPECS } from "../lib/story-formats";

export function StudioFormatHelp() {
  return (
    <details className="studio-card group" data-testid="studio-format-help">
      <summary className="cursor-pointer list-none px-4 py-2.5 border-b border-[var(--studio-border)] bg-[var(--studio-elevated)] flex items-center justify-between gap-2 [&::-webkit-details-marker]:hidden">
        <span className="text-xs font-medium text-[var(--studio-muted)]">
          📏 Formats livre — flash, nouvelle, novella
        </span>
        <span className="text-[10px] uppercase tracking-wide text-[var(--studio-muted)] group-open:hidden">
          Afficher
        </span>
        <span className="text-[10px] uppercase tracking-wide text-[var(--studio-muted)] hidden group-open:inline">
          Masquer
        </span>
      </summary>
      <div className="px-4 py-3 text-sm text-[var(--studio-fg)] space-y-3">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="text-[var(--studio-muted)] border-b border-[var(--studio-border)]">
                <th className="py-1.5 pr-3 font-medium">Format</th>
                <th className="py-1.5 pr-3 font-medium">Mots</th>
                <th className="py-1.5 pr-3 font-medium">Pages (A5)</th>
                <th className="py-1.5 font-medium">Usage</th>
              </tr>
            </thead>
            <tbody>
              {STORY_FORMAT_SPECS.map((spec) => (
                <tr
                  key={spec.key}
                  className="border-b border-[var(--studio-border)]/60 last:border-0"
                >
                  <td className="py-2 pr-3 align-top">
                    <code className="text-[11px] bg-[var(--studio-elevated)] px-1 py-0.5 rounded">
                      {spec.key}
                    </code>
                    {!spec.supported && (
                      <span className="ml-1 text-[10px] text-[var(--studio-muted)]">
                        bientôt
                      </span>
                    )}
                  </td>
                  <td className="py-2 pr-3 align-top whitespace-nowrap">{spec.words}</td>
                  <td className="py-2 pr-3 align-top whitespace-nowrap">{spec.pagesA5}</td>
                  <td className="py-2 align-top text-[var(--studio-muted)]">
                    {spec.description}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="text-xs text-[var(--studio-muted)] leading-relaxed">{FORMATS_UI_HINT}</p>
      </div>
    </details>
  );
}
