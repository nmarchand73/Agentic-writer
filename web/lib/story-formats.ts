/** Repères éditoriaux — garder aligné avec src/agentic_writer/format_specs.py */

export type StoryFormatSpec = {
  key: string;
  label: string;
  words: string;
  pagesA5: string;
  description: string;
  supported: boolean;
};

export const STORY_FORMAT_SPECS: readonly StoryFormatSpec[] = [
  {
    key: "flash",
    label: "Flash",
    words: "~800–2 500 mots",
    pagesA5: "~3–10 p. (A5)",
    description: "Micro-fiction, un arc court.",
    supported: true,
  },
  {
    key: "nouvelle",
    label: "Nouvelle",
    words: "8 000–15 000 mots",
    pagesA5: "~30–55 p. (A5)",
    description: "Nouvelle de genre — défaut.",
    supported: true,
  },
  {
    key: "novella",
    label: "Novella",
    words: "30 000–50 000 mots",
    pagesA5: "~100–200 p. (A5)",
    description: "Roman court.",
    supported: true,
  },
  {
    key: "roman",
    label: "Roman",
    words: "70 000–90 000 mots",
    pagesA5: "~250–350 p. (A5)",
    description: "Roman long — bientôt dans le pipeline.",
    supported: false,
  },
] as const;

export const SUPPORTED_FORMAT_KEYS = STORY_FORMAT_SPECS.filter((s) => s.supported).map(
  (s) => s.key,
);

export const FORMATS_UI_HINT =
  "Dans le chat : précise format flash | nouvelle | novella et langue fr | en. Export docx/pdf A5 sauf si tu demandes markdown seul.";
