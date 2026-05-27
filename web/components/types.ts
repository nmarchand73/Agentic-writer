export type StepStatus = "pending" | "running" | "completed";

export interface PipelineStepState {
  description: string;
  status: StepStatus;
}

export interface StudioAgentState {
  slug?: string;
  pitch?: string;
  format?: string;
  lang?: string;
  steps?: PipelineStepState[];
  output_dir?: string | null;
  manuscript_preview?: string | null;
  manuscript_md?: string | null;
  error?: string | null;
}
