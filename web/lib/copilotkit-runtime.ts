import {
  CopilotSseRuntime,
  createCopilotHonoHandler,
} from "@copilotkit/runtime/v2";
import { HttpAgent } from "@ag-ui/client";
import { handle } from "hono/vercel";
import { Agent, setGlobalDispatcher } from "undici";
import { studioRunner } from "./studio-runtime";

const aguiUrl =
  process.env.AGENTIC_WRITER_AGUI_URL ?? "http://127.0.0.1:8000/agui";

// Prevent undici BodyTimeoutError on long AG-UI runs (LLM steps can take minutes).
// Default undici body timeout is too low for end-to-end pipelines.
const bodyTimeoutMs = Number(
  process.env.AGENTIC_WRITER_UNDICI_BODY_TIMEOUT_MS ?? "1200000",
); // 20 minutes
if (Number.isFinite(bodyTimeoutMs) && bodyTimeoutMs > 0) {
  setGlobalDispatcher(new Agent({ bodyTimeout: bodyTimeoutMs }));
}

const runtime = new CopilotSseRuntime({
  agents: {
    agentic_writer_studio: new HttpAgent({ url: aguiUrl }),
  },
  runner: studioRunner,
});

/** multi-route: GET /threads, POST /agent/:id/run, etc. (required by CopilotKit v2 UI) */
const app = createCopilotHonoHandler({
  runtime,
  basePath: "/api/copilotkit",
  mode: "multi-route",
});

export const handleRequest = handle(app);
