# labyrobot
labyrinthe1.py : 1ère version
  - Génération et tracé du labyrinthe
  - Interface Tk pour dimensionner la taille et lancer l'affichage

Manque :
  - Lancement automatique de l'interface
  - Définition des positions entrée et sortie
  - Algorithme de recherche du chemin


labyrinthe2.py : 2ème version
  - Démarrage automatique de l'interface Tk
  - Affichage et positionnement de l'entrée et de la sortie du labyrinthe (interface Tk)
  - Changement de couleur des entrées et sortie (interface Tk)
  
Manque :
  - Sortie du labyrinthe (interface et algorithme)


labyrinthe3.py : 3ème version
  - Interface Tk pour algorithme de sortie
  - Algorithme de sortie fonctionnel
  - Replay du trajet de sortie fonctionnel

Problèmes :
  - algorithme peut revenir sur ses pas au départ
  - le replay n'est pas toujours synchronisé avec le scale

Manque :
  - resize de la fenêtre


labyrinthe4.py : 4ème version
  - Ajout de la taille des hexagones
  - Changement du replay pour remplacer la turtle par le numéro de cellule (plus de problème de synchro)
  - Correction du bug de l'algorithme de sortie
  - Correction du bug sur le calcul de nombre de murs cibles
  - Correction du bug sur la taille du scale du replay

Problèmes :
  - Resize ne retrace pas le labyrinthe centré
  - Le changement initial de la taille de cellule n'est pas pris en compte
  - Possibilité de cliquer sur 'Démarrer' sans avoir créé de labyrinthe 

