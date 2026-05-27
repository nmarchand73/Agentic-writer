"use client";

import { useThreads, type Thread } from "@copilotkit/react-core/v2";
import { useCallback, useState } from "react";

const AGENT_ID = "agentic_writer_studio";

function formatThreadDate(thread: Thread): string {
  const raw = thread.lastRunAt ?? thread.updatedAt;
  try {
    return new Date(raw).toLocaleString("fr-FR", {
      day: "numeric",
      month: "short",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return "";
  }
}

type StudioThreadPanelProps = {
  activeThreadId: string | null;
  onSelectThread: (threadId: string) => void;
  onNewThread: () => void;
};

export function StudioThreadPanel({
  activeThreadId,
  onSelectThread,
  onNewThread,
}: StudioThreadPanelProps) {
  const { threads, isLoading, error } = useThreads({ agentId: AGENT_ID });
  const [open, setOpen] = useState(false);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const handleDelete = useCallback(
    async (threadId: string, e: React.MouseEvent) => {
      e.stopPropagation();
      if (!confirm("Supprimer cette conversation ? (irréversible)")) return;
      setDeletingId(threadId);
      try {
        await fetch(`/api/studio/threads/${encodeURIComponent(threadId)}`, {
          method: "DELETE",
        });
        if (threadId === activeThreadId) onNewThread();
        window.location.reload();
      } catch {
        /* ignore */
      } finally {
        setDeletingId(null);
      }
    },
    [activeThreadId, onNewThread],
  );

  const label =
    threads.find((t) => t.id === activeThreadId)?.name?.trim() || "Conversation";

  return (
    <div className="relative">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="studio-thread-trigger"
        aria-expanded={open}
        aria-haspopup="listbox"
        title="Historique des conversations"
      >
        <span className="studio-thread-trigger-icon" aria-hidden>
          🕐
        </span>
        <span className="max-w-[140px] truncate">{label}</span>
        <span className="text-[10px] opacity-70" aria-hidden>
          {open ? "▲" : "▼"}
        </span>
      </button>

      {open && (
        <>
          <button
            type="button"
            className="fixed inset-0 z-30 cursor-default"
            aria-label="Fermer l'historique"
            onClick={() => setOpen(false)}
          />
          <div className="studio-thread-dropdown" role="listbox">
            <div className="flex items-center justify-between gap-2 px-3 py-2 border-b border-[var(--studio-border)]">
              <p className="text-xs font-semibold text-[var(--studio-fg)]">Historique</p>
              <button
                type="button"
                className="text-xs font-medium text-[var(--studio-accent)] hover:underline"
                onClick={() => {
                  onNewThread();
                  setOpen(false);
                }}
              >
                + Nouvelle
              </button>
            </div>

            {isLoading && (
              <p className="px-3 py-4 text-xs text-[var(--studio-muted)]">Chargement…</p>
            )}
            {error && (
              <p className="px-3 py-4 text-xs text-red-600">
                Impossible de charger l&apos;historique.
              </p>
            )}
            {!isLoading && !error && threads.length === 0 && (
              <p className="px-3 py-4 text-xs text-[var(--studio-muted)]">
                Aucune conversation enregistrée. Lance un brief pour commencer.
              </p>
            )}

            <ul className="max-h-64 overflow-y-auto py-1">
              {threads.map((thread) => {
                const active = thread.id === activeThreadId;
                return (
                  <li key={thread.id} className="studio-thread-row">
                    <button
                      type="button"
                      role="option"
                      aria-selected={active}
                      className={`studio-thread-item flex-1 min-w-0 text-left ${active ? "studio-thread-item-active" : ""}`}
                      onClick={() => {
                        onSelectThread(thread.id);
                        setOpen(false);
                      }}
                    >
                      <span className="block text-sm font-medium truncate">
                        {thread.name?.trim() || "Sans titre"}
                      </span>
                      <span className="block text-[10px] text-[var(--studio-muted)] mt-0.5">
                        {formatThreadDate(thread)}
                      </span>
                    </button>
                    <button
                      type="button"
                      className="studio-thread-delete shrink-0"
                      title="Supprimer"
                      disabled={deletingId === thread.id}
                      onClick={(e) => void handleDelete(thread.id, e)}
                    >
                      ×
                    </button>
                  </li>
                );
              })}
            </ul>

            <p className="px-3 py-2 text-[10px] text-[var(--studio-muted)] border-t border-[var(--studio-border)]">
              Sauvegardé dans <code className="text-[9px]">.data/studio-threads/</code>
            </p>
          </div>
        </>
      )}
    </div>
  );
}
