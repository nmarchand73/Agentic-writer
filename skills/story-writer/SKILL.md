---
name: story-writer
description: Create domestic psychological suspense novels and short stories (BookTok-style twist fiction) (The Housemaid, Never Lie, The Crash, Do You Remember?, The Inmate, The Teacher, The Boyfriend, Dear Debbie, The Divorce). Use this skill when users want to (1) generate original thrillers in McFadden's voice, (2) write novellas or full-length domestic suspense, (3) build collections of twist-ending short stories, (4) reproduce her signature mechanics — first-person present narration, short binge-able chapters, mid-twist + end-twist + coda bombshell, locked-attic huis clos, wealthy abusive couples, working-class avenger heroines. Triggers include requests about "Freida McFadden", "McFadden style", "thriller psychologique domestique", "domestic suspense", "Housemaid-style", "BookTok thriller", "twist endings", "good for her revenge fiction".
---

# Story Writer — suspense psychologique domestique

Generate domestic psychological suspense fiction that reads as if written by Freida McFadden herself. The voice is intimate, ironic, present-tense, first-person; the architecture is propulsive, chapter-by-chapter, with a guaranteed mid-twist, end-twist, and final-page bombshell.

This skill is calqued on `twilight-zone-novelist`. The reference document `references/narrative_style_guide.md` is the canonical distilled grammar of McFadden's style — **read it in full before generating a single sentence**. The reference document `references/modern_layout_guide.md` defines the print-ready layout — **read it in full before generating the `.docx`**.

## Quick Start

To write a McFadden-style novella or short story:

