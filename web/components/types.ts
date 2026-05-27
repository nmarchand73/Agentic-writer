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
  md_only?: boolean;
  steps?: PipelineStepState[];
  output_dir?: string | null;
  manuscript_preview?: string | null;
  manuscript_md?: string | null;
  error?: string | null;
  usage_input_tokens?: number;
  usage_output_tokens?: number;
  usage_requests?: number;
  estimated_cost_usd?: number | null;
}
