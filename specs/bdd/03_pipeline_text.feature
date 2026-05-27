# language: fr
@agentic-writer @pipeline
Fonctionnalité: Pipeline récit éditorial
  En tant qu'auteur
  Je veux une fiche twist, un plan chapitres, un manuscrit relu et audité
  Afin de livrer un texte prêt avant l'export docx/pdf

  @integration
  Scénario: Architecte, chapitres, Editor et Auditeur produisent des résultats structurés
    Étant donné un Architecte simulé retournant writer_flash.json
    Et un Writer chapitre simulé avec un corps long
    Et un Editor simulé retournant editor_flash.json
    Et un Auditeur simulé avec succès
    Et un brief format "flash" slug "pipeline-integ"
    Quand j'exécute le pipeline sans export imprimable
    Alors le résultat contient un WriterResult valide
    Et le résultat contient un EditorResult valide
    Et l'Editor est appelé après l'Architecte et les chapitres

  @integration
  Scénario: La relecture reçoit le twist_final du plan
    Étant donné un Architecte simulé retournant writer_flash.json
    Et un Writer chapitre simulé avec un corps long
    Et un Editor simulé capturant le prompt
    Et un Auditeur simulé avec succès
    Et un brief format "flash" slug "pipeline-integ"
    Quand j'exécute le pipeline sans export imprimable
    Alors le prompt de relecture contient le twist_final du fixture

  @integration
  Scénario: Les artefacts markdown sont écrits dans le dossier de sortie
    Étant donné des agents simulés
    Et le slug "artefacts-test"
    Quand j'exécute le pipeline sans export imprimable
    Alors le fichier "twist_sheet.json" existe dans le dossier de sortie
    Et le fichier "blueprint.json" existe dans le dossier de sortie
    Et le fichier "draft_manuscript.md" existe dans le dossier de sortie
    Et le fichier "review.md" existe dans le dossier de sortie
    Et le fichier "manuscript_final.md" existe dans le dossier de sortie
    Et le fichier "audit_report.md" existe dans le dossier de sortie

  @integration
  Scénario: La fiche twist persistée reprend le twist_final du plan
    Étant donné un Architecte simulé retournant writer_flash.json
    Et un Writer chapitre simulé avec un corps long
    Et un Editor simulé retournant editor_flash.json
    Et un Auditeur simulé avec succès
    Et le slug "twist-persist"
    Quand j'exécute le pipeline sans export imprimable
    Alors twist_sheet.json contient le twist_final du fixture