1. Read the style guide: `references/narrative_style_guide.md`.
2. Read the market calibration: `../_shared/bestseller_mechanics_2026.md` (les dix principes du best-seller 2026 — McFadden les pratique déjà nativement, mais la collection doit s'y aligner explicitement).
3. **Conceive the twist first.** Do not write a word of prose until you can verbalize:
   - The **final twist** (the irreversible recontextualization of the whole book).
   - The **mid-twist** (the false resolution around the 50–60 % mark).
   - The **coda bombshell** (the last-page reveal that re-rewrites everything).
   - The narrator's **lie by omission** (what she knows and never says out loud).
   - The **one-sentence pitch** (test BookTok : si le pitch ne tient pas en 15 mots émotionnellement clairs, le concept est encore flou).
   - L'**émotion dominante** du livre (suspense, vengeance, peur intime, indignation sociale).
4. Cast the archetypes (see `references/narrative_style_guide.md` §7):
   - A precarious working-class heroine with a buried past.
   - A wealthy antagonist couple — the inquiétant + the rassurant — exactly one of whom is the true predator.
   - One auxiliary warner (gardener, neighbour, child) who cryptically signals danger.
5. Pick the trap-house and the isolating element (snow storm, locked attic, hidden basement, suburb cul-de-sac).
6. Write the **prologue choc** (200–400 words, anonymous first person, present tense).
7. Cut the story into **short chapters of 800–2 500 words**. Each chapter ends on one of the six signature hook patterns.
8. Place the mid-twist around the 50–60 % mark, the end-twist in the last 15 %, and the coda bombshell in the final 1–2 pages.
9. Self-check against the §13.3 quality checklist in the style guide AND the universal page-turner test in `../_shared/bestseller_mechanics_2026.md`.

## Story Formats

| Format | Mots | Structure |
|--------|-------|-----------|
| Flash thriller | 1 500 – 3 000 | Un prologue choc + 2 chapitres + coda bombe |
| Nouvelle | 8 000 – 15 000 | 1 POV, 6–12 chapitres, mid + end + coda |
| Novella | 30 000 – 50 000 | 1–2 POV, dual timeline possible, 20–40 chapitres |
| Roman | 70 000 – 90 000 | 2–3 POV, structure complète 3 actes, dual timeline obligatoire |
| Anthologie thématique | 5–7 nouvelles | Variations sur un thème (la maison-piège, le couple toxique, la maternité menacée) — patterns de twist **différents** d'une nouvelle à l'autre |

## Writing Process

### Phase 1 — Twist Engineering (avant toute écriture)

McFadden l'a dit elle-même : *« Je ne commencerai jamais à écrire tant que je n'ai pas un twist. Si mon mari dit "oh, c'est pas mal" — ça ne suffit pas. »* Reproduire cette discipline.

Remplir cette fiche AVANT de commencer :

```
TWIST FINAL : [phrase qui réécrit le sens du livre]
MID-TWIST (fausse résolution ~50 %) : [phrase]
CODA BOMBE (dernière page) : [phrase]
MENSONGE PAR OMISSION DE LA NARRATRICE : [ce qu'elle sait et tait]
3 SCÈNES QUE LE TWIST RECONTEXTUALISE : [scène A, scène B, scène C]
2 INDICES DE FORESHADOWING EN PREMIÈRE MOITIÉ : [indice 1, indice 2]
```

Si la fiche est incomplète, ne pas passer à la phase 2.

### Phase 2 — Personnages

- **Protagoniste** : femme 25–45 ans, précaire (économique / conjugale / médicale / juridique), avec un secret du passé (prison, avortement, premier mariage caché, accident, condamnation), sous-estimée par son entourage, intelligente mais joue la naïve. Voix intérieure ironique, autodérision.
- **Couple antagoniste** : un membre inquiétant dès le départ, un membre charmant et rassurant. Décider lequel est le vrai prédateur — c'est l'inversion qui produit le twist.
- **Personnage utilitaire 1** : l'avertisseur cryptique (jardinier, voisin, enfant — *cf.* Enzo dans *The Housemaid*).
- **Personnage utilitaire 2 (optionnel)** : autorité corrompue qui freine la résolution (médecin, avocat, policier).

### Phase 3 — Décor et huis clos

- Une **maison bourgeoise belle dehors / étouffante dedans**, dotée d'un **détail anomique** signalé dès l'Acte I (chambre verrouillée de l'extérieur, sous-sol interdit, cassettes cachées, grenier muré).
- Un **élément d'isolement** : tempête de neige, blizzard, ouragan, route coupée, voiture en panne.
- Un **contraste social brutal** entre le décor de la protagoniste (studio à Lewiston, voiture cassée) et celui de l'antagoniste (manoir, garage triple).

### Phase 4 — Architecture narrative

Suivre la structure McFadden canonique :

| Section | Proportion | Fonction |
|---------|------------|----------|
| Prologue choc | 200–400 mots | Scène irréversible hors contexte, narrateur anonyme, présent |
| Acte I — Installation | 25–30 % | Quotidien, maison-piège, détail anomique planté |
| Acte II — Spirale paranoïaque | ~50 % | Indices troublants, gaslighting, **mid-twist** vers 50–60 % |
| Acte III — Retournement | 20–25 % | **End-twist** : inversion victime/bourreau, identité cachée, complot conjugal |
| Coda finale | 100–200 mots | **Bombe finale** qui réécrit tout |

### Phase 5 — Écriture chapitre par chapitre

Pour CHAQUE chapitre :

1. **Longueur** : 800–2 500 mots. Pas plus.
2. **Première ligne** : phrase choc, menace, sentence ou contradiction (jamais une description).
3. **Voix** : première personne, présent, conversationnel, ironique. Phrases courtes, parataxe.
4. **Densité dialogue** : ~40–50 % du chapitre. Répliques brèves, mordantes, qui font avancer le plot.
5. **Voix intérieure** : au moins une pensée ironique / vulgaire / drôle par scène.
6. **Détails sensoriels** : **uniquement s'ils servent le plot** (règle d'or McFadden : un détail = un usage narratif).
7. **Fin de chapitre** : terminer sur l'un des six hooks signature :
   1. Découverte d'objet (« Et c'est là que j'ai vu le couteau, glissé sous l'oreiller. »)
   2. Réplique-bombe (« — Tu sais qu'elle n'est pas vraiment morte. »)
   3. Bascule de perception (« Soudain, j'ai compris que ce n'était pas elle, la victime. C'était moi. »)
   4. Action interrompue (« Ethan tendit la main vers la poignée de la chambre. »)
   5. Question ouverte (« Pourquoi mentait-elle ? Et pourquoi maintenant ? »)
   6. Révélation différée (« Je savais ce que je devais faire. Mais je ne pouvais pas le faire ce soir-là. »)

### Phase 6 — Twist, coda, vérification

- **Mid-twist** : autour des 50–60 %. Doit sembler résoudre l'énigme — c'est du *fool's gold*.
- **End-twist** : dans les 15 derniers %. Doit recontextualiser au moins 3 scènes antérieures, être préparé par au moins 2 indices, et ne demander pas plus de 500 mots d'explication.
- **Coda bombe** : 100–200 mots, dernière page, une ou deux phrases qui réécrivent le sens.
- **Self-check** : passer la checklist §13.3 du style guide.

## Calibration marché 2026

McFadden incarne déjà nativement la **commercial fiction storytelling** anglo-saxonne en train de gagner le marché français. Trois principes du best-seller 2026 (cf. `../_shared/bestseller_mechanics_2026.md`) demandent néanmoins une attention explicite à chaque écriture :

### A. Thèmes universels contemporains (principe §5)

McFadden recycle les mêmes traumas. Pour rester pertinent en 2026, **rattacher chaque livre à au moins un thème universel actuel** :

```
santé mentale · burn-out · maternité contrainte · violence économique
contrôle coercitif · charge mentale · précarité du soin · injustice sociale
solitude post-confinement · solitude algorithmique · pression patriarcale
secret de famille générationnel · dépendance affective
```

Le thème ne doit jamais être exposé frontalement : il est porté par la situation de la protagoniste.

### B. Pitch BookTok (principe §8)

Avant d'écrire, formuler le pitch en UNE phrase de 15 mots maximum, structure :

> *[protagoniste vulnérable + identifiant social] + [situation domestique inquiétante] + [promesse de twist].*

**Exemples calibrés :**
- *« Femme de ménage tout juste sortie de prison, elle découvre que la chambre de la belle maison ne se verrouille que de l'extérieur. »*
- *« Enceinte de huit mois, sans-abri en puissance, elle accepte l'aide d'un couple un peu trop parfait. »*
- *« Infirmière de nuit, elle reconnaît son nouveau patient : c'est l'ex qu'elle a fait condamner. »*

Si le pitch est flou, retravailler le concept avant d'écrire un mot.

### C. Scène mémorable + réplique-citation (principe §8)

Chaque livre McFadden doit contenir :

- **Au moins une scène mémorable** que les lecteurs filment / décrivent sur TikTok (la porte qui se verrouille de l'extérieur ; la cassette retrouvée dans le mur ; le moment où l'on comprend qui est vraiment l'épouse à l'étage).
- **Au moins une réplique-citation** qui se tweete (modèle : *« Everybody lies »*, *« Le genre avec des mots »*, *« Don't even try to take my expired bread »*).

Identifier ces deux éléments avant la dernière passe d'écriture. Si aucun n'émerge naturellement, le manuscrit n'est pas viral.

### D. Hybridation contrôlée (principe §6)

Le thriller psychologique pur fonctionne, mais le marché récompense de plus en plus les **hybrides** :

- Thriller + saga familiale (secrets sur trois générations).
- Thriller + romance toxique (l'ennemi est aussi l'objet de désir).
- Thriller + feel-good inversé (la communauté soudée cache l'horreur).
- Thriller + speculative léger (mémoire, identité, amnésie médicalement plausible — McFadden l'a déjà ouvert avec *Do You Remember?*).

Choisir un greffon par livre, jamais deux.

### E. Évasion malgré la noirceur (principe §7)

Même quand le sujet est dur (féminicide, abus médical, violence conjugale), le livre doit offrir une **forme d'évasion** : un décor dépaysant (manoir de Long Island, cabane du Maine, lune de miel exotique, hôpital isolé), une vengeance jouissive, un sentiment de complicité avec la narratrice. McFadden = *« good for her »*, jamais misérabilisme.

---

## Règles d'or McFadden (les cinq commandements)

1. **Voix intime au présent**, première personne, conversationnelle, ironique, complice du lecteur.
2. **Chapitres courts** qui terminent tous sur un hook.
3. **Twist double** — fausse résolution au milieu, vraie révélation à la fin, bombe en coda.
4. **Huis clos domestique** avec un élément anomique signalé tôt.
5. **Critique sociale du pouvoir** (riche/pauvre, mari/épouse, employeur/employée) qui ne se dit jamais mais structure tout.

## Le piège n°1 à éviter : le « narrative cheating »

La narratrice à la première personne peut **omettre** mais ne doit **jamais explicitement contredire** la vérité dans sa pensée intérieure. Elle peut éviter un sujet, le détourner, le présenter par une métaphore. Elle ne peut pas penser activement une fausseté.

> ❌ Mauvais : *« Je me demandais qui avait bien pu tuer Maria. »* (alors que la narratrice est la meurtrière)
> ✅ Bon : *« La police interrogerait tout le monde. Je devais être prête. »*

C'est le grief le plus fréquent contre McFadden — la skill doit l'éviter.

## Citations modèles à imiter

**Prologue type — *The Crash* :**
> *« I've never killed anyone before.*
> *I'm not a murderer. I'm a good person. I don't lie. I don't cheat. I don't steal. I hardly ever even raise my voice. There are very few things I've done in my life that I'm ashamed of.*
> *Yet here I am.*
> *I expected a struggle from the person beneath me. But I didn't expect this much of a struggle. I didn't expect this much thrashing.*
> *Or the muffled screams. »*

**Première ligne signature — *Never Lie* :**
> *« Everybody lies. »*

**Dialogue mordant — *The Housemaid* :**
> *« — Qu'est-ce que tu aimes lire ?*
> *— Des livres.*
> *— Quel genre de livres ?*
> *— Le genre avec des mots. »*

**Voix intérieure ironique — *The Crash* :**
> *« Don't even try to take my expired bread, you asshole. »*

**Information sismique enterrée dans une réplique anodine :**
> *« He is not, by the way, the father of my unborn child. He's not my boyfriend either. »*

## Banque de tropes (à varier entre nouvelles d'une collection)

| Trope | Description | Référence |
|-------|-------------|-----------|
| Locked Attic Room | Chambre subalterne verrouillée de l'extérieur | *The Housemaid* |
| The Live-in Servant | Domestique vivant chez l'employeur | *The Housemaid* |
| Snow-trapped | Couple bloqué par tempête | *Never Lie*, *The Crash* |
| Hidden Recordings | Cassettes / journal secret découverts | *Never Lie* |
| The Wife Replaced | L'épouse précédente n'est peut-être pas morte | *The Wife Upstairs* |
| The Pregnant Refugee | Enceinte fuyant un foyer dangereux, recueillie par des inconnus | *The Crash* |
| The Inmate Lover | Détenu = ex de la soignante | *The Inmate* |
| The Suburban Avenger | Mère de banlieue devient justicière | *Dear Debbie* |
| The Memory Lapse | Amnésie partielle exploitée par l'entourage | *Do You Remember?* |
| Mid-twist + Final twist + Coda | Faux dénouement → vrai twist → bombe | Quasi tous |
| The Letter / The Note | Document écrit qui ré-explique tout | Fréquent |
| The Switched Identity | Le personnage n'est pas qui elle prétend être | *Never Lie*, *The Boyfriend* |
| Wealthy Couple, Dark Secret | Couple aisé cache une horreur | Très fréquent |
| The Unreliable Confidante | Le ou la meilleur(e) ami(e) ment | Fréquent |

**Règle d'anthologie** : ne jamais réutiliser le même pattern de twist deux fois dans la même collection. Le lecteur McFadden expérimenté flaire la répétition.

## Garde-fous éthiques

McFadden traite de violence conjugale, abus sexuels, avortement, suicide, troubles psychiatriques. La skill doit :

- Représenter la violence sans la **glamouriser** ni la décrire avec complaisance graphique.
- Donner aux victimes une **agentivité narrative** (le « *good for her* »).
- Éviter les stéréotypes psychiatriques stigmatisants (la « folle » qui s'avère réellement folle est un trope à inverser).
- Ne pas reproduire le narrative cheating dénoncé par les lecteurs.

## Output Format

**Toujours produire un `.docx` ET un `.pdf`** au terme de chaque nouvelle ou collection.

### Étape 1 — Lire le guide de mise en page

Avant d'écrire le moindre code de génération, lire en entier :

```
references/modern_layout_guide.md
```

Ce guide définit le système visuel complet : format A5, Palatino Linotype, page de couverture, ouverture de chapitre, blocs de prose justifiés, séparateurs de scène, pieds de page numérotés. **Ne pas inventer une mise en page — suivre le guide.**

### Étape 2 — Générer le `.docx`

Utiliser `docx-js` (`npm install -g docx`). Suivre le squelette et les helpers du `modern_layout_guide.md` à la lettre. Règles clés :

- Palatino Linotype partout.
- Couverture : titre en grandes bold 64pt, sous-titre italique, label série en petites capitales.
- Ouverture de chapitre : numéro 36pt en gris pâle, titre en small-caps tracées, filet horizontal.
- Corps : 10.5pt, justifié, alinéa de première ligne 240 DXA (sauf premier paragraphe après titre / après séparateur).
- Pas de bloc « narration encadrée » à la Serling — McFadden n'a pas de narrateur omniscient.
- Séparateurs de scène : `*  *  *` centrés en gris.
- Pieds de page : numéro de page Palatino 9pt gris.

### Étape 3 — Pipeline de build

Depuis la racine du projet NewBooks :

```bash
bash skills/story-writer/scripts/build_story.sh nom_histoire output/generate.js
```

Le générateur `generate.js` doit écrire le `.docx` dans `process.env.STORY_WORK_DIR` sous le nom `${process.env.STORY_BASE_NAME}.docx` (variables exportées par le script).

Fichiers produits par défaut dans `output/` à la racine NewBooks (`nom_histoire.docx` + `nom_histoire.pdf`). En environnement Cursor cloud, copie additionnelle vers `/mnt/user-data/outputs/` si disponible.

Ce script enchaîne : génération → décompression XML → patch langue/césures FR → patch pieds de page → recompression → validation → conversion PDF.

### Étape 4 — Inspection visuelle

Vérifier le PDF page par page :

- [ ] Page de couverture épurée et centrée.
- [ ] Chaque chapitre commence sur page impaire.
- [ ] Aucun « veuve » ni « orphelin » en bas/haut de page.
- [ ] Folios présents sauf en couverture.
- [ ] Italique pour la voix intérieure courte, pas pour le prologue (qui est en romain).
- [ ] Séparateurs `*  *  *` aux bonnes ruptures de scène.

## Quality Checklist (avant livraison)

Reprendre la checklist §13.3 du style guide :

- [ ] La narratrice a-t-elle un secret du passé révélé entre 30 et 60 % ?
- [ ] Y a-t-il un mid-twist et un end-twist distincts ?
- [ ] La coda contient-elle une dernière révélation ?
- [ ] Chaque chapitre se termine-t-il sur un hook (parmi les six patrons) ?
- [ ] La maison ou le huis-clos a-t-il un détail anomique signalé tôt ?
- [ ] Y a-t-il une critique sociale implicite (classe, genre, pouvoir conjugal) ?
- [ ] Le foreshadowing du twist est-il présent mais détourné ?
- [ ] La narratrice évite-t-elle de mentir explicitement dans sa pensée intérieure ?
- [ ] Les dialogues sont-ils nombreux (~40–50 %) et courts ?
- [ ] Y a-t-il au moins une réplique-citation mémorable ?
- [ ] La voix intérieure est-elle ironique / conversationnelle ?
- [ ] L'antagoniste apparent est-il différent de l'antagoniste réel ?
- [ ] Le lecteur peut-il *« cheer for her »* à la fin ?

**Calibration marché 2026 (cf. `../_shared/bestseller_mechanics_2026.md`) :**

- [ ] Le pitch tient en 1 phrase BookTok de ≤ 15 mots.
- [ ] L'émotion dominante du livre est explicite (suspense, vengeance, peur intime…).
- [ ] Au moins un thème universel 2026 est greffé sans être exposé frontalement.
- [ ] Au moins une scène mémorable « partageable » est identifiée.
- [ ] Au moins une réplique-citation « tweetable » est plantée.
- [ ] L'hybridation (thriller + autre registre) est volontaire et limitée à un greffon.
- [ ] Le livre offre une forme d'évasion malgré la noirceur du sujet.
- [ ] Aucune page ne dépasse 6 lignes consécutives de description sans interruption.

## Reference Materials

- `references/narrative_style_guide.md` — Grammaire stylistique complète de McFadden (à lire en entier avant écriture).
- `references/modern_layout_guide.md` — Système visuel pour la génération `.docx` / `.pdf`.
- `../_shared/bestseller_mechanics_2026.md` — Calibration marché commune aux skills d'écriture.

## Tips pour la justesse stylistique

**Do** :
- Commencer par le twist, jamais par la prose.
- Écrire des chapitres si courts qu'on en veut « juste un de plus ».
- Glisser l'information sismique dans une réplique anodine (*« He is not, by the way, the father of my unborn child »*).
- Une fois par livre, insérer un mini-essai de pop-psychologie (~6 phrases) en utilisant l'expertise médicale.
- Récompenser le lecteur d'une dernière bombe qui re-rewrite tout.

**Don't** :
- Pas de descriptions longues, pas de métaphores littéraires élaborées, pas de digressions philosophiques.
- Pas de vocabulaire recherché — le lexique est délibérément accessible.
- Pas de structures temporelles complexes à l'intérieur d'une scène (les sauts temporels sont gérés par les chapitres).
- Pas plus de **trois** twists par nouvelle (au-delà : épuisement du lecteur).
- Pas de twist qui retombe sur du dérisoire (cf. l'échec critiqué de *The Ex*).
- Ne **jamais** faire mentir la narratrice explicitement dans sa pensée intérieure.

---

Rappel final : McFadden n'écrit pas pour qu'on l'admire — elle écrit pour qu'on **n'arrête pas de lire**. Le bon test : si le lecteur peut poser le livre à la fin d'un chapitre, la skill a échoué.

---

## Agentic Writer (CLI)

Quand tu es invoqué par **Agentic Writer** (pas Cursor interactif) :

- Retourne un **`WriterResult`** structuré : `twist_sheet` (tous les champs) + `manuscript` (markdown complet).
- **Pas de relecture** — l'agent `manuscript-editor` s'en charge ensuite.
- **Pas de docx** — l'export imprimable passe par `docx_build` côté application.
- Respecte le `format`, `lang` et `pitch` du brief utilisateur.
