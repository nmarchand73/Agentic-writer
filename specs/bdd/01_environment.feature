# language: fr
@agentic-writer @bootstrap
Fonctionnalité: Prérequis Agentic Writer
  En tant qu'auteur
  Je veux valider l'installation avant d'appeler l'API ou le Studio
  Afin d'éviter des échecs silencieux sur les skills ou l'export imprimable

  @bootstrap
  Scénario: Doctor confirme un environnement prêt
    Quand j'exécute la commande doctor
    Alors le code de sortie est 0
    Et la sortie mentionne "story-writer"
    Et la sortie mentionne "print-layout"

  @bootstrap
  Scénario: Doctor échoue si la skill d'écriture est absente
    Étant donné le fichier skills/story-writer/SKILL.md est absent
    Quand j'exécute la commande doctor
    Alors le code de sortie est différent de 0
    Et la sortie mentionne "story-writer"

  @bootstrap
  Scénario: L'agent Writer n'expose que story-writer
    Quand je liste les skills exposées à l'agent d'écriture
    Alors la liste contient "story-writer"
    Et la liste ne contient pas "manuscript-editor"

  @bootstrap
  Scénario: L'agent Editor expose relecture et lecture du Writer
    Quand je liste les skills exposées à l'agent de relecture
    Alors la liste contient "manuscript-editor"
    Et la liste contient "story-writer"
