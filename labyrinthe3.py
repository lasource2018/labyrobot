# Pour fonctions mathématiques (sinus, cosinus)
import math
# Pour tracé graphique
import turtle
# Pour calcul de temps / performances
import time
# Pour nombre aléatoire
import random
# Pour Interface Homme-Machine
from tkinter import Tk,Canvas,Label,LabelFrame,IntVar,BooleanVar,Entry,Scale,Checkbutton,Button,Frame,StringVar,OptionMenu
from tkinter.messagebox import showerror, showinfo
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.constants


# ------------------------------------------------------------------------------
# Constantes

# Titre du TPE
TITRE = "Projet Labyrinthe"

# Version
VERSION = " v1.3"

# Texte d'aide
AIDE = \
"""
Entrer la largeur et la hauteur souhaitées du labyrinthe
puis cliquer sur 'Créer'
"""

# Racine de 3 sur 2 = sinus(60°)
RACINE3_2 = math.sqrt(3) / 2

# Nombre de données par hexagone : 1 pour chaque mur (6) + 1 pour les calculs = 7
NBR_HEXA = 7

# Définition du mur externe
MUR_EXT = 0

# Définition du mur interne (fermé)
MUR_INT = 1

# Définition de la paroi interne (ouverte)
PAROI = 2

# Largeur par défaut du labyrinthe
LARGEUR_DEF = 10

# Hauteur par défaut du labyrinthe
HAUTEUR_DEF = 10

# Largeur par défaut (en pixels) de la partie du tracé du labyrinthe
LARGEUR_FEN = 600

# Hauteur par défaut (en pixels) de la partie du tracé du labyrinthe
HAUTEUR_FEN = 600

# Tag de l'entrée
TAG_ENTREE = "Entree_tag"

# Tag de la sortie
TAG_SORTIE = "Sortie_tag"

# Main (quelle main sera posée sur le mur)
MAIN = ("Gauche", "Droite")

# Orientation initiale
ORIENTATION = ("NordEst", "Nord", "NordOuest", "SudOuest", "Sud", "SudEst")


# ------------------------------------------------------------------------------
# Variables globales

# Epaisseur des traits des murs (externe, interne, paroi, chemin)
TailleMurs = (3, 2, 1, 2)

# Couleurs du mur en fonction du type (externe, interne, paroi, chemin)
CouleurMurs = ('black', 'blue', 'pink', 'orange')

# Etat de l'initialisation de Turtle
InitTurtle = False

# Demi-largeur d'un hexagone (en pixels)
DemiLargeurHexa = 20

# Tableau des états des murs
TabLaby = [[[0] * NBR_HEXA] * 1] * 1

# Largeur du labyrinthe
Largeur = 0

# Hauteur du labyrinthe
Hauteur = 0

# Demi largeur et hauteur totales
DemiLargeurTotale = DemiHauteurTotale = 0

# Debug
Debug = False

# Interface
TK = True

# Position de l'entrée du labyrinthe
Entree = [0, 0]

# Position de la sortie du labyrinthe
Sortie = [0, 0]

# Couleur entrée
CoulEntree = "#00FF00"

# Couleur sortie
CoulSortie = "#FF0000"

# Orientation de la 'turtle' : 0 = 30°, 1 = 90°, 2 = 150°, 3 = 210°, 4 = 270°, 5=330°
Heading = 0

# Nouvelle orientation testée : +1 si main droite, -1 si main gauche
# La valeur initiale doit être cohérente avec MAIN[0]
# Si c'est main gauche, on tourne vers la droite pour mettre la main gauche au mur
# Si c'est main droite, on tourne vers la gauche pour mettre la main droite au mur
Sens = -1

# Chemin trouvé (liste des cellules traversées)
Chemin = []

# Canvas pour le tracé du labyrinthe sous Tk
Wcanvas = 0


# ------------------------------------------------------------------------------
# Fonctions

# Affichage des informations
def info() :
    print(TITRE)
    print(VERSION)
    print("Pour plus d'informations :\n>>> aide()\n")
    return


# Affichage du texte d'aide
def aide() :
    print(AIDE)
    return
   

