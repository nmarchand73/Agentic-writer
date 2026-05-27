/**
 * Agentic Writer — minimal docx generator for build_story.sh
 * Env: STORY_WORK_DIR, STORY_BASE_NAME
 */
const fs = require("fs");
const path = require("path");
const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  HeadingLevel,
} = require("docx");

const workDir = process.env.STORY_WORK_DIR || ".";
const baseName = process.env.STORY_BASE_NAME || "story";
const mdPath = path.join(workDir, "manuscript_final.md");
const outPath = path.join(workDir, `${baseName}.docx`);

if (!fs.existsSync(mdPath)) {
  console.error(`Missing ${mdPath}`);
  process.exit(1);
}

const md = fs.readFileSync(mdPath, "utf8");
const children = [];

for (const block of md.split(/\n\n+/)) {
  const trimmed = block.trim();
  if (!trimmed) continue;
  if (trimmed.startsWith("# ")) {
    children.push(
      new Paragraph({
        text: trimmed.slice(2),
        heading: HeadingLevel.HEADING_1,
      })
    );
  } else if (trimmed.startsWith("## ")) {
    children.push(
      new Paragraph({
        text: trimmed.slice(3),
        heading: HeadingLevel.HEADING_2,
      })
    );
  } else {
    children.push(
      new Paragraph({
        children: [new TextRun(trimmed.replace(/\n/g, " "))],
      })
    );
  }
}

const doc = new Document({ sections: [{ children }] });
Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(outPath, buffer);
  console.log(`Wrote ${outPath}`);
});
