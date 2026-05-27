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
      return d.includes("print") || d.includes("docx") || d.includes("pdf");
    }) ?? false
  );
}

export function usePdf(agentState: StudioAgentState) {
  const [available, setAvailable] = useState(false);
  const [checking, setChecking] = useState(false);

  const slug = agentState.slug;
  const ready =
    Boolean(slug) &&
    hadPrintStep(agentState) &&
    (isPipelineComplete(agentState) || Boolean(agentState.output_dir));

  const url = slug ? pdfUrl(slug) : null;

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
  }, [ready, slug, url]);

  return { url, available, checking, ready: ready && hadPrintStep(agentState) };
}