# Création interface Tk
# a_largeur : largeur du labyrinthe
# a_hauteur : hauteur du labyrinthe
def creeInterface(a_largeur = LARGEUR_FEN, a_hauteur = HAUTEUR_FEN) :
    global Wcanvas, ValLargeur, ValHauteur, EntreeX, EntreeY, SortieX, SortieY
    global CoulEntreeLbl, CoulEntreeBtn, CoulSortieLbl, CoulSortieBtn, Main, Orient, Replay
    # Fenêtre principale
    root = Tk()
    root.title(TITRE + VERSION)
    root.geometry(str(a_largeur)+"x"+str(a_hauteur+140)+"-10+10")
    # Frame des données
    dataFrame = Frame(root)
    # Partie 'Labyrinthe'
    labyFrame = LabelFrame(dataFrame, text='Labyrinthe')
    # Première ligne : largeur du labyrinthe
    Label(labyFrame, text='Largeur').grid(row=0, column=0)
    ValLargeur = StringVar(root)
    ValLargeur.set(LARGEUR_DEF)
    Entry(labyFrame, textvariable=ValLargeur, width=2).grid(row=0, column=1)
    # Deuxième ligne : hauteur du labyrinthe
    Label(labyFrame, text='Hauteur').grid(row=1, column=0)
    ValHauteur = StringVar(root)
    ValHauteur.set(HAUTEUR_DEF)
    Entry(labyFrame, textvariable=ValHauteur, width=2).grid(row=1, column=1)
    # Troisième ligne : bouton 'Créer'
    Button(labyFrame, text='Créer', command=creerLabyCmd).grid(row=2, column=0, columnspan=2)
    # Fin de la partie labyFrame
    labyFrame.grid(row=0, column=0, sticky=tkinter.N+tkinter.S)
    # Partie 'Entrée'
    entreeFrame = LabelFrame(dataFrame, text='Entrée')
    # Abscisse
    Label(entreeFrame, text="X").grid(row=0, column=0)
    EntreeX = Scale(entreeFrame, to=LARGEUR_DEF-1, showvalue=False, orient='h', command=xEntreeCmd)
    EntreeX.grid(row=0, column=1)
    # Ordonnée
    Label(entreeFrame, text="Y").grid(row=1, column=0)
    EntreeY = Scale(entreeFrame, to=HAUTEUR_DEF-1, showvalue=False, orient='h', command=yEntreeCmd)
    EntreeY.grid(row=1, column=1)
    # Label Couleur
    CoulEntreeLbl = Label(entreeFrame, text="Couleur", bg=CoulEntree)
    CoulEntreeLbl.grid(row=2, column=0)
    # Bouton Couleur
    CoulEntreeBtn = Button(entreeFrame, text=CoulEntree, bg=CoulEntree, command=coulEntreeCmd)
    CoulEntreeBtn.grid(row=2, column=1)
    # Fin de la partie entreeFrame
    entreeFrame.grid(row=0, column=1, sticky=tkinter.N+tkinter.S)
    # Partie 'Sortie'
    sortieFrame = LabelFrame(dataFrame, text='Sortie')
    # Abscisse
    Label(sortieFrame, text="X").grid(row=0, column=0)
    SortieX = Scale(sortieFrame, to=LARGEUR_DEF-1, showvalue=False, orient='h', command=xSortieCmd)
    SortieX.grid(row=0, column=1)
    # Ordonnée
    Label(sortieFrame, text="Y").grid(row=1, column=0)
    SortieY = Scale(sortieFrame, to=HAUTEUR_DEF-1, showvalue=False, orient='h', command=ySortieCmd)
    SortieY.grid(row=1, column=1)
    # Label Couleur
    CoulSortieLbl = Label(sortieFrame, text="Couleur", bg=CoulSortie)
    CoulSortieLbl.grid(row=2, column=0)
    # Bouton Couleur
    CoulSortieBtn = Button(sortieFrame, text=CoulSortie, bg=CoulSortie, command=coulSortieCmd)
    CoulSortieBtn.grid(row=2, column=1)
    # Fin de la partie sortieFrame
    sortieFrame.grid(row=0, column=2, sticky=tkinter.N+tkinter.S)
    # Partie 'Algo'
    algoFrame = LabelFrame(dataFrame, text='Algorithme')
    # Main
    Label(algoFrame, text='Main').grid(row=0, column=0)
    Main = StringVar(root)
    Main.set(MAIN[0])
    OptionMenu(algoFrame, Main, *MAIN, command=mainCmd).grid(row=0, column=1)
    # Orientation
    Label(algoFrame, text='Orient.').grid(row=1, column=0)
    Orient = StringVar(root)
    Orient.set(ORIENTATION[0])
    OptionMenu(algoFrame, Orient, *ORIENTATION, command=orientationCmd).grid(row=1, column=1)
    # Bouton 'Démarrer'
    Button(algoFrame, text='Démarrer', command=demarrerCmd).grid(row=2, column=0)#, columnspan=2)
    # Scale 'Replay'
    Replay = Scale(algoFrame, showvalue=False, orient='h', command=replayCmd)
    Replay.grid(row=2, column=1)
    # Fin de la partie algoFrame
    algoFrame.grid(row=0, column=3, sticky=tkinter.N+tkinter.S)
    # Fin de la partie dataFrame et affichage
    dataFrame.grid(sticky=tkinter.W)
    # Fenêtre graphique (canvas)
    Wcanvas = Canvas(root, background="white", width=a_largeur, height=a_hauteur)
    # Fin de la partie Wcanvas et affichage
    Wcanvas.grid(row=1, column=0)
    return


