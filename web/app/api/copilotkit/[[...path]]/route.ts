import type { NextRequest } from "next/server";
import { handleRequest } from "@/lib/copilotkit-runtime";

/** CopilotKit v2 (threads, run, subscribe, …) — all methods on /api/copilotkit/* */
const handler = (req: NextRequest) => handleRequest(req);

export const GET = handler;
export const POST = handler;
export const PUT = handler;
export const DELETE = handler;
export const PATCH = handler;
export const OPTIONS = handler;
