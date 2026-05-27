import {
  CopilotSseRuntime,
  createCopilotHonoHandler,
} from "@copilotkit/runtime/v2";
import { HttpAgent } from "@ag-ui/client";
import { handle } from "hono/vercel";
import { studioRunner } from "./studio-runtime";

const aguiUrl =
  process.env.AGENTIC_WRITER_AGUI_URL ?? "http://127.0.0.1:8000/agui";

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
