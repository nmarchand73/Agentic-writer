/** Suggestions du chat — le `title` est le libellé du bouton ; `message` part tel quel. */

type StudioSuggestion = { title: string; message: string };

function generationPrompt(opts: {
  slug: string;
  format: "flash" | "nouvelle";
  lang: "fr" | "en";
  pitch: string;
  mdOnly?: boolean;
}): string {
  const exportLine = opts.mdOnly
    ? "markdown seulement (pas de docx ni pdf)"
    : "docx et pdf (export imprimable)";
  return [
    "Lance la génération complète du pipeline (plan, chapitres, relecture, audit).",
    "",
    `slug : ${opts.slug}`,
    `format : ${opts.format}`,
    `langue : ${opts.lang}`,
    `export : ${exportLine}`,
    "",
    `pitch : ${opts.pitch}`,
  ].join("\n");
}

export const STUDIO_SUGGESTIONS: readonly StudioSuggestion[] = [
  {
    title: "Nouvelle · français · PDF — hangar militaire",
    message: generationPrompt({
      slug: "hangar-scelle",
      format: "nouvelle",
      lang: "fr",
      pitch:
        "Gardienne de nuit sur une base désaffectée. Un hangar scellé depuis 1989 s'ouvre de l'intérieur ; sur la vidéo, la silhouette en combinaison porte son badge d'aujourd'hui.",
    }),
  },
  {
    title: "Nouvelle · français · PDF — UAP sur le radar",
    message: generationPrompt({
      slug: "dossier-lumiere-noire",
      format: "nouvelle",
      lang: "fr",
      pitch:
        "Contrôleuse radar civile : un blip UAP suit sa route domicile–travail. Son mari et les caméras de l'immeuble jurent qu'elle n'est jamais rentrée cette nuit-là.",
    }),
  },
  {
    title: "Flash · français · PDF — voix sur la fréquence",
    message: generationPrompt({
      slug: "signal-77",
      format: "flash",
      lang: "fr",
      pitch:
        "Technicienne satellite : formation lumineuse non cataloguée. Une voix sur la fréquence de secours prononce le prénom de sa mère, morte depuis dix ans.",
    }),
  },
  {
    title: "Flash · français · texte seul (pas de PDF)",
    message: generationPrompt({
      slug: "archives-grises",
      format: "flash",
      lang: "fr",
      mdOnly: true,
      pitch:
        "Archiviste du programme UAP : pellicule de 1967. Sur le champ, une femme lui fait signe — c'est elle, vieillie de trois jours seulement.",
    }),
  },
  {
    title: "Flash · anglais · PDF — black triangle",
    message: generationPrompt({
      slug: "black-triangle",
      format: "flash",
      lang: "en",
      pitch:
        "Air traffic controller logs a black triangle over her suburb. Her daughter's school calls: the girl was picked up by \"Mom\" an hour ago.",
    }),
  },
  {
    title: "Nouvelle · français · PDF — porte sous le salon",
    message: generationPrompt({
      slug: "projet-meniscus",
      format: "nouvelle",
      lang: "fr",
      pitch:
        "Ex-scientifique du programme UAP reçoit des coordonnées GPS vers son sous-sol. Une porte qu'il n'a jamais eue s'ouvre sur un ciel étoilé en plein midi.",
    }),
  },
] as const;
