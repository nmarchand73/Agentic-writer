/**
 * Print layout — markdown → docx (A5 Palatino, calqué twilight-zone-novelist).
 * Env: STORY_WORK_DIR, STORY_BASE_NAME
 *
 * Conventions markdown (manuscrit Agentic Writer) :
 *   # Titre du livre          → page de couverture
 *   ## Titre de chapitre      → section impaire + ouverture chapitre
 *   > ligne                   → bloc narration encadrée (italique, filet)
 *   * * *  ou  ---            → séparateur de scène
 *   paragraphes               → corps justifié (alinéa sauf 1er après chapitre / sép.)
 */
const fs = require("fs");
const path = require("path");
const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  Footer,
  AlignmentType,
  BorderStyle,
  SectionType,
  SimpleField,
} = require("docx");

const FONT = "Palatino Linotype";
const BODY_SZ = 21;
const NARR_SZ = 20;
const LINE = 264;
const NARR_L = 252;

const PAGE = {
  size: { width: 8391, height: 11906 },
  margin: {
    top: 1021,
    bottom: 1247,
    left: 1134,
    right: 907,
    header: 567,
    footer: 680,
  },
};

const workDir = process.env.STORY_WORK_DIR || ".";
const baseName = process.env.STORY_BASE_NAME || "story";
const mdPath = path.join(workDir, "manuscript_final.md");
const outPath = path.join(workDir, `${baseName}.docx`);

if (!fs.existsSync(mdPath)) {
  console.error(`Missing ${mdPath}`);
  process.exit(1);
}

const md = fs.readFileSync(mdPath, "utf8");

const P = (text) =>
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { before: 0, after: 0, line: LINE, lineRule: "atLeast" },
    indent: { firstLine: 240 },
    widowControl: true,
    children: [
      new TextRun({ text, font: FONT, size: BODY_SZ, color: "111111" }),
    ],
  });

const P0 = (text) =>
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { before: 0, after: 0, line: LINE, lineRule: "atLeast" },
    widowControl: true,
    children: [
      new TextRun({ text, font: FONT, size: BODY_SZ, color: "111111" }),
    ],
  });

const NARR = (lines) =>
  new Paragraph({
    alignment: AlignmentType.LEFT,
    indent: { left: 480, right: 240 },
    spacing: { before: 480, after: 480, line: NARR_L, lineRule: "atLeast" },
    border: {
      left: { style: BorderStyle.SINGLE, size: 6, color: "111111", space: 12 },
    },
    widowControl: true,
    children: lines.flatMap((line, i) =>
      i < lines.length - 1
        ? [
            new TextRun({
              text: line,
              font: FONT,
              size: NARR_SZ,
              italics: true,
              color: "333333",
            }),
            new TextRun({ break: 1 }),
          ]
        : [
            new TextRun({
              text: line,
              font: FONT,
              size: NARR_SZ,
              italics: true,
              color: "333333",
            }),
          ]
    ),
  });

const SEP = () =>
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 360, after: 360 },
    children: [
      new TextRun({ text: "*  *  *", font: FONT, size: 18, color: "999999" }),
    ],
  });

const VSPACE = (dxa) =>
  new Paragraph({
    spacing: { before: dxa, after: 0 },
    children: [new TextRun({ text: "", size: 4 })],
  });

const RULE = (before = 0, after = 400) =>
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before, after },
    border: {
      bottom: { style: BorderStyle.SINGLE, size: 2, color: "CCCCCC", space: 1 },
    },
    indent: { left: 1270, right: 1270 },
    children: [new TextRun({ text: "", size: 4 })],
  });

const chapterHeading = (num, title) => [
  VSPACE(2880),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 60 },
    children: [
      new TextRun({ text: num, font: FONT, size: 72, color: "CCCCCC" }),
    ],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 120 },
    children: [
      new TextRun({
        text: title.toUpperCase(),
        font: FONT,
        size: 26,
        smallCaps: true,
        color: "222222",
        characterSpacing: 60,
      }),
    ],
  }),
  RULE(0, 480),
];

const FOOTER = () =>
  new Footer({
    children: [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({
            font: FONT,
            size: 18,
            color: "AAAAAA",
            children: [new SimpleField("PAGE")],
          }),
        ],
      }),
    ],
  });

const chapterSection = (heading, bodyBlocks) => ({
  properties: { type: SectionType.ODD_PAGE, page: PAGE },
  footers: { default: FOOTER() },
  children: [...heading, ...bodyBlocks],
});

function isSeparator(line) {
  const t = line.trim();
  return t === "* * *" || t === "***" || t === "---" || t === "—" || t === "–––";
}

function parseChapterBody(raw) {
  const blocks = [];
  let needP0 = true;
  const paragraphs = raw.split(/\n\n+/);

  for (const block of paragraphs) {
    const trimmed = block.trim();
    if (!trimmed) continue;

    if (isSeparator(trimmed.split("\n")[0])) {
      blocks.push(SEP());
      needP0 = true;
      continue;
    }

    const lines = trimmed.split("\n");
    if (lines.every((l) => l.trim().startsWith(">"))) {
      const narrLines = lines.map((l) => l.replace(/^>\s?/, "").trim());
      blocks.push(NARR(narrLines));
      needP0 = true;
      continue;
    }

    const text = lines.join(" ").trim();
    if (!text) continue;
    blocks.push(needP0 ? P0(text) : P(text));
    needP0 = false;
  }
  return blocks;
}

function romanNumeral(n) {
  const vals = [
    [10, "X"],
    [9, "IX"],
    [5, "V"],
    [4, "IV"],
    [1, "I"],
  ];
  let num = n;
  let out = "";
  for (const [v, s] of vals) {
    while (num >= v) {
      out += s;
      num -= v;
    }
  }
  return out || String(n);
}

// Split on ## headings
const parts = md.split(/^##\s+/m);
let bookTitle = baseName.replace(/-/g, " ");
const preamble = parts[0].trim();
if (preamble) {
  const titleMatch = preamble.match(/^#\s+(.+)$/m);
  if (titleMatch) bookTitle = titleMatch[1].trim();
}

const sections = [];

sections.push({
  properties: { page: PAGE },
  children: [
    VSPACE(3200),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 280 },
      children: [
        new TextRun({
          text: bookTitle,
          font: FONT,
          size: 128,
          bold: true,
          color: "111111",
        }),
      ],
    }),
    VSPACE(3000),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 0 },
      children: [
        new TextRun({
          text: new Date().getFullYear().toString(),
          font: FONT,
          size: 19,
          color: "BBBBBB",
          characterSpacing: 80,
        }),
      ],
    }),
  ],
});

let chapterIndex = 0;
for (let i = 1; i < parts.length; i++) {
  const chunk = parts[i].trim();
  if (!chunk) continue;
  const nl = chunk.indexOf("\n");
  const titleLine = nl === -1 ? chunk : chunk.slice(0, nl);
  const body = nl === -1 ? "" : chunk.slice(nl + 1);
  chapterIndex += 1;
  const num = romanNumeral(chapterIndex);
  const bodyBlocks = parseChapterBody(body);
  sections.push(chapterSection(chapterHeading(num, titleLine), bodyBlocks));
}

if (sections.length === 1) {
  sections.push(
    chapterSection(chapterHeading("I", "Texte"), parseChapterBody(md.replace(/^#\s+.+$/m, "").trim()))
  );
}

const doc = new Document({ sections });

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(outPath, buffer);
  console.log(`Wrote ${outPath} (${sections.length} sections)`);
});
