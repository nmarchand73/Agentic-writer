# language: fr
@agentic-writer @pipeline
Fonctionnalité: Pipeline récit Writer puis Editor
  En tant qu'auteur
  Je veux une fiche twist, un brouillon relu et des artefacts markdown
  Afin de livrer un manuscrit avant l'export docx/pdf

  @integration
  Scénario: Writer puis Editor produisent des résultats structurés
    Étant donné un Writer simulé retournant writer_flash.json
    Et un Editor simulé retournant editor_flash.json
    Et un brief format "flash" slug "pipeline-integ"
    Quand j'exécute le pipeline sans export imprimable
    Alors le résultat contient un WriterResult valide
    Et le résultat contient un EditorResult valide
    Et l'Editor est appelé une fois après le Writer

  @integration
  Scénario: La relecture reçoit le twist_final du Writer
    Étant donné un Writer simulé retournant writer_flash.json
    Et un Editor simulé capturant le prompt
    Et un brief format "flash" slug "pipeline-integ"
    Quand j'exécute le pipeline sans export imprimable
    Alors le prompt de relecture contient le twist_final du fixture

  @integration
  Scénario: Les artefacts markdown sont écrits dans le dossier de sortie
    Étant donné des agents simulés
    Et le slug "artefacts-test"
    Quand j'exécute le pipeline sans export imprimable
    Alors le fichier "twist_sheet.json" existe dans le dossier de sortie
    Et le fichier "draft_manuscript.md" existe dans le dossier de sortie
    Et le fichier "review.md" existe dans le dossier de sortie
    Et le fichier "manuscript_final.md" existe dans le dossier de sortie

  @integration
  Scénario: La fiche twist persistée reprend le twist_final du Writer
    Étant donné un Writer simulé retournant writer_flash.json
    Et un Editor simulé retournant editor_flash.json
    Et le slug "twist-persist"
    Quand j'exécute le pipeline sans export imprimable
    Alors twist_sheet.json contient le twist_final du fixture