# Replay de l'algorithme de sortie du labyrinthe
def replayCmd(a_val):
    if len(Chemin) > 0 :
        # Récupération de la valeur du scale
        pos = int(a_val)
        if pos < len(Chemin) :
            turtle.penup()
            (x, y) = centreHexa(Chemin[pos][0], Chemin[pos][1])
            turtle.goto(x, y)
    return


# Lancement de l'algorithme de sortie du labyrinthe (bouton 'Démarrer')
def demarrerCmd():
    global Heading
    # On retrace le labyrinthe (pour effacer les chemins turtle précédents si il y en a)
    traceGrilleHexa()
    # On trace !
    turtle.pendown()
    # Couleur du chemin
    turtle.pencolor(CouleurMurs[3])
    # Epaisseur du chemin
    turtle.pensize(TailleMurs[3])
    # Position de départ (attention pos = Entree ne marche pas)
    pos = [Entree[0], Entree[1]]
    # Nombre de cellules visitées
    cellules = 1
    # Mise à zéro du chemin
    Chemin.clear()
    # Première cellule
    Chemin.append((Entree[0], Entree[1]))
    # On cherche le premier mur dans la direction initiale
    cellules += toutDroit(pos)
    # Tant qu'on a pas trouvé la sortie on avance en suivant le mur
    while pos != Sortie :
        # On change l'orientation dans le sens de 'Main' jusqu'au mur libre
        for i in range(6) :
            # Si on ne peut pas avancer on change de direction
            if TabLaby[pos[0]][pos[1]][Heading] != PAROI :
                # Nouvelle orientation
                Heading = (Heading + Sens) % 6
                # Visualisation de l'orientation
                orientation()
            # On peut avancer dans cette direction
            else :
                # On avance dans la cellule suivante
                cellules += avance(pos)
                # Nouvelle orientation
                # Main gauche sur le mur : 0 => 2, 1 => 3, 2 => 4, 3 => 5, 4 => 0, 5 => 1
                # Main droite sur le mur : 0 => 4, 1 => 5, 2 => 0, 3 => 1, 4 => 2, 5 => 3
                Heading = (Heading + Sens + 3) % 6
                break
    # On a trouvé la sortie
    print('Nombre de cellules visitées :', cellules)
    # Le scale du replay doit aller de 0 à cellules
    Replay.configure(to=cellules+1)
    # Le replay est positionné à la sortie
    Replay.set(cellules)
    return


# Changement du choix de la main collée au mur (gauche => -1, droite => +1)
def mainCmd(a_val):
    global Sens
    # Sur main gauche collée au mur, Sens = -1 (on tourne vers la droite, sens montre)
    if a_val == MAIN[0] :
        Sens = -1
    # Sur main droite collée au mur, Sens = +1 (on tourne vers la gauche, sens trigo)
    else :
        Sens = 1
    return


# Changement du choix d'orientation de départ
def orientationCmd(a_val):
    global Heading
    # L'index 0 correspond à 30 degrés, le 5 à 330 °
    Heading = ORIENTATION.index(a_val)
    # Positionne la turtle en fonction de l'orientation
    orientation()
    return


# Changement de la position en abscisse de l'entrée du labyrinthe
def xEntreeCmd(a_val):
    global Entree
    # Récupération de l'abscisse de l'entrée
    Entree[0] = int(a_val)
    # On trace l'entrée avec la nouvelle valeur
    traceEntree()
    return


# Changement de la position en ordonnée de l'entrée du labyrinthe
def yEntreeCmd(a_val):
    global Entree
    # Récupération de l'ordonnée de l'entrée
    Entree[1] = int(a_val)
    # On trace l'entrée avec la nouvelle valeur
    traceEntree()
    return


# Changement de la position en abscisse de la sortie du labyrinthe
def xSortieCmd(a_val):
    global Sortie
    # Récupération de l'abscisse de la sortie
    Sortie[0] = int(a_val)
    # On trace la sortie avec la nouvelle valeur
    traceSortie()
    return


# Changement de la position en ordonnée de la sortie du labyrinthe
def ySortieCmd(a_val):
    global Sortie
    # Récupération de l'ordonnée de la sortie
    Sortie[1] = int(a_val)
    # On trace la sortie avec la nouvelle valeur
    traceSortie()
    return


