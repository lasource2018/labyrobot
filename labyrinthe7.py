# Pour fonctions mathématiques (sqrt, degrees, atan2)
import math
# Pour tracé graphique
import turtle
# Pour calcul de temps / performances
import time
# Pour nombre aléatoire
import random
# Pour Interface Homme-Machine Tk
from tkinter import Tk, Canvas, Label, LabelFrame, Entry, Scale, Button, Frame, StringVar, OptionMenu
from tkinter.messagebox import showinfo, showerror
from tkinter.colorchooser import askcolor
import tkinter.constants


# ------------------------------------------------------------------------------
# Constantes NON modifiables 

# Racine de 3 sur 2 = sinus(60°)
RACINE3_2 = math.sqrt(3) / 2

# Nombre de données par hexagone : 1 pour chaque côté (6) + 1 pour les calculs = 7
NBR_HEXA = 7

# Valeur de la donnée d'un côté de l'hexagone pour un mur externe
MUR_EXT = 0

# Valeur de la donnée d'un côté de l'hexagone pour un mur interne (fermé)
MUR_INT = 1

# Valeur de la donnée d'un côté de l'hexagone pour une ouverture
OUVERTURE = 2

# Index du chemin dans les tableaux de couleur et d'épaisseur
CHEMIN = 3


# ------------------------------------------------------------------------------
# Paramètres modifiables 

# Titre du projet
TITRE = "Projet Labyrinthe"

# Version
VERSION = " v1.7"

# Utilisation de l'interface TK (sinon on utilise seulement turtle)
TK = True

# Texte d'aide
AIDE = \
"""
Zone 'Labyrinthe' :
    Entrer la largeur et la hauteur souhaitées du labyrinthe
    puis cliquer sur 'Créer'
    L'ascenseur 'Taille hexa' permet de changer la taille des hexagones
Les zones 'Entrée' et 'Sortie' permettent de changer couleur et position de l'entrée et de la sortie
Zone 'Algorithme' :
    Le choix 'Main' définit quelle main est posée sur le mur
    Le choix 'Orientation' définit l'orientation initiale
    Le choix 'Vitesse' définit la vitesse de tracé du chemin
    Le bouton 'Démarrer' lance la recherche de sortie, il n'est actif que si un labyrinthe a été créé
    L'ascenseur 'Chemin' permet de visualiser la succession des hexagones traversés
""" \
if TK else \
"""
Commandes :
    testLaby(largeur, hauteur) : crée et trace un labyrinthe de dimensions (largeur, hauteur)
    traceGrilleHexa() : retrace le labyrinthe
    demarrerCmd() : lance la résolution du labyrinthe
    changeMur(i, j, k) : échange le type de mur entre MUR_INT et OUVERTURE
    tailleCmd(taille) : change la taille des hexagones et retrace le labyrinthe
    Sens : -1 pour main gauche, +1 pour main droite contre le mur
    Entree : position de l'entrée dans le labyrinthe (par défaut coin inférieur gauche [0, 0])
    Sortie : position de la sortie dans le labyrinthe (défaut coin supérieur droit [Largeur-1, Hauteur-1])
    CoulEntree : couleur de l'entrée (#RRGGBB)
    CoulSortie : couleur de la sortie (#RRGGBB)
    Vitesse : vitesse du tracé de chemin (-1 : variable, 0 : max, croissante de 1 à 10)
"""

# Largeurs et hauteurs minimales du labyrinthe (en cellules)
LARG_HAUT_MIN = 2

# Largeurs et hauteurs maximales du labyrinthe (en cellules)
LARG_HAUT_MAX = 60

# Largeur par défaut du labyrinthe (en cellules)
LARGEUR_DEF = 10

# Hauteur par défaut du labyrinthe (en cellules)
HAUTEUR_DEF = 10

# Largeur par défaut (en pixels) de la partie du tracé du labyrinthe
LARGEUR_FEN = 765

# Hauteur par défaut (en pixels) de la partie du tracé du labyrinthe
HAUTEUR_FEN = 600

# Hauteur de la zone de menus (en pixels)
HAUTEUR_MENU = 105

# Tag de l'entrée
TAG_ENTREE = "Entree_tag"

# Tag de la sortie
TAG_SORTIE = "Sortie_tag"

# Tag du chemin
TAG_CHEMIN = "Chemin_tag"

# Label pour la main gauche
MAIN_GAUCHE = "Gauche"

# Label pour la main droite
MAIN_DROITE = "Droite"

# Main (quelle main sera posée sur le mur)
MAIN = (MAIN_GAUCHE, MAIN_DROITE)

# Orientation initiale (correspond aux directions, ne pas changer l'ordre)
ORIENTATION = ("NordEst", "Nord", "NordOuest", "SudOuest", "Sud", "SudEst")

# Epaisseur des traits (mur externe, mur interne, ouverture, chemin)
EPAISSEUR_LABY = (3, 2, 1, 2)

# Couleurs du tracé en fonction du type (mur externe, mur interne, ouverture, chemin)
COULEUR_LABY = ('black', 'blue', 'pink', 'orange')

# Libellés des choix de vitesses
VITESSE_TXT = ('Variable', 'Lente', 'Moyenne', 'Rapide', 'Max')

# Valeurs des vitesses correspondantes aux libellés de VITESSE_TXT
# A part -1 qui indique une vitesse variable, les autres valeurs sont celles de turtle.speed()
VITESSE_VAL = (        -1,       3,         6,        9,     0)

# Index de la valeur par défaut dans la liste VITESSE_TXT (valeur maximale : len(VITESSE_TXT) - 1)
VITESSE_DEF = 0

# Taille minimale des cellules (en pixels)
CELLULE_MIN = 15

# Taille initiale des cellules (en pixels)
CELLULE_INI = 20

# Taille maximale des cellules (en pixels)
CELLULE_MAX = 35

# Coefficient multiplicatif du nombre total de cellules pour déterminer le nombre de cellules visitables
MULT_CELLULES = 2


# ------------------------------------------------------------------------------
# Variables globales

# Etat de l'initialisation de Turtle
InitTurtle = False

# Demi-largeur d'un hexagone (en pixels)
DemiTailleHexa = CELLULE_INI

