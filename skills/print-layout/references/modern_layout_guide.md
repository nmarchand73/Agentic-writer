# Modern Layout Guide — Twilight Zone Novelist
# Standards de l'industrie du livre (édition française)

**Lire en entier avant d'écrire le moindre code.**

---

## 1. Philosophie

Mise en page de livre littéraire imprimable tel quel.
Référence : Folio, Gallimard, Actes Sud, Faber & Faber.
Règle d'or : la mise en page doit être **invisible**.

---

## 2. Format de page — A5 avec marges asymétriques

```javascript
const PAGE = {
  size:   { width: 8391, height: 11906 },   // A5 148×210 mm
  margin: { top: 1021, bottom: 1247,         // 18mm haut, 22mm bas
            left: 1134, right: 907,          // 20mm gouttière, 16mm ext.
            header: 567, footer: 680 }
};
// Zone texte : 8391 − 1134 − 907 = 6350 DXA
```

---

## 3. Typographie

**Police : Palatino Linotype** (tous systèmes). Ne pas substituer.

| Rôle                 | size | pt     | line |
|----------------------|------|--------|------|
| Corps / dialogue     |  21  | 10.5pt | 264  |
| Narration Serling    |  20  | 10pt   | 252  |
| Titre couverture     | 128  | 64pt   | —    |
| Numéro chapitre      |  72  | 36pt   | —    |
| Titre chapitre       |  26  | 13pt   | —    |
| Folio / labels       |  18  | 9pt    | —    |

---

## 4. Helpers complets (copier-coller direct)

```javascript
const {
  Document, Packer, Paragraph, TextRun, Footer,
  AlignmentType, BorderStyle, SectionType, SimpleField
} = require('docx');
const fs = require('fs');

const FONT    = "Palatino Linotype";
const BODY_SZ = 21;
const NARR_SZ = 20;
const LINE    = 264;
const NARR_L  = 252;

const PAGE = {
  size:   { width: 8391, height: 11906 },
  margin: { top: 1021, bottom: 1247, left: 1134, right: 907,
            header: 567, footer: 680 }
};

// Corps justifié avec alinéa
const P = (text) => new Paragraph({
  alignment: AlignmentType.JUSTIFIED,
  spacing: { before: 0, after: 0, line: LINE, lineRule: "atLeast" },
  indent: { firstLine: 240 },
  widowControl: true,
  children: [new TextRun({ text, font: FONT, size: BODY_SZ, color: "111111" })]
});

// Premier paragraphe (pas d'alinéa)
const P0 = (text) => new Paragraph({
  alignment: AlignmentType.JUSTIFIED,
  spacing: { before: 0, after: 0, line: LINE, lineRule: "atLeast" },
  widowControl: true,
  children: [new TextRun({ text, font: FONT, size: BODY_SZ, color: "111111" })]
});

// Bloc narration Serling : UN seul paragraphe, retours forcés, filet gauche
const NARR = (lines) => new Paragraph({
  alignment: AlignmentType.LEFT,
  indent: { left: 480, right: 240 },
  spacing: { before: 480, after: 480, line: NARR_L, lineRule: "atLeast" },
  border: { left: { style: BorderStyle.SINGLE, size: 6, color: "111111", space: 12 } },
  widowControl: true,
  children: lines.flatMap((line, i) => i < lines.length - 1
    ? [new TextRun({ text: line, font: FONT, size: NARR_SZ, italics: true, color: "333333" }),
       new TextRun({ break: 1 })]
    : [new TextRun({ text: line, font: FONT, size: NARR_SZ, italics: true, color: "333333" })]
  )
});

// Séparateur de scène
const SEP = () => new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 360, after: 360 },
  children: [new TextRun({ text: "*  *  *", font: FONT, size: 18, color: "999999" })]
});

// Espace vertical
const VSPACE = (dxa) => new Paragraph({
  spacing: { before: dxa, after: 0 },
  children: [new TextRun({ text: "", size: 4 })]
});

// Filet horizontal centré
const RULE = (before = 0, after = 400) => new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before, after },
  border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: "CCCCCC", space: 1 } },
  indent: { left: 1270, right: 1270 },
  children: [new TextRun({ text: "", size: 4 })]
});

// Ouverture de chapitre : espace + numéro + titre + filet
const CHAP = (num, title) => [
  VSPACE(2880),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 60 },
    children: [new TextRun({ text: num, font: FONT, size: 72, color: "CCCCCC" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 120 },
    children: [new TextRun({
      text: title.toUpperCase(), font: FONT, size: 26,
      smallCaps: true, color: "222222", characterSpacing: 60
    })]
  }),
  RULE(0, 480),
];

// Pied de page — placeholder remplacé par le script patch_footers.py
const FOOTER = () => new Footer({
  children: [new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ font: FONT, size: 18, color: "AAAAAA",
      children: [new SimpleField("PAGE")] })]
  })]
});
```