# Lancement de la création du labyrinthe (bouton 'Créer')
def creerLabyCmd() :
    # Récupération de la largeur choisie
    Largeur = int(ValLargeur.get())
    # Récupération de la hauteur choisie
    Hauteur = int(ValHauteur.get())
    # Le scale en X doit aller de 0 à Largeur - 1
    EntreeX.configure(to=Largeur-1)
    # Le scale en Y doit aller de 0 à Hauteur - 1
    EntreeY.configure(to=Hauteur-1)
    # Le scale en X doit aller de 0 à Largeur - 1
    SortieX.configure(to=Largeur-1)
    # Le scale en Y doit aller de 0 à Hauteur - 1
    SortieY.configure(to=Hauteur-1)
    # Initialisation du labyrinthe
    init(Largeur, Hauteur)
    # Création du labyrinthe parfait aléatoirement
    creeLaby()
    # Tracé du labyrinthe
    traceGrilleHexa()
    # Valeur par défaut de la sortie : coin supérieur droit
    SortieX.set(Largeur-1)
    SortieY.set(Hauteur-1)
    return


# Callback du bouton pour la couleur entrée
def coulEntreeCmd() :
    global CoulEntree
    # Boîte de dialogue de choix de couleur
    coul = askcolor(CoulEntree)
    # Si une couleur est choisie
    if coul[1] != None :
        # Récupération de la couleur choisie
        CoulEntree = coul[1]
        # On utilise la couleur choisie comme couleur de fond du label
        CoulEntreeLbl.configure(bg=coul[1])
        # On utilise la couleur choisie comme couleur de fond du bouton
        CoulEntreeBtn.configure(bg=coul[1])
        # On retrace l'entrée avec la bonne couleur
        traceEntree()
    return


# Callback du bouton pour la couleur sortie
def coulSortieCmd() :
    global CoulSortie
    # Boîte de dialogue de choix de couleur
    coul = askcolor(CoulSortie)
    # Si une couleur est choisie
    if coul[1] != None :
        # Récupération de la couleur choisie
        CoulSortie = coul[1]
        # On utilise la couleur choisie comme couleur de fond du label
        CoulSortieLbl.configure(bg=coul[1])
        # On utilise la couleur choisie comme couleur de fond du bouton
        CoulSortieBtn.configure(bg=coul[1])
        # On retrace la sortie avec la bonne couleur
        traceSortie()
    return


# Positionne l'orientation de la 'turtle'
def orientation() :
    # Orientation de la turtle
    turtle.setheading(30 + Heading * 60)
    return


# Initialisation de turtle
def initTurtle() :
    global InitTurtle
    # Initialisation de Turtle si pas déjà fait
    if not InitTurtle :
        # Tracé avec Tk : on trace dans le canvas
        if TK :
            from turtle import RawPen
            global turtle
            turtle = RawPen(Wcanvas)
        else :
        # Tracé sans Tk : création de la fenêtre et titre
            turtle.title(TITRE + VERSION)
        # Cache le pointeur de Turtle
        turtle.hideturtle()
        # Vitesse maximale du tracé
        turtle.speed(0)
        # Orientation initiale : Nord-Est
        orientation()
        # Turtle est maintenant initialisé
        InitTurtle = True
    # Turtle est déjà initialisé : on nettoie la fenêtre
    else :
        turtle.clear()
    return


# Tracé d'un hexagone entier
# a_x : abscisse du centre de l'hexagone (en pixels)
# a_y : ordonnée du centre de l'hexagone (en pixels)
# a_type : type de mur (MUR_EXT, MUR_INT, PAROI)
def traceHexa(a_x, a_y, a_type) :
    # On lève le stylo
    turtle.up()
    # On va au coin droit de l'hexagone
    turtle.goto(a_x + DemiLargeurHexa,     a_y)
    # On abaisse le stylo
    turtle.down()
    # On trace le premier segment (dans le sens trigo) : mur 0
    turtle.pensize(TailleMurs[a_type[0]])
    turtle.pencolor(CouleurMurs[a_type[0]])              
    turtle.goto(a_x + DemiLargeurHexa / 2, a_y + DemiLargeurHexa * RACINE3_2)
    # On trace le deuxième segment (dans le sens trigo) : mur 1
    turtle.pensize(TailleMurs[a_type[1]])
    turtle.pencolor(CouleurMurs[a_type[1]])
    turtle.goto(a_x - DemiLargeurHexa / 2, a_y + DemiLargeurHexa * RACINE3_2)
    # On trace le troisième segment (dans le sens trigo) : mur 2
    turtle.pensize(TailleMurs[a_type[2]])
    turtle.pencolor(CouleurMurs[a_type[2]])
    turtle.goto(a_x - DemiLargeurHexa,     a_y)
    # On trace le quatrième segment (dans le sens trigo) : mur 3
    turtle.pensize(TailleMurs[a_type[3]])
    turtle.pencolor(CouleurMurs[a_type[3]])
    turtle.goto(a_x - DemiLargeurHexa / 2, a_y - DemiLargeurHexa * RACINE3_2)
    # On trace le cinquième segment (dans le sens trigo) : mur 4
    turtle.pensize(TailleMurs[a_type[4]])
    turtle.pencolor(CouleurMurs[a_type[4]])
    turtle.goto(a_x + DemiLargeurHexa / 2, a_y - DemiLargeurHexa * RACINE3_2)
    # On trace le sixième segment (dans le sens trigo) : mur 5
    turtle.pensize(TailleMurs[a_type[5]])
    turtle.pencolor(CouleurMurs[a_type[5]])
    turtle.goto(a_x + DemiLargeurHexa,     a_y)
    return