# Tableau des états des côtés (6 valeurs) et de la cellule (1 valeur) : total 7 données par cellule
TabLaby = [[[0] * NBR_HEXA] * 1] * 1

# Largeur du labyrinthe (en cellules)
Largeur = 0

# Hauteur du labyrinthe (en cellules)
Hauteur = 0

# Demi largeur et hauteur totales
DemiLargeurTotale = DemiHauteurTotale = 0

# Impressions additionnelles pour le debug
Debug = False

# Position de l'entrée du labyrinthe (coin bas gauche au départ)
Entree = [0, 0]

# Position de la sortie du labyrinthe (coin haut droite à la création du labyrinthe)
Sortie = [0, 0]

# Couleur entrée (#RRGGBB)
CoulEntree = "#00FF00"

# Couleur sortie (#RRGGBB)
CoulSortie = "#FF0000"

# Orientation de la 'turtle' : 0 = 30°, 1 = 90°, 2 = 150°, 3 = 210°, 4 = 270°, 5=330°
Orientation = 0

# Vitesse de la turtle
Vitesse = VITESSE_VAL[VITESSE_DEF]

# Nouvelle orientation testée : +1 si main droite, -1 si main gauche
# La valeur initiale doit être cohérente avec MAIN[0]
# Si c'est main gauche, on tourne vers la droite pour mettre la main gauche au mur
# Si c'est main droite, on tourne vers la gauche pour mettre la main droite au mur
Sens = -1 if MAIN[0] == MAIN_GAUCHE else 1

# Chemin trouvé (liste des cellules traversées)
Chemin = []

# Widget canvas pour le tracé du labyrinthe sous Tk
Wcanvas = 0

# Widget de base de la fenêtre
Wroot = 0

# Largeurs et hauteurs de la partie graphique (canvas)
LargeurCanvas = HauteurCanvas = LargeurCible = HauteurCible = 0

# Nombre de murs internes (initial, ajoutés, retirés, maximum)
MursInit = MursPlus = MursMoins = MursMax = 0


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
    # Variables globales de type entier
    global LargeurCanvas, HauteurCanvas, LargeurCible, HauteurCible
    # Variables globales de type Widget Tk
    global Wroot, Wcanvas
    # Variables globales de type StringVar Tk
    global VarLargeur, VarHauteur, VarOrient
    # Variables globales de type Scale Tk
    global ScaEntreeX, ScaEntreeY, ScaSortieX, ScaSortieY, ScaChemin
    # Variables globales de type Label Tk
    global LblCoulEntree, LblCoulSortie
    # Variables globales de type Button Tk
    global BtnCoulEntree, BtnCoulSortie, BtnDemarrer
    # Fenêtre principale
    Wroot = Tk()
    # Titre de la fenêtre
    majTitre()
    # Initialisation de la largeur et hauteur du graphique (et de la sauvegarde utilisée pour resize)
    LargeurCible = LargeurCanvas = a_largeur
    HauteurCible = HauteurCanvas = a_hauteur
    # Définition de la taille de la fenêtre principale
    Wroot.geometry(str(a_largeur)+"x"+str(a_hauteur+HAUTEUR_MENU)+"-10+10")
    # Fonction appelée pour le changement de taille de la fenêtre
    Wroot.bind('<Configure>', retailleFenetre)
    # Fonction appelée pour le lacher du bouton souris (indique la fin du resize)
    Wroot.bind('<ButtonRelease>', clicSouris)
    # Frame des données
    dataFrame = Frame(Wroot)
    # Partie 'Labyrinthe'
    labyFrame = LabelFrame(dataFrame, text='Labyrinthe')
    # Première ligne : largeur du labyrinthe
    Label(labyFrame, text='Largeur').grid(row=0, column=0)
    VarLargeur = StringVar(Wroot)
    VarLargeur.set(LARGEUR_DEF)
    Entry(labyFrame, textvariable=VarLargeur, width=2).grid(row=0, column=1)
    # Deuxième ligne : hauteur du labyrinthe
    Label(labyFrame, text='Hauteur').grid(row=1, column=0)
    VarHauteur = StringVar(Wroot)
    VarHauteur.set(HAUTEUR_DEF)
    Entry(labyFrame, textvariable=VarHauteur, width=2).grid(row=1, column=1)
    # Troisième ligne : bouton 'Créer'
    Button(labyFrame, text='Créer', command=creerLabyCmd).grid(row=2, column=0, columnspan=1)
    # Troisième ligne : scale de changement de taille
    scaTaille = Scale(labyFrame, from_=CELLULE_MIN, to=CELLULE_MAX, showvalue=False, orient='h', label='Taille hexa', command=tailleCmd)
    scaTaille.set(CELLULE_INI)
    scaTaille.grid(row=2, column=1)
    # Fin de la partie labyFrame
    labyFrame.grid(row=0, column=0, sticky=tkinter.N+tkinter.S)
    # Partie 'Entrée'
    entreeFrame = LabelFrame(dataFrame, text='Entrée')
    # Abscisse
    Label(entreeFrame, text="X").grid(row=0, column=0)
    ScaEntreeX = Scale(entreeFrame, to=LARGEUR_DEF-1, showvalue=False, orient='h', command=xEntreeCmd)
    ScaEntreeX.grid(row=0, column=1)
    # Ordonnée
    Label(entreeFrame, text="Y").grid(row=1, column=0)
    ScaEntreeY = Scale(entreeFrame, to=HAUTEUR_DEF-1, showvalue=False, orient='h', command=yEntreeCmd)
    ScaEntreeY.grid(row=1, column=1)
    # Label Couleur
    LblCoulEntree = Label(entreeFrame, text='Couleur', bg=CoulEntree)
    LblCoulEntree.grid(row=2, column=0)
    # Bouton Couleur
    BtnCoulEntree = Button(entreeFrame, text=CoulEntree, bg=CoulEntree, command=coulEntreeCmd)
    BtnCoulEntree.grid(row=2, column=1)
    # Fin de la partie entreeFrame
    entreeFrame.grid(row=0, column=1, sticky=tkinter.N+tkinter.S)
    # Partie 'Sortie'
    sortieFrame = LabelFrame(dataFrame, text='Sortie')
    # Abscisse
    Label(sortieFrame, text="X").grid(row=0, column=0)
    ScaSortieX = Scale(sortieFrame, to=LARGEUR_DEF-1, showvalue=False, orient='h', command=xSortieCmd)
    ScaSortieX.grid(row=0, column=1)
    # Ordonnée
    Label(sortieFrame, text="Y").grid(row=1, column=0)
    ScaSortieY = Scale(sortieFrame, to=HAUTEUR_DEF-1, showvalue=False, orient='h', command=ySortieCmd)
    ScaSortieY.grid(row=1, column=1)
    # Label Couleur
    LblCoulSortie = Label(sortieFrame, text='Couleur', bg=CoulSortie)
    LblCoulSortie.grid(row=2, column=0)
    # Bouton Couleur
    BtnCoulSortie = Button(sortieFrame, text=CoulSortie, bg=CoulSortie, command=coulSortieCmd)
    BtnCoulSortie.grid(row=2, column=1)
    # Fin de la partie sortieFrame
    sortieFrame.grid(row=0, column=2, sticky=tkinter.N+tkinter.S)
    # Partie 'Algo'
    algoFrame = LabelFrame(dataFrame, text='Algorithme')
    # Main
    Label(algoFrame, text='Main').grid(row=0, column=0)
    varMain = StringVar(Wroot)
    varMain.set(MAIN[0])
    OptionMenu(algoFrame, varMain, *MAIN, command=mainCmd).grid(row=0, column=1)
    # Orientation
    Label(algoFrame, text='Orientation').grid(row=1, column=0)
    VarOrient = StringVar(Wroot)
    VarOrient.set(ORIENTATION[0])
    OptionMenu(algoFrame, VarOrient, *ORIENTATION, command=orientationCmd).grid(row=1, column=1)
    # Vitesse
    Label(algoFrame, text='Vitesse').grid(row=2, column=0)
    VarVitesse = StringVar(Wroot)
    VarVitesse.set(VITESSE_TXT[VITESSE_DEF])
    OptionMenu(algoFrame, VarVitesse, *VITESSE_TXT, command=vitesseCmd).grid(row=2, column=1)
    # Bouton 'Démarrer'
    BtnDemarrer = Button(algoFrame, text='Démarrer', command=demarrerCmd, state='disabled')
    BtnDemarrer.grid(row=0, column=2, rowspan=2)
    # Scale 'Chemin'
    ScaChemin = Scale(algoFrame, showvalue=False, orient='h', label='Chemin', command=cheminCmd)
    ScaChemin.grid(row=2, column=2)
    # Fin de la partie algoFrame
    algoFrame.grid(row=0, column=3, sticky=tkinter.N+tkinter.S)
    # Fin de la partie dataFrame et affichage
    dataFrame.grid(row=0, column=0)
    # Fenêtre graphique (canvas)
    Wcanvas = Canvas(Wroot, background='white', width=a_largeur, height=a_hauteur)
    # Fin de la partie Wcanvas et affichage
    Wcanvas.grid(row=1, column=0)
    return


