import type { CopilotChatLabels } from "@copilotkit/react-core/v2";

/** Libellés français pour le chat CopilotKit du Studio. */
export const STUDIO_CHAT_LABELS: Partial<CopilotChatLabels> = {
  chatInputPlaceholder:
    "Ou écris ton brief : slug, format (flash/nouvelle), langue, pitch…",
  chatDisclaimerText:
    "L’IA peut se tromper — relis le manuscrit avant publication.",
  welcomeMessageText: "Quelle histoire veux-tu faire naître ?",
  assistantMessageToolbarCopyMessageLabel: "Copier",
  assistantMessageToolbarRegenerateLabel: "Regénérer",
  userMessageToolbarEditMessageLabel: "Modifier",
};
