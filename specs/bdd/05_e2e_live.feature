# language: fr
@agentic-writer @e2e @slow @requires_api
Fonctionnalité: Génération réelle bout en bout (format flash uniquement)
  En tant qu'auteur
  Je veux une flash complète via le pipeline éditorial sur de vrais modèles
  Afin de valider Architecte, chapitres, Editor et Auditeur sans coût nouvelle/novella

  @e2e @requires_api
  Scénario: Generate flash produit manuscrit et blueprint
    Étant donné OPENAI_API_KEY est défini
    Et Node est disponible pour l'export docx
    Quand j'exécute la CLI generate e2e-flash avec pitch court et format flash
    Alors la génération se termine avec succès
    Et le manuscrit final existe et fait plus de 500 octets
    Et le plan chapitres correspond au format flash
