"use client";

export function ErrorBanner({ message }: { message: string }) {
  return (
    <div
      role="alert"
      className="studio-card border-red-200/80 dark:border-red-900/60 bg-red-50/90 dark:bg-red-950/40 px-4 py-3 flex gap-3 items-start"
    >
      <span className="text-lg shrink-0" aria-hidden>
        🚨
      </span>
      <div>
        <p className="font-medium text-red-900 dark:text-red-200 text-sm">
          Oups — la machine s&apos;est emmêlée les pinceaux
        </p>
        <p className="mt-1 text-sm text-red-800/90 dark:text-red-300/90">{message}</p>
      </div>
    </div>
  );
}

export function LoadingManuscript() {
  return (
    <div className="studio-card px-4 py-6 flex flex-col items-center gap-3 text-center">
      <div className="studio-loader" aria-hidden />
      <p className="text-sm font-medium text-[var(--studio-fg)]">
        On feuillette le manuscrit…
      </p>
      <p className="text-xs text-[var(--studio-muted)]">
        Encore quelques secondes — le twist arrive après le chargement.
      </p>
    </div>
  );
}

export function FetchErrorBanner({ detail }: { detail: string }) {
  return (
    <div className="studio-card border-amber-200/80 dark:border-amber-800/50 bg-amber-50/80 dark:bg-amber-950/30 px-4 py-3 text-sm">
      <p className="font-medium text-amber-900 dark:text-amber-200">
        Manuscrit introuvable côté serveur
      </p>
      <p className="mt-1 text-amber-800/90 dark:text-amber-300/80 text-xs font-mono">
        {detail}
      </p>
      <p className="mt-2 text-xs text-[var(--studio-muted)]">
        Lance{" "}
        <code className="studio-inline-code">uv run agentic-writer serve --port 8000</code>{" "}
        puis réessaie.
      </p>
    </div>
  );
}

export function DeliveryCard({
  slug,
  outputDir,
}: {
  slug?: string;
  outputDir: string;
}) {
  return (
    <div className="studio-card studio-card-success overflow-hidden">
      <div className="px-4 py-3 flex items-center gap-3 border-b border-emerald-200/60 dark:border-emerald-800/40 bg-emerald-50/50 dark:bg-emerald-950/20">
        <span className="text-2xl" aria-hidden>
          🎉
        </span>
        <div>
          <p className="font-semibold text-emerald-900 dark:text-emerald-100 text-sm">
            C&apos;est dans la boîte
          </p>
          <p className="text-xs text-emerald-800/80 dark:text-emerald-300/80 mt-0.5">
            Twist, brouillon, relecture, export — tout est rangé au même endroit.
          </p>
        </div>
      </div>
      <div className="px-4 py-3 space-y-2 text-sm">
        {slug && (
          <p className="text-[var(--studio-muted)]">
            Projet{" "}
            <span className="font-mono text-[var(--studio-fg)] bg-[var(--studio-elevated)] px-1.5 py-0.5 rounded">
              {slug}
            </span>
          </p>
        )}
        <p className="font-mono text-xs text-[var(--studio-muted)] break-all">{outputDir}</p>
        <div className="flex flex-wrap gap-1.5 pt-1">
          {["twist_sheet.json", "draft", "review", "final.md", "docx", "pdf"].map((f) => (
            <span key={f} className="studio-file-chip">
              {f}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