# Tracé du bas (mur 4) d'un hexagone
# a_x : abscisse du centre de l'hexagone (en pixels)
# a_y : ordonnée du centre de l'hexagone (en pixels)
# a_type : type de mur (MUR_EXT, MUR_INT, PAROI)
def traceBasHexa(a_x, a_y, a_type) :
    # On lève le stylo
    turtle.up()
    # On va au cinquième segment (dans le sens trigo)
    turtle.goto(a_x - DemiLargeurHexa / 2, a_y - DemiLargeurHexa * RACINE3_2)
    # On abaisse le stylo
    turtle.down()
    # On trace le cinquième segment (dans le sens trigo) : mur 4
    turtle.pensize(TailleMurs[a_type])
    turtle.pencolor(CouleurMurs[a_type])
    turtle.goto(a_x + DemiLargeurHexa / 2, a_y - DemiLargeurHexa * RACINE3_2)
    return


# Initialisation du graphique et du labyrinthe
# a_largeur : largeur du labyrinthe
# a_hauteur : hauteur du labyrinthe
def init(a_largeur, a_hauteur):
    # Initialisation de turtle
    initTurtle()
    # Initialisation du tableau des données
    initDonnees(a_largeur, a_hauteur)


"""
Nombre de murs 'internes' :
    parois horizontales : (H - 1) * L
    parois inclinées    : (2 * H - 1) * (L - 1)
    Parois totales : (H - 1) * L + (2 * H - 1) * (L - 1) = 3HL -2(H+L) + 1
"""
# Calcul du nombre de parois internes en fonction de la taille du labyrinthe
def nbParoisInternes(a_large, a_haut) :
      return (3 * a_large * a_haut - 2 * (a_large + a_haut) + 1)


# Tracé d'une grille d'hexagones centrés
def traceGrilleHexa():
    # Initialisation pour calcul du temps de tracé
    tps = time.time()
    # Désactive l'animation de tracé (pour accelérer le tracé du labyrinthe)
    screen = turtle.getscreen()
    screen.tracer(0)
    # Nettoie l'écran
    turtle.clear()
    # Cache la 'turtle'
    turtle.hideturtle()
    # Boucle de tracé des cellules
    for i in range(Largeur) :
        for j in range(Hauteur) :
            # Calcul de la position du centre de la cellule
            (x, y) = centreHexa(i, j)
            if i % 2 == 0 or i == Largeur - 1 or j == Hauteur - 1 :
                # Tracé complet de la cellule
                traceHexa(x, y, TabLaby[i][j])
            else :
                # Tracé du bas de la cellule
                traceBasHexa(x, y, TabLaby[i][j][4])
    # Affichage du temps de tracé
    print("traceGrilleHexa(", Largeur, ", ", Hauteur, ") : tracé en ", round(time.time() - tps, 2), " s", sep='')
    # Active l'animation de tracé
    screen.tracer(1)
    # Trace l'entrée
    traceEntree()
    # Trace la sortie
    traceSortie()
    # Positionnement de la turtle
    orientationCmd(ORIENTATION[0])
    return


# Calcule la position du centre d'une cellule (coordonnées turtle, axe des ordonnées orienté vers le haut)
def centreHexa(a_i, a_j) :
    # Décalage en abscisse : (DemiLargeurHexa + DemiLargeurHexa * cos(60)) * i
    # Décalage en ordonnée : 2 * DemiLargeurHexa * sin(60) * j pour les abscisses paires, + DemiLargeurHexa * sin(60) pour les impaires
    x = 1.5 * DemiLargeurHexa * a_i - DemiLargeurTotale
    y = DemiLargeurHexa * (2 * RACINE3_2 * a_j + RACINE3_2 * (a_i % 2)) - DemiHauteurTotale
    return (x, y)


