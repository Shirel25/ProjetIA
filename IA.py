import random
import math
from Interface import *

def gagne(tableau, jeton):
	#fonction qui retourne True si le joueur a gagné 

	#Vérification horizontale
	for c in range(NB_COLONNES-3): #seulement à partir de la position où il est possible d'être dans une ligne gagnante
		for l in range(NB_LIGNES):
			if tableau[l][c] == jeton and tableau[l][c+1] == jeton and tableau[l][c+2] == jeton and tableau[l][c+3] == jeton:
				return True

	#Vérification verticale
	for c in range(NB_COLONNES):
		for l in range(NB_LIGNES-3):
			if tableau[l][c] == jeton and tableau[l+1][c] == jeton and tableau[l+2][c] == jeton and tableau[l+3][c] == jeton:
				return True

	#Vérification diagonale positive
	for c in range(NB_COLONNES-3):
		for l in range(NB_LIGNES-3):
			if tableau[l][c] == jeton and tableau[l+1][c+1] == jeton and tableau[l+2][c+2] == jeton and tableau[l+3][c+3] == jeton:
				return True

	#Vérification diagonale négative
	for c in range(NB_COLONNES-3):
		for l in range(3, NB_LIGNES):
			if tableau[l][c] == jeton and tableau[l-1][c+1] == jeton and tableau[l-2][c+2] == jeton and tableau[l-3][c+3] == jeton:
				return True
			

def calcul_score(fenetre, jeton):
	#retourne le score du joueur en fonction des possibilités qui s'offrent à celui selon son placement
	score = 0
	jeton_adverse = JETON_JOUEUR
	if jeton == JETON_JOUEUR:
		jeton_adverse = JETON_IA

	if fenetre.count(jeton) == 4:
		score += 100
	elif fenetre.count(jeton) == 3 and fenetre.count(VIDE) == 1:
		score += 5
	elif fenetre.count(jeton) == 2 and fenetre.count(VIDE) == 2:
		score += 2

	if fenetre.count(jeton_adverse) == 3 and fenetre.count(VIDE) == 1:
		score -= 4

	return score


def score_position(tableau, jeton):
	#fonction qui examine l'etat d'un jeton selon sa position 
    #elle renvoie un score de 100 si elle est de puissance 4, sinon 0    
	score = 0

	## Score colonne du milieu
	tableau_centre = [int(i) for i in list(tableau[:, NB_COLONNES//2])]  #//2 pour avoir la colonne du milieu
	centre_count = tableau_centre.count(jeton)
	score += centre_count * 3

	## Score horizontale
	for l in range(NB_LIGNES):
		tableau_ligne = [int(i) for i in list(tableau[l,:])]
		for c in range(NB_COLONNES-3):
			fenetre = tableau_ligne[c:c+FENETRE_LENGTH]
			score += calcul_score(fenetre, jeton)

	## Score verticale
	for c in range(NB_COLONNES):
		tableau_col = [int(i) for i in list(tableau[:,c])]
		for l in range(NB_LIGNES-3):
			fenetre = tableau_col[l:l+FENETRE_LENGTH]
			score += calcul_score(fenetre, jeton)

	## Score diagonale positive
	for l in range(NB_LIGNES-3):
		for c in range(NB_COLONNES-3):
			fenetre = [tableau[l+i][c+i] for i in range(FENETRE_LENGTH)]
			score += calcul_score(fenetre, jeton)

    ## Score diagonale négative
	for l in range(NB_LIGNES-3):
		for c in range(NB_COLONNES-3):
			fenetre = [tableau[l+3-i][c+i] for i in range(FENETRE_LENGTH)]
			score += calcul_score(fenetre, jeton)

	return score

def fin_jeu(tableau):
	#si le joueur gagne, l'IA gagne, ou toutes les cases sont remplies 
	return gagne(tableau, JETON_JOUEUR) or gagne(tableau, JETON_IA) or len(get_emplacement_valide(tableau)) == 0


def algo_minimax(tableau, profondeur, alpha, beta, joueurMAX):
	#algo representant un arbre dont les noeuds vont alterner entre MAX et MIN
	#MAX va chercher à faire remonter à la racine de l'arbre la plus grande valeur de sortie, tandis que 
	#MIN va chercher à faire remonter la plus basse
	bon_emplacement = get_emplacement_valide(tableau)
	partie_finie = fin_jeu(tableau)
	if profondeur == 0 or partie_finie:
		if partie_finie:
			if gagne(tableau, JETON_IA):
				return (None, 100000000000000)
			elif gagne(tableau, JETON_JOUEUR):
				return (None, -10000000000000)
			else: #Pas de gagnant, plus de possibilité de jouer
				return (None, 0)
		else: # profondeur à 0
			return (None, score_position(tableau, JETON_IA))
	
	# Joueur MAX
	if joueurMAX:
		#on met le score à une faible valeur
		value = -math.inf
		colonne = random.choice(bon_emplacement)
		for col in bon_emplacement:
			ligne = get_ligne_suivante(tableau, col)
			tab_copie = tableau.copy() #on cree une copie du tableau afin que les modifiactions que l'on fera n'auront pas d'impact sur le tableau de base
			depot_jeton(tab_copie, ligne, col, JETON_IA)
			nv_score = algo_minimax(tab_copie, profondeur-1, alpha, beta, False)[1]
			if nv_score > value:
				value = nv_score
				colonne = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return colonne, value

	else: # Joueur MIN
		#on met le score à une forte valeur
		value = math.inf
		colonne = random.choice(bon_emplacement)
		for col in bon_emplacement:
			ligne = get_ligne_suivante(tableau, col)
			tab_copie = tableau.copy()
			depot_jeton(tab_copie, ligne, col, JETON_JOUEUR)
			nv_score = algo_minimax(tab_copie, profondeur-1, alpha, beta, True)[1]
			if nv_score < value:
				value = nv_score
				colonne = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return colonne, value

def get_emplacement_valide(tableau):
	#fonction pour savoir si l'emplacement choisi est valide
	bon_emplacement = []
	for col in range(NB_COLONNES):
		if emplacement_valide(tableau, col):
			bon_emplacement.append(col)
	return bon_emplacement

def meilleur_depot(tableau, jeton):
	#fonction qui retourne la colonne ayant le meilleur choix de depot de jeton
	bon_emplacement = get_emplacement_valide(tableau)
	meilleur_score = -10000
	meilleure_col = random.choice(bon_emplacement)
	for col in bon_emplacement:
		ligne = get_ligne_suivante(tableau, col)
		tableau_tmp = tableau.copy() #on cree une copie du tableau afin que les modifiactions que l'on fera n'auront pas d'impact sur le tableau de base
		depot_jeton(tableau_tmp, ligne, col, jeton)
		score = score_position(tableau_tmp, jeton)
		if score > meilleur_score:
			meilleur_score = score
			meilleure_col = col
			
	return meilleure_col
