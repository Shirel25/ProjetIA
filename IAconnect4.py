import numpy as np
import random
import pygame
import sys
import math

########################################################################################
################################  Initialisations  #####################################
########################################################################################

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

########################################################################################
###################################  Interface  ########################################
########################################################################################

def creer_tableau():
	#fonction servant à afficher le tableau correspondant 
    #au jeu dans le terminal
	tableau = np.zeros((NB_LIGNES,NB_COLONNES))
	return tableau

def depot_jeton(tableau, ligne, col, jeton):
	#le tableau dans le terminal va se remplir avec les jetons ajoutés par les joueurs
	tableau[ligne][col] = jeton


def get_ligne_suivante(tableau, col):
	for l in range(NB_LIGNES):
		if tableau[l][col] == 0:
			return l

def afficher_tableau_terminal(tableau):
	#iverser l'affichage du tableau : on retourne le tableau pour qu'il corresponde aux jetons
    # qui remplissent le tableau d'abord par le bas       
	print(np.flip(tableau, 0))

def draw_tableau(tableau):
	#création de la fenetre graphique
	for c in range(NB_COLONNES):
		for l in range(NB_LIGNES):
			pygame.draw.rect(fenetre, BLEU, (c*TAILLE_GRILLE, l*TAILLE_GRILLE+TAILLE_GRILLE, TAILLE_GRILLE, TAILLE_GRILLE))
			pygame.draw.circle(fenetre, NOIR, (int(c*TAILLE_GRILLE+TAILLE_GRILLE/2), int(l*TAILLE_GRILLE+TAILLE_GRILLE+TAILLE_GRILLE/2)), CERCLE)
	
	for c in range(NB_COLONNES):
		for l in range(NB_LIGNES):		
			if tableau[l][c] == JETON_JOUEUR:
				pygame.draw.circle(fenetre, ROUGE, (int(c*TAILLE_GRILLE+TAILLE_GRILLE/2), hauteur-int(l*TAILLE_GRILLE+TAILLE_GRILLE/2)), CERCLE) #on ajoute "hauteur -" pour que le tableau se remplisse 
			elif tableau[l][c] == JETON_IA: 																									 #par le bas d'abord							
				pygame.draw.circle(fenetre, JAUNE, (int(c*TAILLE_GRILLE+TAILLE_GRILLE/2), hauteur-int(l*TAILLE_GRILLE+TAILLE_GRILLE/2)), CERCLE)
	pygame.display.update()

########################################################################################
##################################  Verification  ######################################
########################################################################################

def emplacement_valide(tableau, col):
	#verifier si un emplacement est valide revient a verifier que la ligne du haut (5eme) est vide (a 0)
	return tableau[NB_LIGNES-1][col] == 0


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

########################################################################################
#######################################  IA  ###########################################
########################################################################################


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





########################################################################################
#####################################  Game  ###########################################
########################################################################################



tableau = creer_tableau()
afficher_tableau_terminal(tableau)
game_over = False

#intialisation de la fenêtre
pygame.init()


largeur = NB_COLONNES * TAILLE_GRILLE
hauteur = (NB_LIGNES+1) * TAILLE_GRILLE #en comptant la ligne du haut où le jeton se déplace

taille = (largeur, hauteur)

CERCLE = int(TAILLE_GRILLE/2 - 5)

fenetre = pygame.display.set_mode(taille)
draw_tableau(tableau)
pygame.display.update()

#police et taille d'écriture
times_new_roman = pygame.font.SysFont('Times New Roman', 75)

#choix aléatoire du joueur qui commence la partie
tour = random.randint(JOUEUR, IA)

while not game_over:
	#pour tout évênement
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			#si on bouge la souris, le jeton suit le mouvement en haut des colonnes
			pygame.draw.rect(fenetre, NOIR, (0,0, largeur, TAILLE_GRILLE))
			posx = event.pos[0]
			if tour == JOUEUR:
				pygame.draw.circle(fenetre, ROUGE, (posx, int(TAILLE_GRILLE/2)), CERCLE)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(fenetre, NOIR, (0,0, largeur, TAILLE_GRILLE))
			#print(event.pos)
			
			if tour == JOUEUR:
				posx = event.pos[0]
				col = int(math.floor(posx/TAILLE_GRILLE))

				if emplacement_valide(tableau, col):
					ligne = get_ligne_suivante(tableau, col)
					depot_jeton(tableau, ligne, col, JETON_JOUEUR)

					if gagne(tableau, JETON_JOUEUR):
						label = times_new_roman.render("Joueur 1 a gagné !!!", 1, ROUGE)
						fenetre.blit(label, (50,10)) #affichage du label sur la fenetre graphique
						game_over = True

					tour += 1
					tour = tour % 2

					afficher_tableau_terminal(tableau)
					draw_tableau(tableau)


	# Si c'est au tour de l'IA et que le jeu n'est pas fini
	if tour == IA and not game_over:				

		#col = random.randint(0, NB_COLONNES-1)
		#col = meilleur_depot(tableau, JETON_IA)
		col, minimax_score = algo_minimax(tableau, 5, -math.inf, math.inf, True)

		if emplacement_valide(tableau, col):
			pygame.time.wait(500) #temps d'attente pour que l'IA joue 
			ligne = get_ligne_suivante(tableau, col)
			depot_jeton(tableau, ligne, col, JETON_IA)

			if gagne(tableau, JETON_IA):
				label = times_new_roman.render("Joueur 2 a gagné !!!", 1, JAUNE)
				fenetre.blit(label, (50,10)) #affichage du label sur la fenetre graphique
				game_over = True

			afficher_tableau_terminal(tableau)
			draw_tableau(tableau)

			tour += 1
			tour = tour % 2

	if game_over:
		pygame.time.wait(5000)