# language: fr
@agentic-writer @export
Fonctionnalité: Export imprimable docx et pdf
  En tant qu'auteur
  Je veux un docx et un pdf A5 à partir du manuscrit final
  Afin d'imprimer ou partager une version mise en page

  @integration
  Scénario: build_docx invoque le pipeline print-layout
    Étant donné manuscript_final.md dans le dossier de travail
    Et build_story.sh simulé avec succès
    Quand j'exécute build_docx pour le slug "export-integ"
    Alors build_story.sh a été invoqué avec le slug "export-integ"
    Et les fichiers temporaires d'export sont absents du dossier de travail

  @integration
  Scénario: Un échec print-layout remonte une erreur pipeline
    Étant donné manuscript_final.md dans le dossier de travail
    Et build_story.sh simulé en échec
    Quand j'exécute build_docx
    Alors une erreur pipeline est levée