# Initialise le tableau de données du labyrinthe
# a_largeur : largeur du labyrinthe (nombre d'hexagones en abscisse)
# a_hauteur : hauteur du labyrinthe (nombre d'hexagones en ordonnée)
def initDonnees(a_largeur, a_hauteur):
    global Largeur, Hauteur, TabLaby, Sortie, DemiLargeurTotale, DemiHauteurTotale
    # Initialisation de la largeur
    Largeur = a_largeur
    # Initialisation de la hauteur
    Hauteur = a_hauteur
    # Position de la sortie au coin opposé à l'entrée
    Sortie = [Largeur - 1, Hauteur - 1]
    # Initialisation du tableau des données (NBR_HEXA valeurs par hexagone)
    TabLaby = [[[0 for _ in range(NBR_HEXA)] for _ in range(a_hauteur)] for _ in range(a_largeur)]
    # Affectation du type de paroi pour les murs externes
    for i in range(a_largeur) :
        for j in range(a_hauteur) :
            for k in range(NBR_HEXA) :
                # Intérieur (on positionne des murs internes partout)
                for k in range(6) :
                    TabLaby[i][j][k] = MUR_INT
                # Coin bas gauche
                if i == 0 and j == 0 :
                    TabLaby[i][j][2] = TabLaby[i][j][3] = TabLaby[i][j][4] = TabLaby[i][j][5] = MUR_EXT
                # Coin haut gauche
                elif i == 0 and j == a_hauteur - 1 :
                    TabLaby[i][j][1] = TabLaby[i][j][2] = TabLaby[i][j][3] = MUR_EXT
                # Coin bas droit
                elif i == a_largeur - 1 and j == 0 :
                    TabLaby[i][j][0] = TabLaby[i][j][4] = TabLaby[i][j][5] = MUR_EXT
                    if i % 2 == 0 :
                        TabLaby[i][j][3] = MUR_EXT                       
                # Coin haut droit
                elif i == a_largeur - 1 and j == a_hauteur - 1 :
                    TabLaby[i][j][0] = TabLaby[i][j][1] = TabLaby[i][j][5] = MUR_EXT
                    if i % 2 == 1 :
                        TabLaby[i][j][2] = MUR_EXT                    
                # Bord gauche
                elif i == 0 :
                    TabLaby[i][j][2] = TabLaby[i][j][3] = MUR_EXT
                # Bord droit :
                elif i == a_largeur - 1:
                    TabLaby[i][j][0] = TabLaby[i][j][5] = MUR_EXT
                # Bord bas
                elif j == 0 :
                    TabLaby[i][j][4] = MUR_EXT
                    if i % 2 == 0 :
                        TabLaby[i][j][3] = TabLaby[i][j][5] = MUR_EXT
                # Bord haut
                elif j == a_hauteur - 1:
                    TabLaby[i][j][1] = MUR_EXT
                    if i % 2 == 1 :
                        TabLaby[i][j][0] = TabLaby[i][j][2] = MUR_EXT                    
    # Moitié de la largeur totale (décalage pour centrage de la grille en largeur)
    DemiLargeurTotale = (a_largeur * DemiLargeurHexa * 1.5 + DemiLargeurHexa / 2) / 2
    # Moitié de la hauteur totale (décalage pour centrage de la grille en hauteur)
    DemiHauteurTotale = DemiLargeurHexa * (2 * RACINE3_2 * a_hauteur + RACINE3_2) / 2
    # Décalage en abscisse
    DemiLargeurTotale -= DemiLargeurHexa
    # Décalage en ordonnée
    DemiHauteurTotale -= DemiLargeurHexa * RACINE3_2
    return


# Calcul de la somme des valeurs des cellules
def sommeCellules() :
    somme = 0
    for i in range(Largeur) :
        for j in range(Hauteur) :
            somme += TabLaby[i][j][6]
    return somme

    
