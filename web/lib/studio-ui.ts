/** Libellés et micro-copy Studio — pro avec une touche de malice. */

export const STUDIO_TAGLINE =
  "Writer, Editor, export — la chaîne de montage de tes histoires pas tout à fait normales.";

export function stepEmoji(description: string): string {
  const d = description.toLowerCase();
  if (d.includes("brief") || d.includes("valider")) return "📋";
  if (d.includes("writer")) return "✍️";
  if (d.includes("editor") || d.includes("relecture")) return "🔎";
  if (d.includes("print") || d.includes("docx") || d.includes("export")) return "📕";
  if (d.includes("artefact") || d.includes("markdown")) return "📁";
  if (d.includes("livraison")) return "🎬";
  return "◆";
}

export function stepStatusLabel(status: string): string | null {
  switch (status) {
    case "running":
      return "En train de bidouiller…";
    case "completed":
      return "OK";
    case "pending":
      return null;
    default:
      return null;
  }
}

export function pipelineHeadline(completed: number, total: number): string {
  if (completed === 0) return "On démarre la machine";
  if (completed < total) return "Ça chauffe dans l'atelier";
  return "Standing ovation — pipeline terminé";
}
