/** Backend Agentic Writer (FastAPI studio), distinct du proxy CopilotKit. */

export const STUDIO_API_BASE =
  process.env.NEXT_PUBLIC_AGENTIC_WRITER_API ?? "http://127.0.0.1:8000";

export function manuscriptUrl(slug: string): string {
  return `${STUDIO_API_BASE}/manuscript/${encodeURIComponent(slug)}`;
}

export function exportBaseName(slug: string, format: string): string {
  return `${slug}-${format}`;
}

export function pdfUrl(slug: string, format?: string): string {
  const path = `${STUDIO_API_BASE}/pdf/${encodeURIComponent(slug)}`;
  if (!format) return path;
  return `${path}?format=${encodeURIComponent(format)}`;
}
