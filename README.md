# Rogue nethack with Flask

Programme Python servant de base à l'évaluation par projet du cours Programme coopérants et Web Intro. 



# Mes modifications 
J'ai tout implémenté, sauf la possibiité de sauvegarder. 

Le mode multijoueur est plus compliqué qu'on ne pourrait l'imaginer. Au contraire de beaucoup de groupes, au lieu de rajouter un deuxième joueur guidé par les clefs ZQSD, je choisis de donner à l'utilisateur de rajouter une nombre infini de joueurs. Il suffit d'ajouter un onglet, donc une deuxième session, et de cliquer sur "Add my player". Un nouveau joueur apparaît sur la carte. La clef de cette méthode réside dans l'utilisation de l'émission emit(..., to = request.sid). 


De plus, j'ai modifié le mode multi-niveau proposé. Au lieu de renvoyer un template différent du premier template lors de l'atteinte du niveau, je choisis de renvoyer à chaque instant toute la carte au client, puis de gérer toute l'information avec Javascript. Cela me permets d'implémenter, dans le même site, les deux niveaux, pour autant de joueurs que je veux. 






TO DO:
- Fix players crossing each other
- Fix spawns for enemies
