"use client";

import type { ReactNode } from "react";
import { STUDIO_TAGLINE } from "../lib/studio-ui";

type StudioHeaderProps = {
  trailing?: ReactNode;
};

export function StudioHeader({ trailing }: StudioHeaderProps) {
  return (
    <header className="studio-header shrink-0 border-b border-[var(--studio-border)] bg-[var(--studio-surface)]/80 backdrop-blur-md">
      <div className="max-w-5xl mx-auto px-5 py-4 flex flex-wrap items-center justify-between gap-3">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="studio-logo" aria-hidden>
              AW
            </span>
            <h1 className="text-lg font-semibold tracking-tight text-[var(--studio-fg)]">
              Agentic Writer
            </h1>
            <span className="studio-badge">Studio</span>
          </div>
          <p className="mt-1.5 text-sm text-[var(--studio-muted)] max-w-xl leading-snug">
            {STUDIO_TAGLINE}
          </p>
        </div>
        <div className="flex items-center gap-3 flex-wrap justify-end">
          {trailing}
          <div className="hidden sm:flex items-center gap-2 text-xs font-medium text-[var(--studio-muted)]">
            <span className="studio-pill">Writer</span>
            <span className="text-[var(--studio-border)]">→</span>
            <span className="studio-pill">Editor</span>
            <span className="text-[var(--studio-border)]">→</span>
            <span className="studio-pill studio-pill-accent">docx · pdf</span>
          </div>
        </div>
      </div>
    </header>
  );
}
