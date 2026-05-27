"use client";

type StudioChatWelcomeProps = {
  isRunning?: boolean;
};

export function StudioChatWelcome({ isRunning }: StudioChatWelcomeProps) {
  return (
    <div className="studio-chat-welcome text-center max-w-lg mx-auto">
      <div className="studio-chat-welcome-icon mx-auto mb-4" aria-hidden>
        ✦
      </div>
      <h2 className="text-xl sm:text-2xl font-semibold tracking-tight text-[var(--studio-fg)]">
        Quelle histoire veux-tu faire naître ?
      </h2>
      <p className="mt-2 text-sm text-[var(--studio-muted)] leading-relaxed">
        Choisis un exemple ci-dessous ou écris ton brief. Chaque bouton précise
        le <span className="font-medium text-[var(--studio-fg)]">format</span>,
        la <span className="font-medium text-[var(--studio-fg)]">langue</span> et
        si tu veux un{" "}
        <span className="font-medium text-[var(--studio-fg)]">PDF</span> à la fin.
      </p>

      <dl className="mt-5 text-left text-xs grid gap-2 sm:grid-cols-3 sm:gap-3">
        <div className="studio-chat-glossary-item">
          <dt className="font-semibold text-[var(--studio-fg)]">slug</dt>
          <dd className="text-[var(--studio-muted)] mt-0.5">
            Nom du dossier, sans espaces (ex.{" "}
            <code className="studio-inline-code">hangar-scelle</code>)
          </dd>
        </div>
        <div className="studio-chat-glossary-item">
          <dt className="font-semibold text-[var(--studio-fg)]">format</dt>
          <dd className="text-[var(--studio-muted)] mt-0.5">
            <code className="studio-inline-code">flash</code> (court) ou{" "}
            <code className="studio-inline-code">nouvelle</code> (long)
          </dd>
        </div>
        <div className="studio-chat-glossary-item">
          <dt className="font-semibold text-[var(--studio-fg)]">pitch</dt>
          <dd className="text-[var(--studio-muted)] mt-0.5">
            Ton intrigue en une ou deux phrases
          </dd>
        </div>
      </dl>

      <p className="mt-4 text-xs text-[var(--studio-muted)]">
        Tu peux modifier le message avant d&apos;envoyer.
      </p>

      {isRunning && (
        <p className="mt-4 text-xs font-medium text-[var(--studio-accent)] animate-pulse">
          Génération en cours…
        </p>
      )}
    </div>
  );
}
