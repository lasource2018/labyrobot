# labyrobot
labyrinthe1.py : 1ère version
  - Génération et tracé du labyrinthe
  - Interface Tk pour dimensionner la taille et lancer l'affichage du labyrinthe

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
  - Replay du trajet de sortie fonctionnel avec turtle

Problèmes :
  - algorithme peut revenir sur ses pas au départ
  - le replay n'est pas toujours synchronisé avec le scale

Manque :
  - resize de la fenêtre


labyrinthe4.py : 4ème version
  - Ajout du choix de la taille des hexagones (Tk et fonction)
  - Changement du replay pour remplacer la turtle par le numéro de cellule (plus de problème de synchro)
  - Correction du bug de l'algorithme de sortie
  - Correction du bug sur le calcul de nombre de murs cibles
  - Correction du bug sur la taille du scale du replay
  - Ajout du resize

Problèmes :
  - Resize ne retrace pas le labyrinthe centré
  - Le changement initial de la taille de cellule n'est pas pris en compte
  - Possibilité de cliquer sur 'Démarrer' sans avoir créé de labyrinthe 


labyrinthe5.py : 5ème version
  - Correction du resize pour retracer le labyrinthe centré
  - Correction du bug pour prendre en compte le changement initial de la taille de cellule (avant le tracé)
  - Correction pour que le bouton 'Démarrer' ne soit actif qu'après avoir créé un labyrinthe

Manque :
  - Changement interactif du type de paroi interne (mur ou ouverture)


labyrinthe6.py : 6ème version
  - Ajout de la vitesse de sortie

Problèmes :
  - La valeur finale du chemin n'apparait que lors de la première exécution du bouton 'Démarrer'
  
  
labyrinthe7.py : 7ème version (finale)
  - Correction du bug : la valeur finale du chemin n'apparaissait que lors de la première exécution du bouton 'Démarrer'
  - Aide en ligne complétée
  - Robustesse améliorée (valeurs mini et maxi testées pour les données largeur et hauteur)
  - Clic pour ajouter ou supprimer des murs internes
  - Calcul de temps et optimisation pour la création du labyrinthe
  - Calcul du temps pour la sortie du labyrinthe
  - Tests et corrections pour fonctionnement sans Tk
  - Mise à jour de la valeur de la couleur dans les textes du bouton
