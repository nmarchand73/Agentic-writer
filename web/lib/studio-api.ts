/** Backend Agentic Writer (FastAPI studio), distinct du proxy CopilotKit. */

export const STUDIO_API_BASE =
  process.env.NEXT_PUBLIC_AGENTIC_WRITER_API ?? "http://127.0.0.1:8000";

export function manuscriptUrl(slug: string): string {
  return `${STUDIO_API_BASE}/manuscript/${encodeURIComponent(slug)}`;
}

export function pdfUrl(slug: string): string {
  return `${STUDIO_API_BASE}/pdf/${encodeURIComponent(slug)}`;
}