---

## 5. Structure en sections

```javascript
const doc = new Document({
  sections: [
    // Section 0 : couverture (pas de folio)
    { properties: { page: PAGE }, children: [ /* titre */ ] },

    // Section 1 : narration d'ouverture (page impaire)
    { properties: { type: SectionType.ODD_PAGE, page: PAGE },
      footers: { default: FOOTER() },
      children: [ VSPACE(1440), NARR([...]) ] },

    // Section N : chaque chapitre (page impaire)
    { properties: { type: SectionType.ODD_PAGE, page: PAGE },
      footers: { default: FOOTER() },
      children: [ ...CHAP("I", "Titre"), P0("..."), P("..."), SEP(), P0("...") ] },
  ]
});

const path = require('path');
const workDir = process.env.STORY_WORK_DIR || path.join(__dirname, '../../../../output');
const base = process.env.STORY_BASE_NAME || 'story';

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(path.join(workDir, `${base}.docx`), buf);
  console.log("OK →", path.join(workDir, `${base}.docx`));
});
```

---

## 6. Page de couverture

```javascript
[ VSPACE(3200),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 280 },
    children: [new TextRun({ text: "Nom de la série", font: FONT, size: 22, italics: true, color: "888888" })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 280 },
    children: [new TextRun({ text: "TITRE", font: FONT, size: 128, bold: true, color: "111111" })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 0 },
    children: [new TextRun({ text: "Sous-titre", font: FONT, size: 20, italics: true, color: "888888" })] }),
  VSPACE(3000),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 0 },
    children: [new TextRun({ text: "Année", font: FONT, size: 19, color: "BBBBBB", characterSpacing: 80 })] }),
]
```

---

## 7. Pipeline de build

Après avoir écrit le générateur JS, utiliser le script :

```bash
# Depuis la racine NewBooks
bash .cursor/skills/twilight-zone-novelist/scripts/build_story.sh nom_histoire output/generate.js
```

Ce script exécute dans l'ordre :
1. `node generate.js` — génère le .docx dans `output/` (via `STORY_WORK_DIR` / `STORY_BASE_NAME`)
2. `unpack.py` — décompresse le XML
3. `patch_language_hyphen.py` — langue FR + autoHyphenation dans settings.xml
4. `patch_footers.py` — remplace SimpleField par les field codes OOXML corrects (**toujours en dernier**)
5. `pack.py` — recompresse et valide
6. `validate.py` — vérification schema
7. `soffice.py --convert-to pdf` — export PDF dans `output/`
8. Copie vers `/mnt/user-data/outputs/` si l'environnement Cursor cloud est disponible

**Important** : `patch_footers.py` doit toujours s'exécuter **après** `patch_language_hyphen.py`, sinon les footers sont corrompus.

---

## 8. Checklist avant livraison

- [ ] Palatino Linotype partout
- [ ] `AlignmentType.JUSTIFIED` sur corps et dialogue
- [ ] `widowControl: true` sur chaque paragraphe
- [ ] `spacing: { before: 0, after: 0, line: 264 }` sur le corps
- [ ] Pas d'alinéa (`P0`) après titre de chapitre et après `* * *`
- [ ] Chaque chapitre = section `SectionType.ODD_PAGE`
- [ ] Folios présents sauf couverture
- [ ] Narration = UN paragraphe avec `TextRun({ break: 1 })`
- [ ] `* * *` pour les séparateurs de scène
- [ ] Pipeline `build_story.sh` exécuté en entier
- [ ] PDF inspecté visuellement page par page
