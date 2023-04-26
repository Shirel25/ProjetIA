import numpy as np


#intialisation des couleurs
BLEU = (0,0,255)
NOIR = (0,0,0)
ROUGE = (255,0,0)
JAUNE = (255,255,0)

#initialisation de la fenêtre
NB_LIGNES = 6
NB_COLONNES = 7
FENETRE_LENGTH = 4 
VIDE = 0
TAILLE_GRILLE = 100

#initialisation du numéro de jeton des joueurs
JOUEUR = 0
IA = 1
#initalisation du numéro du joueur pour l'affichage du tableau dans le terminal 
JETON_JOUEUR = 1
JETON_IA = 2


def creer_tableau():
	#fonction servant à afficher le tableau correspondant 
    #au jeu dans le terminal
	tableau = np.zeros((NB_LIGNES,NB_COLONNES))
	return tableau

def depot_jeton(tableau, ligne, col, jeton):
	#le tableau dans le terminal va se remplir avec les jetons ajoutés par les joueurs
	tableau[ligne][col] = jeton

def emplacement_valide(tableau, col):
	#verifier si un emplacement est valide revient a verifier que la ligne du haut (5eme) est vide (a 0)
	return tableau[NB_LIGNES-1][col] == 0

def get_ligne_suivante(tableau, col):
	for l in range(NB_LIGNES):
		if tableau[l][col] == 0:
			return l

def afficher_tableau_terminal(tableau):
	#iverser l'affichage du tableau : on retourne le tableau pour qu'il corresponde aux jetons
    # qui remplissent le tableau d'abord par le bas       
	print(np.flip(tableau, 0))
	

