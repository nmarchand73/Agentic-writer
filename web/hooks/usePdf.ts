"use client";

import { useEffect, useState } from "react";
import { pdfUrl } from "../lib/studio-api";
import type { StudioAgentState } from "../components/types";

function isPipelineComplete(state: StudioAgentState): boolean {
  const steps = state.steps;
  if (!steps?.length) return false;
  return steps.every((s) => s.status === "completed");
}

function hadPrintStep(state: StudioAgentState): boolean {
  return (
    state.steps?.some((s) => {
      const d = s.description.toLowerCase();
      return (
        d.includes("print") ||
        d.includes("docx") ||
        d.includes("pdf") ||
        d.includes("layout")
      );
    }) ?? false
  );
}

/** Pipeline was run with docx/pdf export (not markdown-only). */
export function expectsPdfExport(state: StudioAgentState): boolean {
  if (state.md_only) return false;
  if (hadPrintStep(state)) return true;
  if (state.output_dir) return true;
  return false;
}

export function usePdf(agentState: StudioAgentState) {
  const [available, setAvailable] = useState(false);
  const [checking, setChecking] = useState(false);

  const slug = agentState.slug;
  const storyFormat = agentState.format;
  const url = slug ? pdfUrl(slug, storyFormat) : null;
  const exportExpected = expectsPdfExport(agentState);

  const ready =
    Boolean(slug) &&
    exportExpected &&
    (isPipelineComplete(agentState) || Boolean(agentState.output_dir));

  useEffect(() => {
    if (!ready || !slug || !url) {
      setAvailable(false);
      return;
    }

    let cancelled = false;
    setChecking(true);

    fetch(url, { method: "HEAD", cache: "no-store" })
      .then((res) => {
        if (!cancelled) {
          setAvailable(res.ok);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setAvailable(false);
        }
      })
      .finally(() => {
        if (!cancelled) {
          setChecking(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [ready, slug, storyFormat, url]);

  const showPdfUi = exportExpected && Boolean(slug) && (available || ready);

  return {
    url,
    available,
    checking,
    ready,
    exportExpected,
    showPdfUi,
  };
}