# Changement du choix de la main collée au mur (gauche => -1, droite => +1)
# a_val : valeur du menu choisie
def vitesseCmd(a_val) :
    global Vitesse
    if Debug : print('vitesseCmd :', a_val, '/ index :', VITESSE_TXT.index(a_val), '/ vitesse :', VITESSE_VAL[VITESSE_TXT.index(a_val)])
    Vitesse = VITESSE_VAL[VITESSE_TXT.index(a_val)]
    return


# Modification de la taille des hexagones
# a_val : valeur du scale (demi taille des hexagones)
def tailleCmd(a_val) :
    global DemiTailleHexa
    DemiTailleHexa = int(a_val)
    # Recalcul et retracé du labyrinthe s'il existe
    if InitTurtle :
        initCentrage()
        traceGrilleHexa()
    return


# Gestion du changement de taille de la fenêtre (événement 'Configure')
# a_evt : événement déclencheur
def retailleFenetre(a_evt) :
    global LargeurCible, HauteurCible
    # On sauve les valeurs des événements 'configure' de l'utilisateur (générés par Wroot)
    if a_evt.widget == Wroot :
        if a_evt.width != LargeurCanvas or a_evt.height != HauteurCanvas + HAUTEUR_MENU :
            if Debug : print('retailleFenetre', a_evt.width, a_evt.height)
            if a_evt.width > 1 :
                LargeurCible = a_evt.width
                HauteurCible = a_evt.height - HAUTEUR_MENU
    return


# Fin du changement de taille de la fenêtre (événement 'ButtonRelease')
# a_evt : événement déclencheur
def clicSouris(a_evt) :
    global LargeurCanvas, HauteurCanvas, InitTurtle
    if Debug : print('clicSouris', a_evt.widget, a_evt.x, a_evt.y)
    # Si la fenêtre a changé de taille
    if (a_evt.widget == Wroot or a_evt.widget == Wcanvas) and (LargeurCible != LargeurCanvas or HauteurCible != HauteurCanvas) :
        # Sauvegarde de la nouvelle taille
        LargeurCanvas = LargeurCible
        HauteurCanvas = HauteurCible
        # Modification du Wcanvas pour la nouvelle taille
        Wcanvas.configure(width=LargeurCanvas, height=HauteurCanvas)
        if Debug : print('clicSouris', InitTurtle, LargeurCible, HauteurCible)
        # Retracé du labyrinthe s'il existe
        if InitTurtle == True :
            global turtle
            # Suppression de la variable turtle existante
            del turtle
            # On recrée le module turtle perdu par la commande précédente
            import turtle
            import importlib
            # On force le rechargement de turtle
            importlib.reload(turtle)
            # On réinitialise turtle
            InitTurtle = False
            initTurtle()
            # On retrace la grille
            traceGrilleHexa()
    # Autre cas (button release sur le canvas)
    elif a_evt.widget == Wcanvas :
        # Position avec origine au centre (ordonnées vers le haut)
        x = a_evt.x - LargeurCanvas / 2
        y = HauteurCanvas / 2 - a_evt.y
        # Gestion du clic sur un mur
        clicMur(x, y)
    return


