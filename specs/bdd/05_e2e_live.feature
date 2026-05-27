# language: fr
@agentic-writer @e2e @slow @requires_api
Fonctionnalité: Génération réelle bout en bout
  En tant qu'auteur
  Je veux une flash complète avec manuscrit et export imprimable
  Afin de valider le pipeline sur de vrais modèles

  @e2e @requires_api
  Scénario: Generate flash produit manuscrit et export
    Étant donné OPENAI_API_KEY est défini
    Et Node est disponible pour l'export docx
    Quand j'exécute la CLI generate e2e-flash avec pitch court et format flash
    Alors la génération se termine avec succès
    Et le manuscrit final existe et fait plus de 500 octets
