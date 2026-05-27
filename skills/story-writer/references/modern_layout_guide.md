# Modern Layout Guide — McFadden Thriller Novelist
# Standards de l'industrie du livre (édition française, thriller commercial)

**Lire en entier avant d'écrire le moindre code.**

---

## 1. Philosophie

Mise en page de thriller commercial imprimable tel quel.
Référence : Robert Laffont (Best-Sellers), Belfond (Noir), Sonatine, Calmann-Lévy Noir & Blanc.
Règle d'or : la mise en page doit être **invisible** et **propulsive**. Le lecteur ne doit jamais s'arrêter sur la typo ; il doit binge-reader.

Différence avec un layout « littéraire » classique :
- **Chapitres très courts** → ouverture de chapitre allégée (pas de pages blanches inutiles).
- **Dialogue dense** → corps légèrement plus aéré pour lisibilité.
- **Voix intérieure** en italique sobre, jamais en bloc encadré (pas de narrateur omniscient à la Serling).

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

Choix Palatino : sérif chaleureuse, parfaitement lisible en petit corps, restitue bien le rythme rapide des chapitres courts McFadden.

| Rôle                  | size | pt     | line |
|-----------------------|------|--------|------|
| Corps / dialogue      |  21  | 10.5pt | 264  |
| Voix intérieure / cit |  21  | 10.5pt | 264  | (italique)
| Prologue choc         |  22  | 11pt   | 272  |
| Titre couverture      | 128  | 64pt   | —    |
| Numéro chapitre       |  56  | 28pt   | —    |
| Titre chapitre        |  24  | 12pt   | —    |
| Folio / labels        |  18  | 9pt    | —    |

Numéro de chapitre légèrement plus petit qu'en littéraire classique (28pt vs 36pt) car les chapitres McFadden sont courts et nombreux : pas besoin de monumentaliser chaque ouverture.

---

## 4. Helpers complets (copier-coller direct)

```javascript
const {
  Document, Packer, Paragraph, TextRun, Footer,
  AlignmentType, BorderStyle, SectionType, SimpleField
} = require('docx');
const fs = require('fs');

const FONT     = "Palatino Linotype";
const BODY_SZ  = 21;   // 10.5pt
const PROL_SZ  = 22;   // 11pt (prologue choc - légèrement plus grand)
const LINE     = 264;
const PROL_L   = 272;

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

// Premier paragraphe (pas d'alinéa) — après titre, après séparateur, après ligne blanche
const P0 = (text) => new Paragraph({
  alignment: AlignmentType.JUSTIFIED,
  spacing: { before: 0, after: 0, line: LINE, lineRule: "atLeast" },
  widowControl: true,
  children: [new TextRun({ text, font: FONT, size: BODY_SZ, color: "111111" })]
});

// Pensée intérieure / passage en italique
const PI = (text) => new Paragraph({
  alignment: AlignmentType.JUSTIFIED,
  spacing: { before: 0, after: 0, line: LINE, lineRule: "atLeast" },
  indent: { firstLine: 240 },
  widowControl: true,
  children: [new TextRun({ text, font: FONT, size: BODY_SZ, italics: true, color: "111111" })]
});

// Paragraphe-couperet (phrase isolée, type "Mais pas ce soir." / "Pourtant me voilà.")
const COUPERET = (text) => new Paragraph({
  alignment: AlignmentType.JUSTIFIED,
  spacing: { before: 200, after: 200, line: LINE, lineRule: "atLeast" },
  widowControl: true,
  children: [new TextRun({ text, font: FONT, size: BODY_SZ, color: "111111" })]
});

// Bloc PROLOGUE (légèrement plus grand, plus aéré)
const PROL = (text) => new Paragraph({
  alignment: AlignmentType.JUSTIFIED,
  spacing: { before: 0, after: 0, line: PROL_L, lineRule: "atLeast" },
  indent: { firstLine: 240 },
  widowControl: true,
  children: [new TextRun({ text, font: FONT, size: PROL_SZ, color: "111111" })]
});

const PROL0 = (text) => new Paragraph({
  alignment: AlignmentType.JUSTIFIED,
  spacing: { before: 0, after: 0, line: PROL_L, lineRule: "atLeast" },
  widowControl: true,
  children: [new TextRun({ text, font: FONT, size: PROL_SZ, color: "111111" })]
});

// Séparateur de scène — trois étoiles centrées en gris pâle
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

// Ouverture de chapitre McFadden — compacte (chapitres courts et nombreux)
const CHAP = (num, title) => [
  VSPACE(1920),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 60 },
    children: [new TextRun({ text: num, font: FONT, size: 56, color: "CCCCCC" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 120 },
    children: [new TextRun({
      text: title ? title.toUpperCase() : "", font: FONT, size: 24,
      smallCaps: true, color: "222222", characterSpacing: 60
    })]
  }),
  RULE(0, 360),
];

// Ouverture de chapitre numéroté SEULEMENT (sans titre) — souvent chez McFadden
const CHAP_N = (num) => [
  VSPACE(1920),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 120 },
    children: [new TextRun({ text: num, font: FONT, size: 56, color: "CCCCCC" })]
  }),
  RULE(0, 360),
];

// Bloc POV label (pour dual narration, ex: "MILLIE" / "NINA")
const POV = (name) => new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 240, after: 480 },
  children: [new TextRun({
    text: name.toUpperCase(), font: FONT, size: 20,
    smallCaps: true, color: "555555", characterSpacing: 80
  })]
});

// Bloc TIMELINE label (pour dual timeline, ex: "AUJOURD'HUI" / "AVANT")
const TIMELINE = (label) => new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 240, after: 480 },
  children: [new TextRun({
    text: label.toUpperCase(), font: FONT, size: 18, italics: true,
    smallCaps: true, color: "888888", characterSpacing: 80
  })]
});

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

    // Section 1 : prologue (page impaire, intitulé "AVANT", "APRÈS", "UNE SEMAINE PLUS TÔT"...)
    { properties: { type: SectionType.ODD_PAGE, page: PAGE },
      footers: { default: FOOTER() },
      children: [ VSPACE(1440), ...CHAP("Prologue", "Trois ans plus tard"), PROL0("..."), PROL("..."), COUPERET("Pourtant me voilà.") ] },

    // Section N : chaque chapitre (page impaire pour début, autres en flux)
    { properties: { type: SectionType.ODD_PAGE, page: PAGE },
      footers: { default: FOOTER() },
      children: [ ...CHAP_N("1"), P0("..."), P("..."), SEP(), P0("...") ] },
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

### Convention chapitres / sections

- **Chapitre 1, 2, 3...** → numérotés seulement (`CHAP_N("1")`), souvent sans titre. C'est la convention McFadden.
- **Prologue / Épilogue / Avant / Après** → titré (`CHAP("Prologue", "Trois ans plus tard")`).
- **Dual POV** : insérer `POV("MILLIE")` ou `POV("NINA")` juste après le numéro de chapitre.
- **Dual timeline** : insérer `TIMELINE("Aujourd'hui")` ou `TIMELINE("Avant")` juste après le numéro de chapitre.
- **Chaque chapitre démarre sur page impaire** via `SectionType.ODD_PAGE`.

---

## 6. Page de couverture

```javascript
[ VSPACE(3200),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 240 },
    children: [new TextRun({ text: "Freida McFadden", font: FONT, size: 22, italics: true, color: "888888" })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 280 },
    children: [new TextRun({ text: "TITRE DU ROMAN", font: FONT, size: 128, bold: true, color: "111111" })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 0 },
    children: [new TextRun({ text: "Un thriller", font: FONT, size: 20, italics: true, color: "888888" })] }),
  VSPACE(3000),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 0 },
    children: [new TextRun({ text: "2026", font: FONT, size: 19, color: "BBBBBB", characterSpacing: 80 })] }),
]
```

Si la skill est utilisée à des fins de pastiche public, **ne pas signer du nom de Freida McFadden** — utiliser le nom de l'auteur réel ou *« d'après le style de Freida McFadden »*.

---

## 7. Pipeline de build

Après avoir écrit le générateur JS, utiliser le script :

```bash
# Depuis la racine NewBooks
bash skills/story-writer/scripts/build_story.sh nom_histoire output/generate.js
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

