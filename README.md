# Rogue nethack with Flask

<img width="639" alt="image" src="https://user-images.githubusercontent.com/63783521/173240175-59331687-4243-4604-97d1-9c54b7126bf6.png">


# Mes modifications 
J'ai tout implémenté, sauf la possibiité de sauvegarder.
Les enemies sont en vert 

Le mode multijoueur est plus compliqué qu'on ne pourrait l'imaginer. Au contraire de beaucoup de groupes, au lieu de rajouter un deuxième joueur guidé par les clefs ZQSD, je choisis de donner à l'utilisateur la possibilité d'ajouter une nombre infini de joueurs. Il suffit d'ajouter un onglet, donc une deuxième session, et de cliquer sur "Add my player". Un nouveau joueur apparaît sur la carte. La clef de cette méthode réside dans l'utilisation de l'émission emit(..., to = request.sid). 

De plus, j'ai modifié le mode multi-niveau proposé. Au lieu de renvoyer un template différent du premier template lors de l'atteinte du niveau, je choisis de renvoyer à chaque instant toute la carte au client, puis de gérer toute l'information avec Javascript. Cela me permets d'implémenter, dans le même site, les deux niveaux, pour autant de joueurs que je veux. 

Enfin, j'ai implémenté la fonction sauvegarde. Il suffit d'entrer un username dans la boite indiqué, et de cliquer sur Save Game (le bouton bleu). L'état exacte du jeu sera sauvegardé dans une base de données SQLlite, dans le dossier du jeu Rogue, sur votre ordinateur, dans un fichier nommé "memory.db". 
