import { StudioAgentRunner } from "./studio-agent-runner";

/** Singleton partagé entre la route CopilotKit et l’API Studio. */
export const studioRunner = new StudioAgentRunner();
