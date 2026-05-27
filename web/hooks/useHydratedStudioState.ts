"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import type { AbstractAgent } from "@ag-ui/client";
import type { StudioAgentState } from "../components/types";
import {
  fetchThreadStudioState,
  mergeStudioState,
} from "../lib/studio-thread-state";

/**
 * Merges live CopilotKit agent state with the last STATE_SNAPSHOT from disk
 * (via GET /api/copilotkit/threads/:id/state) so pipeline steps show when
 * reopening a thread from History.
 */
export function useHydratedStudioState(
  threadId: string,
  liveState: StudioAgentState,
  agent: AbstractAgent | null | undefined,
): StudioAgentState {
  const [persisted, setPersisted] = useState<StudioAgentState | null>(null);
  const wasRunning = useRef(false);
  const hydratedKey = useRef<string | null>(null);
  const isRunning = Boolean(agent?.isRunning);

  const load = useCallback(async () => {
    const state = await fetchThreadStudioState(threadId);
    setPersisted(state);
    return state;
  }, [threadId]);

  useEffect(() => {
    hydratedKey.current = null;
    setPersisted(null);
    void load();
  }, [threadId, load]);

  useEffect(() => {
    if (wasRunning.current && !isRunning) {
      void load();
    }
    wasRunning.current = isRunning;
  }, [isRunning, load]);

  const displayState = mergeStudioState(liveState, persisted, isRunning);

  useEffect(() => {
    if (isRunning) return;
    if (!persisted?.steps?.length) return;
    if (liveState.steps?.length) return;
    const key = `${threadId}:${persisted.steps.length}`;
    if (hydratedKey.current === key) return;
    hydratedKey.current = key;
    try {
      agent?.setState(
        mergeStudioState(liveState, persisted, false) as Record<string, unknown>,
      );
    } catch {
      /* displayState merge still applies */
    }
  }, [agent, isRunning, liveState, persisted, threadId]);

  return displayState;
}
