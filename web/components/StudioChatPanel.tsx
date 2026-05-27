"use client";

import { CopilotChat } from "@copilotkit/react-core/v2";
import { STUDIO_CHAT_LABELS } from "../lib/studio-chat-labels";
import { StudioChatWelcome } from "./StudioChatWelcome";

const AGENT_ID = "agentic_writer_studio";

type StudioChatPanelProps = {
  isRunning?: boolean;
};

export function StudioChatPanel({ isRunning = false }: StudioChatPanelProps) {
  return (
    <section
      className="studio-card studio-chat-panel flex flex-col overflow-hidden min-h-[min(520px,62vh)]"
      aria-label="Conversation avec l’orchestrateur"
    >
      <header className="studio-chat-header shrink-0 px-4 py-3 border-b border-[var(--studio-border)]">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <p className="text-[10px] font-semibold uppercase tracking-widest text-[var(--studio-accent)]">
              Brief &amp; consignes
            </p>
            <h2 className="text-base font-semibold text-[var(--studio-fg)] mt-0.5">
              Décris ton récit
            </h2>
            <p className="text-xs text-[var(--studio-muted)] mt-1 max-w-lg leading-relaxed">
              Architecte → chapitres → éditeur → auditeur → export. La progression
              apparaît sous le chat.
            </p>
          </div>
          {isRunning && (
            <span
              className="studio-chat-live-badge"
              role="status"
              aria-live="polite"
            >
              <span className="studio-chat-live-dot" aria-hidden />
              En cours
            </span>
          )}
        </div>
      </header>

      <div className="flex-1 min-h-0 flex flex-col copilot-chat-wrap studio-chat-body">
        <CopilotChat
          agentId={AGENT_ID}
          className="h-full min-h-[360px] flex flex-col"
          labels={STUDIO_CHAT_LABELS}
          welcomeScreen={{
            welcomeMessage: () => (
              <StudioChatWelcome isRunning={isRunning} />
            ),
          }}
          messageView={{
            children: ({ messageElements, interruptElement }) => (
              <div
                data-testid="copilot-message-list"
                className="studio-chat-messages flex flex-col gap-3 py-2"
              >
                {messageElements}
                {interruptElement}
              </div>
            ),
          }}
        />
      </div>
    </section>
  );
}
