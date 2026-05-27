"use client";

import { pdfUrl } from "../lib/studio-api";

export function PdfView({ slug }: { slug: string }) {
  const src = pdfUrl(slug);
  const downloadName = `${slug}.pdf`;

  return (
    <section
      data-testid="pdf-view"
      className="studio-card overflow-hidden"
      aria-label="Aperçu PDF"
    >
      <header className="px-4 py-3 border-b border-[var(--studio-border)] bg-[var(--studio-elevated)] flex flex-wrap items-center justify-between gap-2">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-[var(--studio-accent)]">
            Export imprimable
          </p>
          <h2 className="text-base font-semibold text-[var(--studio-fg)] mt-0.5">
            Version PDF — mise en page livre
          </h2>
          <p className="text-xs text-[var(--studio-muted)] mt-1">
            Aperçu tel qu&apos;exporté (A5, Palatino). Le navigateur peut mettre une
            seconde à afficher.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <a
            href={src}
            target="_blank"
            rel="noopener noreferrer"
            className="studio-btn studio-btn-ghost text-xs"
          >
            Ouvrir ↗
          </a>
          <a href={src} download={downloadName} className="studio-btn studio-btn-primary text-xs">
            Télécharger
          </a>
        </div>
      </header>
      <div className="bg-[var(--studio-elevated)] p-2 sm:p-3">
        <iframe
          title={`PDF ${slug}`}
          src={src}
          className="w-full rounded-lg border border-[var(--studio-border)] bg-white dark:bg-slate-900"
          style={{ height: "min(70vh, 42rem)" }}
        />
      </div>
    </section>
  );
}
