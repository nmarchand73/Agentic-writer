"use client";

import { useEffect, useState } from "react";
import { manuscriptUrl } from "../lib/studio-api";
import type { StudioAgentState } from "../components/types";

function isPipelineComplete(state: StudioAgentState): boolean {
  const steps = state.steps;
  if (!steps?.length) return false;
  return steps.every((s) => s.status === "completed");
}

export function useManuscript(agentState: StudioAgentState) {
  const [markdown, setMarkdown] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [fetchError, setFetchError] = useState<string | null>(null);

  const slug = agentState.slug;
  const ready =
    Boolean(slug) &&
    (isPipelineComplete(agentState) || Boolean(agentState.output_dir));

  useEffect(() => {
    if (!ready || !slug) {
      setMarkdown(null);
      setFetchError(null);
      return;
    }

    if (agentState.manuscript_md) {
      setMarkdown(agentState.manuscript_md);
      setFetchError(null);
      setLoading(false);
      return;
    }

    let cancelled = false;
    setLoading(true);
    setFetchError(null);

    fetch(manuscriptUrl(slug), { cache: "no-store" })
      .then(async (res) => {
        if (!res.ok) {
          throw new Error(`${res.status} ${res.statusText}`);
        }
        return res.text();
      })
      .then((text) => {
        if (!cancelled) {
          setMarkdown(text);
        }
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          setMarkdown(null);
          setFetchError(
            err instanceof Error ? err.message : "Impossible de charger le manuscrit",
          );
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [ready, slug, agentState.manuscript_md, agentState.output_dir]);

  return { markdown, loading, fetchError, ready };
}
