# language: fr
@agentic-writer @studio @ui
Fonctionnalité: API Studio pour l'interface CopilotKit
  En tant qu'auteur
  Je veux récupérer santé, manuscrit et PDF depuis le frontend
  Afin d'afficher la progression et les livrables sans tout charger dans le chat

  @integration @ui
  Scénario: Health confirme que le backend Studio répond
    Étant donné le serveur FastAPI studio démarré en mode test
    Quand je GET sur "/health"
    Alors le code de statut HTTP est 200
    Et la réponse JSON contient status "ok"

  @integration @ui
  Scénario: Manuscrit introuvable renvoie 404
    Étant donné le serveur FastAPI studio démarré en mode test
    Quand je GET sur "/manuscript/slug-inexistant"
    Alors le code de statut HTTP est 404

  @integration @ui
  Scénario: Manuscrit final servi en markdown
    Étant donné le serveur FastAPI studio démarré en mode test
    Et un manuscrit final pour le slug "hangar-scelle"
    Quand je GET sur "/manuscript/hangar-scelle"
    Alors le code de statut HTTP est 200
    Et le corps contient "# Titre"

  @integration @ui
  Scénario: PDF servi pour prévisualisation
    Étant donné le serveur FastAPI studio démarré en mode test
    Et un pdf pour le slug "hangar-scelle"
    Quand je GET sur "/pdf/hangar-scelle"
    Alors le code de statut HTTP est 200
    Et le type de contenu est application/pdf

  @integration @ui
  Scénario: L'état Studio porte le brief et les étapes pipeline par défaut
    Étant donné un état studio initial pour slug "studio-integ" et pitch "Test pitch."
    Quand je construis les étapes pipeline avec export imprimable
    Alors l'état studio contient le slug "studio-integ"
    Et l'état studio contient le pitch "Test pitch."
    Et les étapes pipeline contiennent "Writer — fiche twist + brouillon"
    Et les étapes pipeline contiennent "Print layout — docx & pdf"