# Change le type de côté entre OUVERTURE et MUR_INT
# a_x : abscisse (origine au centre de l'écran)
# a_y : ordonnée (origine au centre de l'écran, orientée vers le haut)
def clicMur(a_x, a_y) :
    # Récupération de la position en fraction d'hexagone
    (i, j) = coordHexa(a_x, a_y)
    # Coordonnées de l'hexagone 
    i = round(i)
    j = round(j)
    # On ne prend que les hexagones dans le labyrinthe 
    if 0 <= i and i < Largeur and 0 <= j and j < Hauteur :
        # Coordonnées du centre le plus proche
        c_x, c_y = centreHexa(i, j)
        # Angle du clic par rapport au centre le plus proche
        angle = math.degrees(math.atan2(a_y - c_y, a_x - c_x))
        # Index du mur le plus proche
        k = int(angle % 360 / 60)
        if Debug : print('clicMur', i, j, k)
        # Changement du type de mur
        changeMur(i, j, k)
        if Debug : turtle.goto(c_x, c_y)
    return


# Change le type de côté entre OUVERTURE et MUR_INT
# a_i : abscisse de l'hexagone
# a_j : ordonnée de l'hexagone
# a_k : numéro du mur
def changeMur(a_i, a_j, a_k) :
    global MursPlus, MursMoins
    # Validité des arguments
    if 0 <= a_i and a_i < Largeur and 0 <= a_j and a_j < Hauteur and 0 <= a_k and a_k < 6 :
        # Changement du type de mur
        typeMur = TabLaby[a_i][a_j][a_k]
        # On ne change pas le type de mur externe
        if typeMur != MUR_EXT :
            # Paroi voisine à changer aussi
            (v_i, v_j, v_k) = voisin(a_i, a_j, a_k)
            # Nouveau type de côté (on échange MUR_INT et OUVERTURE)
            if typeMur == OUVERTURE :
                nouveauType = MUR_INT
                # On ajoute un mur
                MursPlus += 1
            else :
                nouveauType = OUVERTURE
                # On retire un mur
                MursMoins += 1
            # On affecte le nouveau type de mur pour les 2 parois
            TabLaby[a_i][a_j][a_k] = TabLaby[v_i][v_j][v_k] = nouveauType
            # Retracé du labyrinthe
            traceGrilleHexa()
            # Mise à jour du titre
            majTitre()
    return


# Mise à jour du titre de la fenêtre
def majTitre() :
    # Titre de la fenêtre après ajout / suppression de murs (on les indique)
    if MursPlus > 0 or MursMoins > 0 :
        titre = TITRE + VERSION + ' : ' + str(MursInit) + ' + ' + str(MursPlus) + ' - ' + str(MursMoins) + ' = ' + str(MursInit + MursPlus - MursMoins) + ' murs / ' + str(MursMax) + ' (max)'
    # Titre de la fenêtre avant création du labyrinthe
    elif MursInit == 0 :
        titre = TITRE + VERSION
    # Titre de la fenêtre après création du labyrinthe mais avant ajout / suppression de murs
    else :
        titre = TITRE + VERSION + ' : ' + str(MursInit) + ' murs / ' + str(MursMax) + ' (max)'
    # Affichage du titre avec Tk
    if Wroot != 0 :
        Wroot.title(titre)
    # Affichage du titre avec turtle (sans Tk)
    else :
        turtle.title(titre)
    return


# Numéro d'un hexagone en fonction de la position (a_x, a_y)
# a_x : abscisse (origine au centre de l'écran)
# a_y : ordonnée (origine au centre de l'écran, orientée vers le haut)
# Return : numéro de l'hexagone (i, j)
def coordHexa(a_x, a_y) :
    if InitTurtle :
        i = (a_x + DemiLargeurTotale) / DemiTailleHexa / 1.5
        j = (((a_y + DemiHauteurTotale) / DemiTailleHexa / RACINE3_2) - round(i) % 2) / 2
        if Debug : print('coordHexa', i, j)
    else :
        i = j = 0
    return (i, j)


# Replay de l'algorithme de sortie du labyrinthe
# a_val : valeur du scale
def cheminCmd(a_val) :
    if len(Chemin) > 0 :
        # Récupération de la valeur du scale (de 0 à nombre de cellules - 1 traversées)
        pos = int(a_val)
        # Affichage d'un symbole (la valeur du scale) sur le centre de la cellule (en noir, plus visible)
        traceSymbole(Chemin[pos][0], Chemin[pos][1], TAG_CHEMIN, 'black', str(pos+1))
    return