## 8. Conventions typographiques françaises (à respecter)

- **Guillemets français** : `« texte »` avec espace insécable interne.
- **Tirets de dialogue** : tiret cadratin `—` en début de réplique. Pas `-`.
- **Apostrophe française** : `'` (typographique), pas `'` (droit).
- **Points de suspension** : `…` (caractère unique), pas `...`.
- **Espaces fines insécables** avant `: ; ! ?` — gérées par autoHyphenation FR.

Exemple de dialogue correctement formaté :

> *« Qu'est-ce que tu fais ici ? murmure-t-il.*
> *— Je pourrais te poser la même question.*
> *— Tu ne devrais pas être là.*
> *— Non. Mais me voilà. »*

---

## 9. Checklist avant livraison

- [ ] Palatino Linotype partout (corps + couverture).
- [ ] `AlignmentType.JUSTIFIED` sur corps et dialogue.
- [ ] `widowControl: true` sur chaque paragraphe.
- [ ] `spacing: { before: 0, after: 0, line: 264 }` sur le corps.
- [ ] Pas d'alinéa (`P0`) après titre de chapitre et après `*  *  *`.
- [ ] Chaque chapitre = section `SectionType.ODD_PAGE`.
- [ ] Folios présents sauf couverture.
- [ ] Chapitres numérotés sans titre (convention McFadden) — sauf prologue / épilogue.
- [ ] Voix intérieure courte en italique (`PI`) si elle s'étend sur un paragraphe.
- [ ] Paragraphes-couperets (`COUPERET`) pour les bascules type *« Mais pas ce soir. »*.
- [ ] Séparateurs `*  *  *` aux ruptures de scène intra-chapitre.
- [ ] Guillemets `« »` et tirets cadratin `—` partout.
- [ ] Apostrophes typographiques `'`.
- [ ] Pipeline `build_story.sh` exécuté en entier.
- [ ] PDF inspecté page par page (aucune veuve ni orpheline, aucune césure tronquée).

---

## 10. Anti-patterns spécifiques à éviter

- ❌ Pas de **bloc encadré narratif** type Serling — McFadden n'a pas de narrateur omniscient.
- ❌ Pas de **drop-cap / lettrine** sur le premier paragraphe — trop littéraire, brise le rythme thriller.
- ❌ Pas de **page blanche de respiration** entre chapitres — McFadden enchaîne, le lecteur doit pouvoir tourner immédiatement.
- ❌ Pas de **citation en exergue** ornementale (épigraphes Goethe / Shakespeare) — McFadden ouvre sec.
- ❌ Pas de **note de bas de page** — incompatible avec la prose addictive.
