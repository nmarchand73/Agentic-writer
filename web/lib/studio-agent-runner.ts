/**
 * Runner CopilotKit avec persistance disque (niveau 2).
 * Étend InMemoryAgentRunner pour rester compatible avec les handlers GET /threads.
 */
import { InMemoryAgentRunner } from "@copilotkit/runtime/v2";
import type {
  AgentRunnerConnectRequest,
  AgentRunnerRunRequest,
} from "@copilotkit/runtime/v2";
import { compactEvents, EventType, type BaseEvent, type Message } from "@ag-ui/client";
import { Observable, ReplaySubject } from "rxjs";
import {
  clearThreadFiles,
  deleteThreadFile,
  listStoredThreads,
  loadThread,
  resolveThreadsDir,
  saveThread,
  threadDisplayName,
  type StoredThread,
} from "./thread-persistence";

function snapshotFromRunner(
  runner: InMemoryAgentRunner,
  threadId: string,
): StoredThread | null {
  const events = runner.getThreadEvents(threadId);
  if (events.length === 0) return null;
  const messages = runner.getThreadMessages(threadId);
  const listed = runner.listThreads().find((t) => t.id === threadId);
  return {
    threadId,
    name: listed?.name ?? null,
    historicRuns: [
      {
        threadId,
        runId: "snapshot",
        agentId: listed?.agentId ?? "agentic_writer_studio",
        parentRunId: null,
        events,
        messages,
        createdAt: listed ? new Date(listed.updatedAt).getTime() : Date.now(),
      },
    ],
  };
}

function loadDiskSnapshot(persistDir: string, threadId: string): StoredThread | null {
  return loadThread(persistDir, threadId);
}

function diskEvents(data: StoredThread): BaseEvent[] {
  const all: BaseEvent[] = [];
  for (const run of data.historicRuns) all.push(...run.events);
  return compactEvents(all);
}

function diskMessages(data: StoredThread): Message[] {
  if (data.historicRuns.length === 0) return [];
  return data.historicRuns[data.historicRuns.length - 1].messages;
}

type JsonPatchOp = { op: string; path: string; value?: unknown };

function applyStateDelta(
  state: Record<string, unknown>,
  rawDelta: unknown,
): Record<string, unknown> {
  const ops: JsonPatchOp[] = Array.isArray(rawDelta)
    ? (rawDelta as JsonPatchOp[])
    : [rawDelta as JsonPatchOp];
  const next: Record<string, unknown> = { ...state };
  const steps = Array.isArray(state.steps)
    ? (state.steps as Record<string, unknown>[]).map((s) => ({ ...s }))
    : null;

  for (const op of ops) {
    if (op.op !== "replace" || typeof op.path !== "string") continue;
    const stepMatch = /^\/steps\/(\d+)\/status$/.exec(op.path);
    if (stepMatch && steps) {
      const i = Number(stepMatch[1]);
      if (steps[i]) steps[i] = { ...steps[i], status: op.value };
      continue;
    }
    const key = op.path.replace(/^\//, "");
    if (key && !key.includes("/")) {
      next[key] = op.value;
    }
  }
  if (steps) next.steps = steps;
  return next;
}

function diskState(data: StoredThread): Record<string, unknown> | null {
  const events = diskEvents(data);
  let state: Record<string, unknown> | null = null;
  for (const event of events) {
    if (event.type === EventType.STATE_SNAPSHOT) {
      const snapshot = event.snapshot;
      if (snapshot && typeof snapshot === "object") {
        state = snapshot as Record<string, unknown>;
      }
    } else if (
      event.type === EventType.STATE_DELTA &&
      state &&
      "delta" in event
    ) {
      state = applyStateDelta(state, (event as { delta: unknown }).delta);
    }
  }
  return state;
}

export class StudioAgentRunner extends InMemoryAgentRunner {
  readonly persistDir: string;

  constructor(persistDir?: string) {
    super();
    this.persistDir = persistDir ?? resolveThreadsDir();
  }

  private persist(threadId: string): void {
    const snap = snapshotFromRunner(this, threadId);
    if (!snap) return;
    if (!snap.name) snap.name = threadDisplayName(snap);
    saveThread(this.persistDir, snap);
  }

  private memoryEvents(threadId: string): BaseEvent[] {
    return super.getThreadEvents(threadId);
  }

  override run(request: AgentRunnerRunRequest): Observable<BaseEvent> {
    const obs = super.run(request);
    return new Observable((subscriber) => {
      const sub = obs.subscribe({
        next: (e) => subscriber.next(e),
        error: (err) => subscriber.error(err),
        complete: () => {
          try {
            this.persist(request.threadId);
          } catch (err) {
            console.error("[StudioAgentRunner] persist failed", err);
          }
          subscriber.complete();
        },
      });
      return () => sub.unsubscribe();
    });
  }

  override connect(request: AgentRunnerConnectRequest): Observable<BaseEvent> {
    if (this.memoryEvents(request.threadId).length > 0) {
      return super.connect(request);
    }
    const disk = loadDiskSnapshot(this.persistDir, request.threadId);
    if (!disk || disk.historicRuns.length === 0) {
      return super.connect(request);
    }
    const subject = new ReplaySubject<BaseEvent>(Infinity);
    for (const event of diskEvents(disk)) subject.next(event);
    subject.complete();
    return subject.asObservable();
  }

  override listThreads(): ReturnType<InMemoryAgentRunner["listThreads"]> {
    const mem = super.listThreads();
    const byId = new Map(mem.map((t) => [t.id, t]));
    for (const disk of listStoredThreads(this.persistDir)) {
      if (disk.historicRuns.length === 0 || byId.has(disk.threadId)) continue;
      const last = disk.historicRuns[disk.historicRuns.length - 1];
      const first = disk.historicRuns[0];
      byId.set(disk.threadId, {
        id: disk.threadId,
        name: disk.name ?? threadDisplayName(disk),
        agentId: last.agentId,
        organizationId: "",
        createdById: "",
        archived: false,
        createdAt: new Date(first.createdAt).toISOString(),
        updatedAt: new Date(last.createdAt).toISOString(),
      });
    }
    return [...byId.values()].sort(
      (a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime(),
    );
  }

  override getThreadMessages(threadId: string): Message[] {
    const mem = super.getThreadMessages(threadId);
    if (mem.length > 0) return mem;
    const disk = loadDiskSnapshot(this.persistDir, threadId);
    return disk ? diskMessages(disk) : [];
  }

  override getThreadEvents(threadId: string): BaseEvent[] {
    const mem = this.memoryEvents(threadId);
    if (mem.length > 0) return mem;
    const disk = loadDiskSnapshot(this.persistDir, threadId);
    return disk ? diskEvents(disk) : [];
  }

  override getThreadState(threadId: string): Record<string, unknown> | null {
    const mem = super.getThreadState(threadId);
    if (mem) return mem;
    const disk = loadDiskSnapshot(this.persistDir, threadId);
    return disk ? diskState(disk) : null;
  }

  override clearThreads(): void {
    super.clearThreads();
    clearThreadFiles(this.persistDir);
  }

  /** Supprime le fichier disque et vide la RAM (les autres threads restent lisibles via disque). */
  deleteThread(threadId: string): void {
    deleteThreadFile(this.persistDir, threadId);
    super.clearThreads();
  }
}
