"use client";

import { useEffect, useState } from "react";
import { ManuscriptView } from "./ManuscriptView";
import { PdfView } from "./PdfView";

type Tab = "md" | "pdf";

export function DeliverablesTabs({
  slug,
  markdown,
  outputDir,
  pdfAvailable,
}: {
  slug?: string;
  markdown: string;
  outputDir?: string | null;
  pdfAvailable: boolean;
}) {
  const [tab, setTab] = useState<Tab>("md");

  useEffect(() => {
    if (pdfAvailable) {
      setTab("pdf");
    }
  }, [pdfAvailable]);

  if (!pdfAvailable) {
    return (
      <ManuscriptView markdown={markdown} slug={slug} outputDir={outputDir} />
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

      {tab === "pdf" && slug ? (
        <PdfView slug={slug} />
      ) : (
        <ManuscriptView markdown={markdown} slug={slug} outputDir={outputDir} />
      )}
    </div>
  );
}
