
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
VERSION = " v1.1"

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


# ------------------------------------------------------------------------------
# Variables globales

#épaisseur
TailleMurs = (3, 2, 1)

# Couleurs du mur en fonction du type
CouleurMurs = ('black', 'blue', 'pink')

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

# Debug
Debug = False

# Interface
TK = True


# ------------------------------------------------------------------------------
# Fonctions

# Création interface
def creeInterface(a_largeur = 500, a_hauteur = 500) :
    global Wcanvas, ValLargeur, ValHauteur
    # Fenêtre principale
    root = Tk()
    root.title(TITRE + VERSION)
    root.geometry(str(a_largeur)+"x"+str(a_hauteur+140)+"-10+10")
    # Frame des données
    dataFrame = Frame(root)
    # Partie 'Coordonnées'
    labyFrame = LabelFrame(dataFrame, text='Labyrinthe')
    # Première ligne : largeur du labyrinthe
    lblLargeur = Label(labyFrame, text='Largeur')
    lblLargeur.grid(row=0, column=0)
    ValLargeur = StringVar(root)
    ValLargeur.set(LARGEUR_DEF)
    texLargeur = Entry(labyFrame, textvariable=ValLargeur, width=2)
    texLargeur.grid(row=0, column=1)
    # Deuxième ligne : hauteur du labyrinthe
    lblHauteur = Label(labyFrame, text='Hauteur')
    lblHauteur.grid(row=1, column=0)
    ValHauteur = StringVar(root)
    ValHauteur.set(HAUTEUR_DEF)
    texHauteur = Entry(labyFrame, textvariable=ValHauteur, width=2)
    texHauteur.grid(row=1, column=1)
    # Troisième ligne : bouton 'Créer'
    btnCreer = Button(labyFrame, text='Créer', command=creerLabyCmd)
    btnCreer.grid(row=2, column=0)
    # Fin de la partie labyFrame
    labyFrame.grid(row=0, column=0, sticky=tkinter.N+tkinter.S)
    # Fin de la partie dataFrame
    dataFrame.grid(sticky=tkinter.W)
    # Fenêtre graphique (canvas)
    Wcanvas = Canvas(root, background="white", width=a_largeur, height=a_hauteur)
    Wcanvas.grid(row=1, column=0)
    return


def creerLabyCmd() :
    Largeur = int(ValLargeur.get())
    Hauteur = int(ValHauteur.get())
    init(Largeur, Hauteur)
    creeLaby()
    traceGrilleHexa(Largeur, Hauteur)
    return


# Initialisation de turtle
def initTurtle() :
    global InitTurtle
    # Initialisation de Turtle si pas déjà fait
    if not InitTurtle :
        if TK :
            from turtle import RawPen
            global turtle
            turtle = RawPen(Wcanvas)
            print('Tk')
        else :
        # Titre de la fenêtre
            turtle.title(TITRE + VERSION)
            # Fonction utilisateur définie sur clic
            turtle.onscreenclick(screenClick)
        # Vitesse maximale du tracé
        turtle.speed(0)
        # Cache le pointeur de Turtle
        turtle.hideturtle()
        # Turtle est maintenant initialisé
        InitTurtle = True
    # Turtle est déjà initialisé : on vide la fenêtre
    else :
        turtle.clear()
    return


# Fonction appelée sur clic
# a_x : abscisse du clic
# a_y : ordonnée du clic
def screenClick(a_x, a_y) :
    print('clic en', a_x, a_y)
    return