# Lancement de l'algorithme de sortie du labyrinthe (bouton 'Démarrer')
# 1 : on vérifie qu'on est pas déjà sur la sortie
# 2 : on vérifie qu'on peut changer de cellule
# 3 : on place la main choisie sur le mur en fonction de la direction choisie
# 4 : on avance en suivant toujours le mur jusqu'à la sortie ou un nombre maximum de cellules visité
def demarrerCmd() :
    global Orientation
    # On retrace le labyrinthe (pour effacer les chemins turtle précédents s'il y en a)
    traceGrilleHexa()
    # Initialisation pour calcul du temps de l'algorithme
    tps = time.time()
    # Orientation de la 'turtle'
    orientation()
    # On lève le stylo
    turtle.penup()
    # On va au centre de la cellule
    (x, y) = centreHexa(Entree[0], Entree[1])
    turtle.goto(x, y)
    # Affichage de la 'turtle'
    turtle.showturtle()
    # On trace !
    turtle.pendown()
    # Couleur du chemin
    turtle.pencolor(COULEUR_LABY[CHEMIN])
    # Epaisseur du chemin
    turtle.pensize(EPAISSEUR_LABY[CHEMIN])
    # Position de départ (attention pos = Entree ne marche pas)
    pos = [Entree[0], Entree[1]]
    # Nombre de cellules visitées
    cellules = 1
    # Nombre maximum de cellules visitables
    maxCellules = Largeur * Hauteur * MULT_CELLULES
    # Mise à zéro du chemin
    Chemin.clear()
    # Première cellule
    Chemin.append((Entree[0], Entree[1]))
    # Si on a Tk
    if Wcanvas != 0 :
        # On efface le symbole (texte) du chemin
        Wcanvas.delete(TAG_CHEMIN)
    # Cas trivial : on est déjà à la sortie
    if Entree == Sortie :
        message = 'Cas trivial, entrée et sortie confondues'
        erreur = False
    else :
        # Il faut pouvoir avancer
        prison = TabLaby[pos[0]][pos[1]][0] != OUVERTURE and TabLaby[pos[0]][pos[1]][1] != OUVERTURE and \
                 TabLaby[pos[0]][pos[1]][2] != OUVERTURE and TabLaby[pos[0]][pos[1]][3] != OUVERTURE and \
                 TabLaby[pos[0]][pos[1]][4] != OUVERTURE and TabLaby[pos[0]][pos[1]][5] != OUVERTURE
        if not prison :
            # Vitesse initiale (la plus lente en cas de vitesse variable)
            turtle.speed(1 if Vitesse < 0 else Vitesse)            
            # Tant qu'on a pas trouvé la sortie on avance en suivant le mur (maximum maxCellules visitées)
            while pos != Sortie and cellules < maxCellules :
                if Debug : print('demarrerCmd', cellules, Orientation)
                # On change l'orientation dans le sens de 'Main' jusqu'au mur libre
                for i in range(6) :
                    # Si on ne peut pas avancer on change de direction (pour le départ on met la main sur le mur)
                    if TabLaby[pos[0]][pos[1]][Orientation] != OUVERTURE or cellules == 1 and TabLaby[pos[0]][pos[1]][Orientation-Sens] == OUVERTURE :
                        # Nouvelle orientation
                        Orientation = (Orientation + Sens) % 6
                        # Visualisation de l'orientation
                        orientation()
                    # On peut avancer dans cette direction
                    else :
                        # On avance dans la cellule suivante
                        cellules += avance(pos)
                        # Nouvelle orientation
                        # Main gauche sur le mur : 0 => 2, 1 => 3, 2 => 4, 3 => 5, 4 => 0, 5 => 1
                        # Main droite sur le mur : 0 => 4, 1 => 5, 2 => 0, 3 => 1, 4 => 2, 5 => 3
                        Orientation = (Orientation + Sens + 3) % 6
                        # Si vitesse variable : augmentation progressive de la vitesse de tracé du chemin
                        if Vitesse < 0 :
                            turtle.speed(cellules / 2)
                        # On a trouvé un mur libre, on ne continue pas à chercher
                        break
            # Calcul du temps écoulé
            tps = round(time.time() - tps, 2)
            # On a trouvé la sortie !
            if pos == Sortie :
                message = 'Sortie trouvée en ' + str(tps) + ' s, nombre de cellules visitées : ' + str(cellules) + ' / ' + str(Largeur * Hauteur)
                erreur = False
            # Sortie par nombre max atteint (erreur)
            else :
                message = 'Sortie NON trouvée en ' + str(tps) + ' s, nombre de cellules visitées : ' + str(cellules) + ' / ' + str(Largeur * Hauteur) + ' (coefficient = ' + str(MULT_CELLULES) + ')'
                erreur = True
        # Cas de la prison (erreur)
        else :
            message = "Sortie non trouvable, la cellule d'entrée n'a pas d'issue"
            erreur = True
    # Message de fin
    print(message)
    # Si on a Tk
    if TK :
        # Le scale du chemin doit aller de 0 à cellules - 1
        ScaChemin.configure(to=cellules-1)
        # Le chemin est positionné à la sortie
        ScaChemin.set(cellules-1)
        # Affichage dans la dernière cellule
        cheminCmd(cellules-1)
        # Affichage de la boîte de fin
        if erreur :
            showerror('Fin (erreur)', message)
        else :
            showinfo('Fin (ok)', message)
    return


# Changement du choix de la main collée au mur (gauche => -1, droite => +1)
# a_val : valeur du menu choisie
def mainCmd(a_val) :
    global Sens
    # Sur main gauche collée au mur, Sens = -1 (on tourne vers la droite, sens montre)
    if a_val == MAIN_GAUCHE :
        Sens = -1
    # Sur main droite collée au mur, Sens = +1 (on tourne vers la gauche, sens trigo)
    else :
        Sens = 1
    return


# Changement du choix d'orientation de départ
# a_val : valeur du menu choisie
def orientationCmd(a_val) :
    # L'index 0 correspond à Nord-Est : 30 degrés, le 5 à Sud-Est : 330 °
    changeOrientation(ORIENTATION.index(a_val))
    return


# Changement de la position en abscisse de l'entrée du labyrinthe
# a_val : valeur du scale
def xEntreeCmd(a_val) :
    global Entree
    # Récupération de l'abscisse de l'entrée
    Entree[0] = int(a_val)
    # On trace l'entrée avec la nouvelle valeur
    traceEntree()
    return


# Changement de la position en ordonnée de l'entrée du labyrinthe
# a_val : valeur du scale
def yEntreeCmd(a_val) :
    global Entree
    # Récupération de l'ordonnée de l'entrée
    Entree[1] = int(a_val)
    # On trace l'entrée avec la nouvelle valeur
    traceEntree()
    return


# Changement de la position en abscisse de la sortie du labyrinthe
# a_val : valeur du scale
def xSortieCmd(a_val) :
    global Sortie
    # Récupération de l'abscisse de la sortie
    Sortie[0] = int(a_val)
    # On trace la sortie avec la nouvelle valeur
    traceSortie()
    return


# Changement de la position en ordonnée de la sortie du labyrinthe
# a_val : valeur du scale
def ySortieCmd(a_val) :
    global Sortie
    # Récupération de l'ordonnée de la sortie
    Sortie[1] = int(a_val)
    # On trace la sortie avec la nouvelle valeur
    traceSortie()
    return


