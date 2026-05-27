# language: fr
@agentic-writer @cli
Fonctionnalité: CLI generate — brief minimal
  En tant qu'auteur
  Je veux lancer une génération avec slug et pitch seulement
  Afin d'éviter une longue liste d'options à chaque nouvelle histoire

  @unit
  Plan du scénario: Slug et pitch avec défauts nouvelle en français
    Étant donné le slug <slug>
    Et le pitch <pitch>
    Quand je parse la commande generate
    Alors le brief a le slug <slug>
    Et le brief a le pitch <pitch>
    Et le brief a le format "nouvelle"
    Et le brief a la langue "fr"
    Et le titre résolu est <titre_attendu>

    Exemples:
      | slug                  | pitch                                                                                  | titre_attendu         |
      | dossier-lumiere-noire | Contrôleuse radar voit un blip UAP ; personne ne la voit rentrer.                      | Dossier lumiere noire |
      | black-triangle-en       | ATC logs a black triangle; school says Mom already picked up her daughter.             | Black triangle en      |

  @unit
  Scénario: Format flash et langue anglaise surchargent les défauts
    Étant donné le slug "smoke"
    Et le pitch "Test."
    Et les options generate "--format flash --lang en"
    Quand je parse la commande generate
    Alors le brief a le format "flash"
    Et le brief a la langue "en"

  @unit
  Scénario: Un fichier brief YAML remplace slug et pitch en ligne de commande
    Étant donné le fichier brief "examples/briefs/flash-smoke.yaml"
    Quand je parse generate avec le fichier brief
    Alors le brief a le slug "flash-smoke"
    Et le brief a le format "flash"
    Et le brief a le theme "mystère / UAP"

  @unit
  Scénario: Generate refuse l'absence de pitch et de fichier brief
    Quand j'invoque la commande generate mon-slug
    Alors le code de sortie CLI est 2

  @unit
  Scénario: Generate refuse un format inconnu
    Quand j'invoque la commande generate x --pitch y --format roman-complet
    Alors le code de sortie CLI est 2

  @unit
  Scénario: Le dossier de livraison suit le slug
    Étant donné le slug "ma-nouvelle"
    Quand je résous le dossier de sortie
    Alors le dossier se termine par "output/ma-nouvelle"

  @integration
  Scénario: L'option md-only saute l'export imprimable
    Étant donné des agents simulés
    Et une commande "generate test --pitch p --md-only"
    Quand j'exécute generate via la CLI
    Alors le pipeline a été appelé sans export imprimable

  @integration
  Scénario: Sans md-only l'export imprimable est demandé
    Étant donné des agents simulés
    Et build_docx simulé
    Et une commande "generate test --pitch p"
    Quand j'exécute generate via la CLI
    Alors le pipeline a été appelé avec export imprimable
