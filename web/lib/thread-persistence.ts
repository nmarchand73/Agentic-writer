import fs from "node:fs";
import path from "node:path";
import type { BaseEvent, Message } from "@ag-ui/client";

export interface StoredHistoricRun {
  threadId: string;
  runId: string;
  agentId: string;
  parentRunId: string | null;
  events: BaseEvent[];
  messages: Message[];
  createdAt: number;
}

export interface StoredThread {
  threadId: string;
  name: string | null;
  historicRuns: StoredHistoricRun[];
}

/** Répertoire par défaut : `Agentic-writer/.data/studio-threads` */
export function resolveThreadsDir(): string {
  if (process.env.AGENTIC_WRITER_THREADS_DIR) {
    return path.resolve(process.env.AGENTIC_WRITER_THREADS_DIR);
  }
  const cwd = process.cwd();
  const root = path.basename(cwd) === "web" ? path.join(cwd, "..") : cwd;
  return path.join(root, ".data", "studio-threads");
}

function threadFilePath(dir: string, threadId: string): string {
  const safe = threadId.replace(/[^a-zA-Z0-9_-]/g, "_");
  return path.join(dir, `${safe}.json`);
}

export function ensureThreadsDir(dir: string): void {
  fs.mkdirSync(dir, { recursive: true });
}

export function loadThread(dir: string, threadId: string): StoredThread | null {
  const file = threadFilePath(dir, threadId);
  if (!fs.existsSync(file)) return null;
  try {
    const raw = fs.readFileSync(file, "utf8");
    return JSON.parse(raw) as StoredThread;
  } catch {
    return null;
  }
}

export function listStoredThreads(dir: string): StoredThread[] {
  if (!fs.existsSync(dir)) return [];
  const out: StoredThread[] = [];
  for (const name of fs.readdirSync(dir)) {
    if (!name.endsWith(".json")) continue;
    try {
      const raw = fs.readFileSync(path.join(dir, name), "utf8");
      out.push(JSON.parse(raw) as StoredThread);
    } catch {
      /* skip corrupt files */
    }
  }
  return out;
}

export function saveThread(dir: string, data: StoredThread): void {
  ensureThreadsDir(dir);
  const file = threadFilePath(dir, data.threadId);
  const tmp = `${file}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(data, null, 0), "utf8");
  fs.renameSync(tmp, file);
}

export function deleteThreadFile(dir: string, threadId: string): void {
  const file = threadFilePath(dir, threadId);
  if (fs.existsSync(file)) fs.unlinkSync(file);
}

export function clearThreadFiles(dir: string): void {
  if (!fs.existsSync(dir)) return;
  for (const name of fs.readdirSync(dir)) {
    if (name.endsWith(".json")) fs.unlinkSync(path.join(dir, name));
  }
}

/** Titre affiché : premier message utilisateur ou date. */
export function threadDisplayName(data: StoredThread): string {
  if (data.name) return data.name;
  for (const run of data.historicRuns) {
    for (const msg of run.messages) {
      if (msg.role === "user" && "content" in msg && typeof msg.content === "string") {
        const text = msg.content.trim();
        if (text) return text.length > 48 ? `${text.slice(0, 48)}…` : text;
      }
    }
  }
  const ts = data.historicRuns[data.historicRuns.length - 1]?.createdAt;
  if (ts) return new Date(ts).toLocaleString("fr-FR");
  return "Conversation";
}