# Algorithme de création d'un labyrinthe :
# 1 : on affecte des numéros croissants à chaque cellule (en commençant à 0)
# 2 : tant que la somme des valeurs des cellules est supérieure à 0
#   - on supprime un mur interne (existant) aléatoirement qui sépare 2 cellules de valeurs différentes
#   - on affecte la valeur minimale des 2 cellules concernées aux cellules de valeur maximale
def creeLaby() :
    # Valeur à mettre dans la cellule
    val = 0
    # Affectation du type de paroi pour les murs externes
    for i in range(Largeur) :
        for j in range(Hauteur) :
            TabLaby[i][j][6] = val
            # On incrémente la valeur
            val += 1
    # On a nbMurCibles murs internes destructibles (* 2 pour les 2 côtés du mur possibles)
    nbMursCibles = 2 * nbParoisInternes(Largeur, Hauteur)
    # La somme des valeurs de cellule devra être nulle
    while sommeCellules() != 0 :
        if Debug : print(TabLaby)
        # Choix d'un mur cible à détruire
        murCible = random.randrange(nbMursCibles)
        if Debug : print('nbMursCibles =', nbMursCibles, ' somme =', sommeCellules(), ' cible =', murCible)
        # nbMur : nombre de murs internes
        nbMurs = 0
        # On recherche le mur cible
        for i in range(Largeur) :
            for j in range(Hauteur) :
                for k in range(6) :
                    # Si on trouve un mur interne
                    if TabLaby[i][j][k] == MUR_INT : 
                        # Cellule voisine
                        v_i, v_j, v_k = voisin(i, j, k)
                        # Si les 2 cellules ne sont pas déjà reliées
                        if TabLaby[i][j][6] != TabLaby[v_i][v_j][6] :
                            # Si c'est le mur cible
                            if nbMurs == murCible :
                                if Debug : print(i, j, k, v_i, v_j, v_k)
                                # On le détruit
                                TabLaby[i][j][k] = PAROI
                                # On détruit aussi le mur voisin (l'autre côté de la paroi)
                                TabLaby[v_i][v_j][v_k] = PAROI
                                # Valeurs minimales et maximales des 2 cellules
                                if TabLaby[i][j][6] < TabLaby[v_i][v_j][6] :
                                    valMin = TabLaby[i][j][6]
                                    valMax = TabLaby[v_i][v_j][6]
                                else :
                                    valMin = TabLaby[v_i][v_j][6]
                                    valMax = TabLaby[i][j][6]
                                # Recalcul des valeurs de cellules et du nombre de murs cibles
                                nbMursCibles = 0
                                for m in range(Largeur) :
                                    for n in range(Hauteur) :
                                        # On affecte la valeur min aux cellules de valeur max
                                        if TabLaby[m][n][6] == valMax :
                                            TabLaby[m][n][6] = valMin
                                        # Calcul du nombre de murs 
                                        for o in range(6) :
                                            if TabLaby[m][n][o] == MUR_INT :
                                                v_m, v_n, v_o = voisin(m, n, o)
                                                if TabLaby[m][n][6] != TabLaby[v_m][v_n][6] :
                                                    nbMursCibles += 1
                                if Debug and nbMursCibles % 2 == 1 :
                                    nbMursCibles = 0
                                    for m in range(Largeur) :
                                        for n in range(Hauteur) :
                                            for o in range(6) :
                                                if TabLaby[m][n][o] == MUR_INT :
                                                    v_m, v_n, v_o = voisin(m, n, o)
                                                    if TabLaby[m][n][6] != TabLaby[v_m][v_n][6] :
                                                        nbMursCibles += 1
                                                        print(m, n, o, v_m, v_n, v_o)
                            # On incrémente pour savoir sur quel mur cible potentiel on est
                            nbMurs += 1
    return


# Calcul le mur voisin d'un mur donné (l'autre face du mur)
# a_i : abscisse de l'hexagone (indice)
# a_j : ordonnée de l'hexagone (indice)
# a_k : rang du mur (0 = NE, 1 = N, 2 = NO, 3 = SO, 4 = S, 5 = SE)
# Return : triplet de définition (i, j, k) du mur 'voisin' (k = -1 si pas de voisin)
def voisin(a_i, a_j, a_k) :
    # Sur les bords il n'y a pas de voisin
    if a_i == 0 and (a_k == 2 or a_k == 3) or a_i == Largeur - 1 and (a_k == 0 or a_k == 5) :
        # Indicateur voisin inexistant
        k = -1
    # Indices des abscisses et ordonnées de l'hexagone voisin
    else :
        # Voisin direction Nord-Est
        if a_k == 0 :
            i = a_i + 1
            j = a_j
            if i % 2 == 0 : j += 1
        # Voisin direction Nord
        elif a_k == 1 :
            i = a_i
            j = a_j + 1
        # Voisin direction Nord-Ouest
        elif a_k == 2 :
            i = a_i - 1
            j = a_j
            if i % 2 == 0 : j += 1
        # Voisin direction Sud-Ouest
        elif a_k == 3 :
            i = a_i - 1
            j = a_j
            if i % 2 == 1 : j -= 1
        # Voisin direction Sud
        elif a_k == 4 :
            i = a_i 
            j = a_j - 1
        # Voisin direction Sud-Est
        else :
            i = a_i + 1
            j = a_j
            if i % 2 == 1 : j -= 1
        # Indice du mur de l'hexagone voisin
        k = (a_k + 3) % 6
    return (i, j, k)