# Tracé d'un hexagone entier
# a_x : centre de l'hexagone en abscisse
# a_y : centre de l'hexagone en ordonnée
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
# a_x : centre de l'hexagone en abscisse
# a_y : centre de l'hexagone en ordonnée
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
# a_largeur : nombre d'hexagones en largeur
# a_hauteur : nombre d'hexagones en hauteur
def traceGrilleHexa(a_largeur, a_hauteur):
    # Moitié de la largeur totale (décalage pour centrage de la grille en largeur)
    demiLargeurTotale = (a_largeur * DemiLargeurHexa * 1.5 + DemiLargeurHexa / 2) / 2
    # Moitié de la hauteur totale (décalage pour centrage de la grille en hauteur)
    demiHauteurTotale = DemiLargeurHexa * (2 * RACINE3_2 * a_hauteur + RACINE3_2) / 2
    """
    turtle.up()
    turtle.goto(-demiLargeurTotale, -demiHauteurTotale)
    turtle.down()
    turtle.goto( demiLargeurTotale, -demiHauteurTotale)
    turtle.goto( demiLargeurTotale,  demiHauteurTotale)
    turtle.goto(-demiLargeurTotale,  demiHauteurTotale)    
    turtle.goto(-demiLargeurTotale, -demiHauteurTotale)
    """
    # Décalage en abscisse
    demiLargeurTotale -= DemiLargeurHexa
    # Décalage en ordonnée
    demiHauteurTotale -= DemiLargeurHexa * RACINE3_2
    # Initialisation pour calcul du temps de tracé
    tps = time.time()
    # Désactive l'animation de tracé
    if not TK : turtle.tracer(0)
    for i in range(a_largeur) :
        for j in range(a_hauteur) :
            # Décalage en abscisse : (DemiLargeurHexa + DemiLargeurHexa * cos(60)) * i
            # Décalage en ordonnée : 2 * DemiLargeurHexa * sin(60) * j pour les abscisses paires, + DemiLargeurHexa * sin(60) pour les impaires
            if i % 2 == 0 or i == a_largeur - 1 or j == a_hauteur - 1 :
                traceHexa(1.5 * DemiLargeurHexa * i - demiLargeurTotale, DemiLargeurHexa * (2 * RACINE3_2 * j + RACINE3_2 * (i % 2)) - demiHauteurTotale, TabLaby[i][j])
            else :
                traceBasHexa(1.5 * DemiLargeurHexa * i - demiLargeurTotale, DemiLargeurHexa * (2 * RACINE3_2 * j + RACINE3_2 * (i % 2)) - demiHauteurTotale, TabLaby[i][j][4])
    # Affichage du temps de tracé
    print("traceGrilleHexa(", a_largeur, ", ", a_hauteur, ") : tracé en ", round(time.time() - tps, 2), " s", sep='')
    # Active l'animation de tracé
    if not TK : turtle.tracer(1)
    return


# Initialise le tableau de données du labyrinthe
# a_largeur : largeur du labyrinthe (nombre d'hexagones en abscisse)
# a_hauteur : hauteur du labyrinthe (nombre d'hexagones en ordonnée)
def initDonnees(a_largeur, a_hauteur):
    global Largeur, Hauteur, TabLaby
    # Initialisation de la largeur
    Largeur = a_largeur
    # Initialisation de la hauteur
    Hauteur = a_hauteur
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
#   - on affecte la valeur minimale des 2 cellules concernées aux 2 cellules
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
# ret : triplet de définition du mur 'voisin' (z = -1 si pas de voisin)
def voisin(a_i, a_j, a_k) :
    # Sur les bords il n'y a pas de voisin (TBD compléter, tests gauche et droite faits)
    if a_i == 0 and (a_k == 2 or a_k == 3) or a_i == Largeur - 1 and (a_k == 0 or a_k == 5) :
        # Indicateur voisin inexistant
        k = -1
    else :
        # Indices des abscisses et ordonnées de l'hexagone voisin
        if a_k == 0 :
            i = a_i + 1
            j = a_j
            if i % 2 == 0 : j += 1
        elif a_k == 1 :
            i = a_i
            j = a_j + 1
        elif a_k == 2 :
            i = a_i - 1
            j = a_j
            if i % 2 == 0 : j += 1
        elif a_k == 3 :
            i = a_i - 1
            j = a_j
            if i % 2 == 1 : j -= 1
        elif a_k == 4 :
            i = a_i 
            j = a_j - 1
        else :
            i = a_i + 1
            j = a_j
            if i % 2 == 1 : j -= 1
        # Indice du mur de l'hexagone voisin
        k = (a_k + 3) % 6
    return (i, j, k)


# Positionne un mur à une valeur donnée (ainsi que l'autre face du mur)
# a_x : abscisse de l'hexagone
# a_y : ordonnée de l'hexagone
# a_z : rang du mur (0 = NE, 1 = N, 2 = NO, 3 = SO, 4 = S, 5 = SE)
def setMur(a_i, a_j, a_k, a_val) :
    global TabLaby
    TabLaby[a_i][a_j][a_k] = a_val
    x, y, z = voisin(a_i, a_j, a_k)
    if z >= 0 :
        TabLaby[x][y][z] = a_val
    return
    
    
def test(a_largeur = 8, a_hauteur = 5) :
    if TK :
        creeInterface()
    else :
        init(a_largeur, a_hauteur)
        creeLaby()
        traceGrilleHexa(a_largeur, a_hauteur)
    return
