/**
 * Assertions runner Studio pour pytest-bdd (via BDD_SCRIPT + AGENTIC_WRITER_THREADS_DIR).
 */
import { StudioAgentRunner } from "../lib/studio-agent-runner";
import { loadThread } from "../lib/thread-persistence";

const persistDir = process.env.AGENTIC_WRITER_THREADS_DIR;
const script = process.env.BDD_SCRIPT;
const threadId = process.env.BDD_THREAD_ID ?? "";
const expectedMessage = process.env.BDD_MESSAGE ?? "";

function fail(msg: string): never {
  console.error(`[thread-runner-bdd] ${msg}`);
  process.exit(1);
}

if (!persistDir) fail("AGENTIC_WRITER_THREADS_DIR manquant");
if (!script) fail("BDD_SCRIPT manquant");

const runner = new StudioAgentRunner(persistDir);

switch (script) {
  case "count": {
    const n = runner.listThreads().length;
    const expected = Number(process.env.BDD_THREAD_COUNT ?? "0");
    if (n !== expected) {
      fail(`attendu ${expected} threads, obtenu ${n}`);
    }
    break;
  }
  case "list-and-messages": {
    const listed = runner.listThreads();
    if (!listed.some((t) => t.id === threadId)) {
      fail(`thread ${threadId} absent de listThreads()`);
    }
    const messages = runner.getThreadMessages(threadId);
    const found = messages.some(
      (m) =>
        m.role === "user" &&
        "content" in m &&
        typeof m.content === "string" &&
        m.content.includes(expectedMessage),
    );
    if (!found) {
      fail(
        `message attendu "${expectedMessage}" introuvable: ${JSON.stringify(messages)}`,
      );
    }
    break;
  }
  case "delete": {
    runner.deleteThread(threadId);
    if (loadThread(persistDir, threadId)) {
      fail(`fichier thread ${threadId} encore présent après delete`);
    }
    break;
  }
  case "get-state": {
    const state = runner.getThreadState(threadId);
    const expectedSteps = Number(process.env.BDD_STEP_COUNT ?? "0");
    const steps = state?.steps;
    if (!Array.isArray(steps) || steps.length !== expectedSteps) {
      fail(
        `attendu ${expectedSteps} steps dans state, obtenu: ${JSON.stringify(state)}`,
      );
    }
    const expectedSlug = process.env.BDD_SLUG;
    if (expectedSlug && state?.slug !== expectedSlug) {
      fail(`slug attendu ${expectedSlug}, obtenu ${String(state?.slug)}`);
    }
    break;
  }
  default:
    fail(`BDD_SCRIPT inconnu: ${script}`);
}

process.exit(0);