# Lancement de la création du labyrinthe (bouton 'Créer')
def creerLabyCmd() :
    try :
        # Récupération de la largeur choisie
        largeur = int(VarLargeur.get())
        # Récupération de la hauteur choisie
        hauteur = int(VarHauteur.get())
    except :
        largeur = hauteur = 0
    # Vérification de la validité des valeurs saisies
    if largeur < LARG_HAUT_MIN or hauteur < LARG_HAUT_MIN :
        # Valeurs erronées
        showerror('Données', 'Les valeurs de largeur et de hauteur doivent être au minimum de ' + str(LARG_HAUT_MIN))
    elif largeur > LARG_HAUT_MAX or hauteur > LARG_HAUT_MAX :
        # Valeurs erronées
        showerror('Données', 'Les valeurs de largeur et de hauteur doivent être au maximum de ' + str(LARG_HAUT_MAX))
    else :
        # Le scale en X doit aller de 0 à largeur - 1
        ScaEntreeX.configure(to=largeur-1)
        # Le scale en Y doit aller de 0 à hauteur - 1
        ScaEntreeY.configure(to=hauteur-1)
        # Le scale en X doit aller de 0 à largeur - 1
        ScaSortieX.configure(to=largeur-1)
        # Le scale en Y doit aller de 0 à hauteur - 1
        ScaSortieY.configure(to=hauteur-1)
        # Initialisation du labyrinthe
        init(largeur, hauteur)
        # Création du labyrinthe parfait aléatoirement
        creeLaby()
        # Tracé du labyrinthe
        traceGrilleHexa()
        # Valeur par défaut de la sortie : coin supérieur droit
        ScaSortieX.set(largeur-1)
        ScaSortieY.set(hauteur-1)
        # Le bouton 'démarrer' est maintenant actif
        BtnDemarrer.configure(state='normal')
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
        LblCoulEntree.configure(bg=coul[1])
        # On utilise la couleur choisie comme label et couleur de fond du bouton
        BtnCoulEntree.configure(text=coul[1].upper(), bg=coul[1])
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
        LblCoulSortie.configure(bg=coul[1])
        # On utilise la couleur choisie comme label et couleur de fond du bouton
        BtnCoulSortie.configure(text=coul[1].upper(), bg=coul[1])
        # On retrace la sortie avec la bonne couleur
        traceSortie()
    return


# Changement du choix d'orientation de départ
# a_val : valeur de l'orientation (0 à 5)
def changeOrientation(a_val) :
    global Orientation
    # L'index 0 correspond à 30 degrés, le 5 à 330 °
    Orientation = a_val
    # Positionne la turtle en fonction de l'orientation
    if InitTurtle :
        orientation()
    return


# Positionne l'orientation de la 'turtle'
def orientation() :
    # Orientation de la turtle
    turtle.setheading(30 + Orientation * 60)
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
            if Debug : print('initTurtle', turtle.getscreen().screensize())
        # Tracé sans Tk : création de la fenêtre et titre
        else :
            majTitre()
            # Action sur clic souris
            turtle.onscreenclick(clicMur)
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
# a_type : type de côté (MUR_EXT, MUR_INT, OUVERTURE)
def traceHexa(a_x, a_y, a_type) :
    # On lève le stylo
    turtle.up()
    # On va au coin droit de l'hexagone
    turtle.goto(a_x + DemiTailleHexa,     a_y)
    # On abaisse le stylo
    turtle.down()
    # On trace le premier segment (dans le sens trigo) : mur 0
    turtle.pensize(EPAISSEUR_LABY[a_type[0]])
    turtle.pencolor(COULEUR_LABY[a_type[0]])              
    turtle.goto(a_x + DemiTailleHexa / 2, a_y + DemiTailleHexa * RACINE3_2)
    # On trace le deuxième segment (dans le sens trigo) : mur 1
    turtle.pensize(EPAISSEUR_LABY[a_type[1]])
    turtle.pencolor(COULEUR_LABY[a_type[1]])
    turtle.goto(a_x - DemiTailleHexa / 2, a_y + DemiTailleHexa * RACINE3_2)
    # On trace le troisième segment (dans le sens trigo) : mur 2
    turtle.pensize(EPAISSEUR_LABY[a_type[2]])
    turtle.pencolor(COULEUR_LABY[a_type[2]])
    turtle.goto(a_x - DemiTailleHexa,     a_y)
    # On trace le quatrième segment (dans le sens trigo) : mur 3
    turtle.pensize(EPAISSEUR_LABY[a_type[3]])
    turtle.pencolor(COULEUR_LABY[a_type[3]])
    turtle.goto(a_x - DemiTailleHexa / 2, a_y - DemiTailleHexa * RACINE3_2)
    # On trace le cinquième segment (dans le sens trigo) : mur 4
    turtle.pensize(EPAISSEUR_LABY[a_type[4]])
    turtle.pencolor(COULEUR_LABY[a_type[4]])
    turtle.goto(a_x + DemiTailleHexa / 2, a_y - DemiTailleHexa * RACINE3_2)
    # On trace le sixième segment (dans le sens trigo) : mur 5
    turtle.pensize(EPAISSEUR_LABY[a_type[5]])
    turtle.pencolor(COULEUR_LABY[a_type[5]])
    turtle.goto(a_x + DemiTailleHexa,     a_y)
    return


# Tracé du bas (mur 4) d'un hexagone
# a_x : abscisse du centre de l'hexagone (en pixels)
# a_y : ordonnée du centre de l'hexagone (en pixels)
# a_type : type de mur (MUR_EXT, MUR_INT, OUVERTURE)
def traceBasHexa(a_x, a_y, a_type) :
    # On lève le stylo
    turtle.up()
    # On va au cinquième segment (dans le sens trigo)
    turtle.goto(a_x - DemiTailleHexa / 2, a_y - DemiTailleHexa * RACINE3_2)
    # On abaisse le stylo
    turtle.down()
    # On trace le cinquième segment (dans le sens trigo) : mur 4
    turtle.pensize(EPAISSEUR_LABY[a_type])
    turtle.pencolor(COULEUR_LABY[a_type])
    turtle.goto(a_x + DemiTailleHexa / 2, a_y - DemiTailleHexa * RACINE3_2)
    return


# Initialisation du graphique et du labyrinthe
# a_largeur : largeur du labyrinthe
# a_hauteur : hauteur du labyrinthe
def init(a_largeur, a_hauteur):
    # Initialisation de turtle
    initTurtle()
    # Initialisation du tableau des données
    initDonnees(a_largeur, a_hauteur)
    return


