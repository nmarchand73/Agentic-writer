"use client";

import { useEffect, useState } from "react";
import { ManuscriptView } from "./ManuscriptView";
import { PdfView } from "./PdfView";

type Tab = "md" | "pdf";

export function DeliverablesTabs({
  slug,
  format,
  markdown,
  outputDir,
  pdfUrl: pdfHref,
  showPdfUi,
  pdfChecking,
}: {
  slug?: string;
  format?: string;
  markdown: string;
  outputDir?: string | null;
  pdfUrl?: string | null;
  showPdfUi: boolean;
  pdfChecking?: boolean;
}) {
  const [tab, setTab] = useState<Tab>("md");

  useEffect(() => {
    if (showPdfUi && pdfHref) {
      setTab("pdf");
    }
  }, [showPdfUi, pdfHref]);

  if (!showPdfUi || !pdfHref || !slug) {
    return (
      <ManuscriptView
        markdown={markdown}
        slug={slug}
        outputDir={outputDir}
        pdfHref={pdfHref ?? undefined}
      />
    );
  }

  return (
    <div className="space-y-3">
      <div
        className="inline-flex p-1 rounded-lg bg-[var(--studio-elevated)] border border-[var(--studio-border)]"
        role="tablist"
        aria-label="Format de lecture"
      >
        <button
          type="button"
          role="tab"
          aria-selected={tab === "pdf"}
          className={`studio-tab ${tab === "pdf" ? "studio-tab-active" : ""}`}
          onClick={() => setTab("pdf")}
        >
          📕 PDF
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={tab === "md"}
          className={`studio-tab ${tab === "md" ? "studio-tab-active" : ""}`}
          onClick={() => setTab("md")}
        >
          📝 Markdown
        </button>
      </div>

      {pdfChecking && tab === "pdf" && (
        <p className="text-xs text-center text-[var(--studio-muted)] py-1">
          Vérification du PDF…
        </p>
      )}

      {tab === "pdf" ? (
        <PdfView slug={slug} format={format} />
      ) : (
        <ManuscriptView
          markdown={markdown}
          slug={slug}
          outputDir={outputDir}
          pdfHref={pdfHref}
        />
      )}
    </div>
  );
}
