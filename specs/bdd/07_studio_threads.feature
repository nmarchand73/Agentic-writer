# language: fr
@agentic-writer @studio @ui @threads
Fonctionnalité: Mémoire des conversations Studio
  En tant qu'auteur
  Je veux retrouver mes chats après redémarrage du serveur web
  Afin de reprendre un brief ou consulter une génération passée

  @integration @ui
  Scénario: Un message utilisateur est persisté avec un titre lisible
    Étant donné un dossier studio threads vide
    Quand je sauvegarde un thread "bdd-save-1" avec le message utilisateur "Radar UAP la nuit"
    Alors le fichier thread "bdd-save-1" existe sur disque
    Et le thread sur disque a pour titre "Radar UAP la nuit"

  @integration @ui
  Scénario: Après redémarrage le runner relit messages et liste des threads
    Étant donné un dossier studio threads vide
    Et un thread "bdd-reload-1" sauvegardé sur disque avec le message "Pitch hangar scellé"
    Quand je crée un runner studio frais sur ce dossier
    Alors le runner liste le thread "bdd-reload-1"
    Et le runner expose le message "Pitch hangar scellé" pour ce thread

  @integration @ui
  Scénario: Plusieurs threads sur disque apparaissent dans l'historique
    Étant donné un dossier studio threads vide
    Et un thread "bdd-a" sauvegardé sur disque avec le message "Brief A"
    Et un thread "bdd-b" sauvegardé sur disque avec le message "Brief B"
    Quand je crée un runner studio frais sur ce dossier
    Alors le runner liste 2 threads

  @integration @ui
  Scénario: Supprimer une conversation retire son fichier
    Étant donné un dossier studio threads vide
    Et un thread "bdd-del-1" sauvegardé sur disque
    Quand je supprime le thread "bdd-del-1" via le runner studio
    Alors le fichier thread "bdd-del-1" n'existe pas sur disque
