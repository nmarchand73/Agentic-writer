"use client";

import {
  CopilotKit,
  useAgent,
  UseAgentUpdate,
  useConfigureSuggestions,
} from "@copilotkit/react-core/v2";
import { useHydratedStudioState } from "../hooks/useHydratedStudioState";
import { useManuscript } from "../hooks/useManuscript";
import { usePdf } from "../hooks/usePdf";
import { useStudioThreadId } from "../hooks/useStudioThreadId";
import { STUDIO_SUGGESTIONS } from "./studioSuggestions";
import { DeliverablesTabs } from "./DeliverablesTabs";
import { StudioFormatHelp } from "./StudioFormatHelp";
import { StudioHeader } from "./StudioHeader";
import { StudioThreadPanel } from "./StudioThreadPanel";
import {
  DeliveryCard,
  ErrorBanner,
  FetchErrorBanner,
  LoadingManuscript,
} from "./StudioStatusCards";
import { StudioChatPanel } from "./StudioChatPanel";
import { TaskProgress } from "./TaskProgress";
import { UsageCostBar } from "./UsageCostBar";
import type { StudioAgentState } from "./types";

const AGENT_ID = "agentic_writer_studio";

export function StudioChat() {
  const { threadId, ready, setThreadId, startNewThread } = useStudioThreadId();

  if (!ready || !threadId) {
    return (
      <div className="studio-shell flex h-screen items-center justify-center text-sm text-[var(--studio-muted)]">
        Chargement du Studio…
      </div>
    );
  }

  return (
    <CopilotKit
      key={threadId}
      runtimeUrl="/api/copilotkit"
      agent={AGENT_ID}
      threadId={threadId}
      showDevConsole={false}
      useSingleEndpoint={false}
    >
      <ChatInner
        threadId={threadId}
        onSelectThread={setThreadId}
        onNewThread={startNewThread}
      />
    </CopilotKit>
  );
}

type ChatInnerProps = {
  threadId: string;
  onSelectThread: (id: string) => void;
  onNewThread: () => void;
};

function ChatInner({ threadId, onSelectThread, onNewThread }: ChatInnerProps) {
  const { agent } = useAgent({
    agentId: AGENT_ID,
    updates: [UseAgentUpdate.OnStateChanged, UseAgentUpdate.OnRunStatusChanged],
  });

  const liveState = (agent?.state ?? {}) as StudioAgentState;
  const agentState = useHydratedStudioState(threadId, liveState, agent);
  const steps = agentState.steps;
  const { markdown, loading, fetchError, ready } = useManuscript(agentState);
  const {
    url: pdfHref,
    available: pdfAvailable,
    checking: pdfChecking,
    ready: pdfReady,
    showPdfUi,
  } = usePdf(agentState);

  useConfigureSuggestions({
    suggestions: [...STUDIO_SUGGESTIONS],
    available: "always",
  });

  const showDelivery = Boolean(agentState.output_dir) && !agentState.error;
  const showManuscript = Boolean(markdown) && !agentState.error;
  const isRunning = Boolean(agent?.isRunning);

  return (
    <div className="studio-shell flex flex-col h-screen w-full">
      <StudioHeader
        trailing={
          <StudioThreadPanel
            activeThreadId={threadId}
            onSelectThread={onSelectThread}
            onNewThread={onNewThread}
          />
        }
      />

      <main className="flex-1 flex flex-col min-h-0 overflow-y-auto">
        <div className="max-w-5xl w-full mx-auto px-4 py-5 flex flex-col gap-4 flex-1">
          <StudioChatPanel isRunning={isRunning} />
          <StudioFormatHelp />

          <UsageCostBar state={agentState} isRunning={isRunning} />

          {steps && steps.length > 0 && <TaskProgress steps={steps} />}

          {agentState.error && <ErrorBanner message={agentState.error} />}

          {showDelivery && (
            <DeliveryCard
              slug={agentState.slug}
              outputDir={agentState.output_dir!}
              pdfHref={showPdfUi ? pdfHref ?? undefined : undefined}
            />
          )}

          {ready && loading && !markdown && <LoadingManuscript />}

          {pdfReady && pdfChecking && !pdfAvailable && markdown && (
            <p className="text-xs text-center text-[var(--studio-muted)] py-1">
              Génération du PDF en cours…
            </p>
          )}

          {fetchError && <FetchErrorBanner detail={fetchError} />}

          {showManuscript && (
            <DeliverablesTabs
              markdown={markdown!}
              slug={agentState.slug}
              format={agentState.format}
              outputDir={agentState.output_dir}
              pdfUrl={pdfHref}
              showPdfUi={showPdfUi}
              pdfChecking={pdfChecking}
            />
          )}
        </div>
      </main>
    </div>
  );
}
