"use client";

import { useCallback, useEffect, useState } from "react";

const STORAGE_KEY = "agentic_writer_active_thread_id";

function newThreadId(): string {
  return crypto.randomUUID();
}

function readStored(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(STORAGE_KEY);
}

export function useStudioThreadId() {
  const [threadId, setThreadIdState] = useState<string | null>(null);

  useEffect(() => {
    setThreadIdState(readStored() ?? newThreadId());
  }, []);

  const setThreadId = useCallback((id: string) => {
    localStorage.setItem(STORAGE_KEY, id);
    setThreadIdState(id);
  }, []);

  const startNewThread = useCallback(() => {
    const id = newThreadId();
    setThreadId(id);
    return id;
  }, [setThreadId]);

  return {
    threadId,
    ready: threadId !== null,
    setThreadId,
    startNewThread,
  };
}