"""
Nombre de murs 'internes' :
    parois horizontales : (H - 1) * L
    parois inclinées    : (2 * H - 1) * (L - 1)
    Parois totales : (H - 1) * L + (2 * H - 1) * (L - 1) = 3HL - 2(H+L) + 1
"""
# Calcul du nombre de parois internes en fonction de la taille du labyrinthe
# a_largeur : largeur du labyrinthe
# a_hauteur : hauteur du labyrinthe
# Return : nombre de parois internes
def nbParoisInternes(a_largeur, a_hauteur) :
      return (3 * a_largeur * a_hauteur - 2 * (a_largeur + a_hauteur) + 1)


# Tracé d'une grille d'hexagones centrés
def traceGrilleHexa():
    global Orientation
    # Initialisation pour calcul du temps de tracé
    tps = time.time()
    # Désactive l'animation de tracé (pour accelérer le tracé du labyrinthe)
    screen = turtle.getscreen()
    screen.tracer(0)
    # Nettoie l'écran
    turtle.clear()
    # Cache la 'turtle'
    turtle.hideturtle()
    # Mise à zéro du chemin
    Chemin.clear()
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
    # Calcul et affichage du temps écoulé
    tps = round(time.time() - tps, 2)
    print("traceGrilleHexa(", Largeur, ", ", Hauteur, ") : tracé taille ", DemiTailleHexa, " en ", tps, " s", sep='')
    # Active l'animation de tracé
    screen.tracer(1)
    # Efface le symbole du chemin
    if Wcanvas != 0 :
        Wcanvas.delete(TAG_CHEMIN)    
    # Trace l'entrée
    traceEntree()
    # Trace la sortie
    traceSortie()
    # Positionnement de la turtle en fonction de l'orientation
    if TK :
        Orientation = ORIENTATION.index(VarOrient.get())
    else :
        Orientation = 0
    orientation()
    return


# Calcule la position du centre d'une cellule (coordonnées turtle, axe des ordonnées orienté vers le haut)
# a_i : index en abscisse de la cellule
# a_j : index en ordonnée de la cellule
# Return : position du centre de le cellule (x, y) en pixels
def centreHexa(a_i, a_j) :
    # Décalage en abscisse : (DemiTailleHexa + DemiTailleHexa * cos(60)) * i
    x = 1.5 * DemiTailleHexa * a_i - DemiLargeurTotale
    # Décalage en ordonnée : 2 * DemiTailleHexa * sin(60) * j pour les abscisses paires, + DemiTailleHexa * sin(60) pour les impaires
    y = DemiTailleHexa * RACINE3_2 * (2 * a_j + (a_i % 2)) - DemiHauteurTotale
    return (x, y)


# Initialise le tableau de données du labyrinthe
# a_largeur : largeur du labyrinthe (nombre d'hexagones en abscisse)
# a_hauteur : hauteur du labyrinthe (nombre d'hexagones en ordonnée)
def initDonnees(a_largeur, a_hauteur):
    global Largeur, Hauteur, TabLaby, Sortie
    # Initialisation de la largeur
    Largeur = a_largeur
    # Initialisation de la hauteur
    Hauteur = a_hauteur
    # Position de la sortie au coin opposé à l'entrée
    Sortie = [Largeur - 1, Hauteur - 1]
    # Initialisation du tableau des données (NBR_HEXA valeurs par hexagone)
    TabLaby = [[[0 for _ in range(NBR_HEXA)] for _ in range(a_hauteur)] for _ in range(a_largeur)]
    # Affectation du type de paroi (MUR_EXT, MUR_INT ou OUVERTURE) pour les côtés
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
    # Initialisation des valeurs de centrage du labyrinthe
    initCentrage()
    return


# Initialisation des valeurs globales pour le centrage du labyrinthe
def initCentrage() :
    global DemiLargeurTotale, DemiHauteurTotale
    # Moitié de la largeur totale (décalage pour centrage de la grille en largeur)
    DemiLargeurTotale = (Largeur * DemiTailleHexa * 1.5 + DemiTailleHexa / 2) / 2
    # Moitié de la hauteur totale (décalage pour centrage de la grille en hauteur)
    DemiHauteurTotale = DemiTailleHexa * RACINE3_2 * (2 * Hauteur + 1) / 2
    # Décalage en abscisse
    DemiLargeurTotale -= DemiTailleHexa
    # Décalage en ordonnée
    DemiHauteurTotale -= DemiTailleHexa * RACINE3_2
    return


# Calcule si les valeurs des cellules sont nulles
# Return : True si les valeurs ne sont pas toutes nulles
#          False si elles sont toutes nulles
def cellulesNonNulles() :
    valNonNulle = False
    for i in range(Largeur) :
        if valNonNulle : break
        for j in range(Hauteur) :
            if TabLaby[i][j][6] > 0 :
                valNonNulle = True
                break
    return valNonNulle

    
