"use client";

import ReactMarkdown from "react-markdown";

export function ManuscriptView({
  markdown,
  slug,
  outputDir,
  pdfHref,
}: {
  markdown: string;
  slug?: string;
  outputDir?: string | null;
  pdfHref?: string;
}) {
  const wordApprox = markdown.trim().split(/\s+/).length;

  return (
    <article
      data-testid="manuscript-view"
      className="studio-card overflow-hidden studio-manuscript"
    >
      <header className="px-4 py-3 border-b border-[var(--studio-border)] bg-[var(--studio-elevated)]">
        <div className="flex flex-wrap items-start justify-between gap-2">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-[var(--studio-accent)]">
              Lecture
            </p>
            <h2 className="text-base font-semibold text-[var(--studio-fg)] mt-0.5">
              Manuscrit final
            </h2>
            <p className="text-xs text-[var(--studio-muted)] mt-1">
              Spoiler : c&apos;est ton texte — pas un best-seller volé au rayon.
            </p>
          </div>
          <div className="flex flex-wrap gap-1.5 items-center">
            <span className="studio-file-chip">~{wordApprox.toLocaleString("fr-FR")} mots</span>
            {slug && <span className="studio-file-chip font-mono">{slug}</span>}
            {pdfHref && (
              <a
                href={pdfHref}
                target="_blank"
                rel="noopener noreferrer"
                className="studio-btn studio-btn-primary text-xs py-1 px-2.5"
              >
                PDF ↗
              </a>
            )}
          </div>
        </div>
        {outputDir && (
          <p className="mt-2 text-[10px] font-mono text-[var(--studio-muted)] truncate">
            {outputDir}
          </p>
        )}
      </header>
      <div className="studio-manuscript-body max-h-[min(65vh,40rem)] overflow-y-auto px-6 py-6">
        <ReactMarkdown>{markdown}</ReactMarkdown>
      </div>
    </article>
  );
}