# On avance d'une cellule à partir de la position a_pos dans la direction Heading
# a_pos : position initiale
# Return : nombre de cellules visitées
def avance(a_pos) :
    global Chemin
    # On cherche le voisin
    (i, j, k) = voisin(a_pos[0], a_pos[1], Heading)
    # On va jusqu'au centre suivant
    turtle.goto(centreHexa(i, j))
    # On se positionne à la nouvelle cellule
    a_pos[0] = i
    a_pos[1] = j
    # Sauvegarde de la position
    Chemin.append((a_pos[0], a_pos[1]))
    return 1


# On avance jusqu'au mur ou la sortie à partir de la position a_pos dans la direction Heading
# a_pos : position initiale
# Return : nombre de cellules visitées
def toutDroit(a_pos) :
    # cellules visitées
    cellules = 0
    # Si on n'est pas à la sortie et si pas de mur dans la direction choisie
    while a_pos != Sortie and TabLaby[a_pos[0]][a_pos[1]][Heading] == PAROI :
        # On avance d'une cellule
        cellules += avance(a_pos)
    return cellules


# Trace l'entrée du labyrinthe
def traceEntree() :
    # On enleve le dessin d'entrée si il existe
    traceSymbole(Entree[0], Entree[1], TAG_ENTREE, CoulEntree)
    # Au cas où il y a superposition on retrace la sortie qui est au-dessus
    if Sortie == Entree :
        traceSortie()
    return


# Trace la sortie du labyrinthe
def traceSortie() :
    # On enleve le dessin d'entrée si il existe
    traceSymbole(Sortie[0], Sortie[1], TAG_SORTIE, CoulSortie)
    return


# Tracé d'un symbole dans l'hexagone
# a_largeur : rang en abscisse de l'hexagone
# a_hauteur : rang en ordonnée de l'hexagone
# a_symbole : symbole pour identifier et pouvoir effacer
# a_color   : couleur du tracé
def traceSymbole(a_largeur, a_hauteur, a_symbole, a_color) :
    if InitTurtle :
        # Position du centre
        (x, y) = centreHexa(a_largeur, a_hauteur)
        # Rayon de la sortie plus petit (il est tracé après l'entrée, cela permet de voir les 2 si superposés)
        if a_symbole == TAG_SORTIE :
            rayon = DemiLargeurHexa / 3
        # Rayon
        else : 
            rayon = DemiLargeurHexa / 2
        # Tracés avec tag sur le canvas de Tk
        if Wcanvas != 0 :
            # On enleve le symbole si il existe
            Wcanvas.delete(a_symbole)
            # Tracé du symbole
            Wcanvas.create_rectangle(x - rayon, -y - rayon, x + rayon, -y + rayon, fill=a_color, tags=a_symbole)
            # Pour l'entrée : on visualise la 'turtle'
            if a_symbole == TAG_ENTREE :
                # Orientation de la 'turtle'
                orientation()
                # On lève le stylo
                turtle.penup()
                # On va au centre de la cellule
                turtle.goto(x, y)
                # Affichage de la 'turtle'
                turtle.showturtle()
        # Tracé sur turtle sans Tk
        else :
            # Pas de tracé
            turtle.penup()
            # On va au centre de la cellule
            turtle.goto(x, y - rayon)
            # Couleur du symbole
            turtle.pencolor(a_color)
            # Tracé
            turtle.pendown()
            # Tracé du symbole
            turtle.setheading(0)
            turtle.circle(rayon, steps=4)
            # Pour l'entrée : on visualise la 'turtle' après la tracé de la sortie
            if a_symbole == TAG_SORTIE :
                # Position du centre
                (x, y) = centreHexa(Entree[0], Entree[1])
                # Orientation de la 'turtle'
                orientation()
                # On lève le stylo
                turtle.penup()
                # On va au centre de la cellule
                turtle.goto(x, y)
                # Affichage de la 'turtle'
                turtle.showturtle()
    return


# Test du labyrinthe : création de la fenêtre et du labyrinthe
# a_largeur : largeur du labyrinthe
# a_hauteur : hauteur du labyrinthe
def testLaby(a_largeur = LARGEUR_DEF, a_hauteur = HAUTEUR_DEF) :
    # Tracé avec interface Tk
    if TK :
        creeInterface()
    # Tracé uniquement avec turtle
    else :
        init(a_largeur, a_hauteur)
        creeLaby()
        traceGrilleHexa()
    return


#-------------------------------------------------------------------------------
# Appel lors de l'exécution du programme
if __name__ == '__main__':
    # Affichage des informations
    info()
    # Démarrage du projet
    testLaby()