# Algorithme de création d'un labyrinthe :
# 1 : on affecte des numéros croissants à chaque cellule (en commençant à 0)
# 2 : tant que les valeurs des cellules ne sont pas toutes nulles
#   - on supprime un mur interne (existant) aléatoirement qui sépare 2 cellules de valeurs différentes
#   - on affecte la valeur minimale des 2 cellules concernées aux cellules de valeur maximale
def creeLaby() :
    # Mise à jour des compteurs de murs
    global MursInit, MursMax, MursPlus, MursMoins
    # Initialisation pour calcul du temps de création
    tps = time.time()
    # Valeur à mettre dans la cellule
    val = 0
    # Affectation d'une valeur croissante pour chaque cellule
    for i in range(Largeur) :
        for j in range(Hauteur) :
            TabLaby[i][j][6] = val
            # On incrémente la valeur
            val += 1
    # Nombre maximum de murs (tous les murs internes possibles)
    MursInit = MursMax = nbParoisInternes(Largeur, Hauteur)
    # Pas de murs ajoutés ou supprimés
    MursPlus = MursMoins = 0
    # On a nbMurCibles murs internes destructibles (* 2 pour les 2 côtés du mur possibles)
    nbMursCibles = 2 * MursMax
    # Les valeurs des cellule devront être toutes nulles pour un labyrinthe parfait
    while cellulesNonNulles() :
        # Choix d'un mur cible à détruire
        murCible = random.randrange(nbMursCibles)
        if Debug : print('creeLaby : nbMursCibles =', nbMursCibles, ' cible =', murCible, '\n', TabLaby)
        # nbMur : nombre de murs internes
        nbMurs = 0
        # On recherche le mur cible
        for i in range(Largeur) :
            # Sortie optimisée
            if murCible < 0 : break
            for j in range(Hauteur) :
                # Sortie optimisée
                if murCible < 0 : break
                for k in range(6) :
                    # Si on trouve un mur interne
                    if TabLaby[i][j][k] == MUR_INT : 
                        # Cellule voisine
                        v_i, v_j, v_k = voisin(i, j, k)
                        # Si les 2 cellules ne sont pas déjà reliées
                        if TabLaby[i][j][6] != TabLaby[v_i][v_j][6] :
                            # Si c'est le mur cible
                            if nbMurs == murCible :
                                # On le détruit
                                TabLaby[i][j][k] = OUVERTURE
                                # On détruit aussi le mur voisin (l'autre côté de la paroi)
                                TabLaby[v_i][v_j][v_k] = OUVERTURE
                                # On décrémente le nombre de murs initial
                                MursInit -= 1
                                # Valeurs minimales et maximales des 2 cellules
                                if TabLaby[i][j][6] < TabLaby[v_i][v_j][6] :
                                    valMin = TabLaby[i][j][6]
                                    valMax = TabLaby[v_i][v_j][6]
                                else :
                                    valMin = TabLaby[v_i][v_j][6]
                                    valMax = TabLaby[i][j][6]
                                # Recalcul des valeurs de cellules
                                nbMursCibles = 0
                                for m in range(Largeur) :
                                    for n in range(Hauteur) :
                                        # On affecte la valeur min aux cellules de valeur max
                                        if TabLaby[m][n][6] == valMax :
                                            TabLaby[m][n][6] = valMin
                                # Recalcul du nombre de murs cibles
                                nbMursCibles = 0
                                for m in range(Largeur) :
                                    for n in range(Hauteur) :
                                        # Calcul du nombre de murs 
                                        for o in range(6) :
                                            if TabLaby[m][n][o] == MUR_INT :
                                                v_m, v_n, v_o = voisin(m, n, o)
                                                if TabLaby[m][n][6] != TabLaby[v_m][v_n][6] :
                                                    nbMursCibles += 1
                                if Debug : print('creeLaby : cible =', i, j, k, '/', v_i, v_j, v_k, '; nbMursCibles =', nbMursCibles)
                                # Optimisation de la boucle (on arrête la boucle quand on a trouvé la cible)
                                murCible = -1
                                break
                            # On incrémente pour savoir sur quel mur cible potentiel on est
                            nbMurs += 1
    # Calcul et affichage du temps écoulé
    tps = round(time.time() - tps, 2)
    print('creeLaby(', Largeur, 'x', Hauteur, '=', Largeur * Hauteur, ') : en ', tps, ' s', sep='')
    # Mise à jour du titre de la fenêtre
    majTitre()
    return


# Calcul le côté voisin d'un côté donné (l'autre face)
# a_i : abscisse de l'hexagone (indice)
# a_j : ordonnée de l'hexagone (indice)
# a_k : rang du côté (0 = NE, 1 = N, 2 = NO, 3 = SO, 4 = S, 5 = SE)
# Return : triplet de définition (i, j, k) du côté 'voisin' (k = -1 si pas de voisin)
def voisin(a_i, a_j, a_k) :
    # Sur les bords il n'y a pas de voisin
    if a_i == 0 and (a_k == 2 or a_k == 3) or a_i == Largeur - 1 and (a_k == 0 or a_k == 5) :
        # Indicateur voisin inexistant
        i = j = k = -1
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


# On avance d'une cellule à partir de la position a_pos dans la direction Orientation
# a_pos : position initiale
# Return : nombre de cellules visitées
def avance(a_pos) :
    global Chemin
    # On cherche le voisin
    (i, j, k) = voisin(a_pos[0], a_pos[1], Orientation)
    # On va jusqu'au centre suivant
    turtle.goto(centreHexa(i, j))
    # On se positionne à la nouvelle cellule
    a_pos[0] = i
    a_pos[1] = j
    # Sauvegarde de la position
    Chemin.append((a_pos[0], a_pos[1]))
    return 1


# Trace l'entrée du labyrinthe
def traceEntree() :
    # On enleve le dessin d'entrée s'il existe
    traceSymbole(Entree[0], Entree[1], TAG_ENTREE, CoulEntree)
    # Au cas où il y a superposition on retrace la sortie qui est au-dessus
    if Sortie == Entree :
        traceSortie()
    return


# Trace la sortie du labyrinthe
def traceSortie() :
    # On enleve le dessin d'entrée s'il existe
    traceSymbole(Sortie[0], Sortie[1], TAG_SORTIE, CoulSortie)
    return


# Tracé d'un symbole dans l'hexagone
# a_largeur : rang en abscisse de l'hexagone
# a_hauteur : rang en ordonnée de l'hexagone
# a_symbole : symbole pour identifier et pouvoir effacer
# a_color   : couleur du tracé
# a_text    : text du symbole (pour le type TAG_CHEMIN)
def traceSymbole(a_largeur, a_hauteur, a_symbole, a_color, a_text='') :
    if InitTurtle :
        # Position du centre
        (x, y) = centreHexa(a_largeur, a_hauteur)
        # Rayon de la sortie plus petit (il est tracé après l'entrée, cela permet de voir les 2 si superposés)
        if a_symbole == TAG_SORTIE :
            rayon = DemiTailleHexa / 3
        # Rayon
        else : 
            rayon = DemiTailleHexa / 2
        # Tracés avec tag sur le canvas de Tk
        if Wcanvas != 0 :
            # On enleve le symbole s'il existe
            Wcanvas.delete(a_symbole)
            # Tracé du symbole (texte pour le chemin)
            if a_symbole == TAG_CHEMIN :
                Wcanvas.create_text(x, -y, text=a_text, fill=a_color, tags=a_symbole)
            # Carré pour entrée et sortie
            else :
                Wcanvas.create_rectangle(x - rayon, -y - rayon, x + rayon, -y + rayon, fill=a_color, tags=a_symbole)
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
            # Tracé du symbole (un carré, coin vers le bas)
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

