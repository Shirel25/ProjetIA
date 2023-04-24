import numpy as np
import random
import pygame
import sys
import math

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
	for r in range(NB_LIGNES):
		if tableau[r][col] == 0:
			return r

def afficher_tableau_terminal(tableau):
	#iverser l'affichage du tableau : on retourne le tableau pour qu'il corresponde aux jetons
    # qui remplissent le tableau d'abord par le bas       
	print(np.flip(tableau, 0))

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

def evaluate_window(window, jeton):
	score = 0
	jeton_suivant = JETON_JOUEUR
	if jeton == JETON_JOUEUR:
		jeton_suivant = JETON_IA

	if window.count(jeton) == 4:
		score += 100
	elif window.count(jeton) == 3 and window.count(VIDE) == 1:
		score += 5
	elif window.count(jeton) == 2 and window.count(VIDE) == 2:
		score += 2

	if window.count(jeton_suivant) == 3 and window.count(VIDE) == 1:
		score -= 4

	return score

def score_position(tableau, jeton):
	#fonction qui examine l'etat d'un jeton selon sa position 
    #elle renvoie un score de 100 si elle est de puissance 4, sinon 0    
	score = 0

	## Score colonne du mileu
	center_array = [int(i) for i in list(tableau[:, NB_COLONNES//2])]
	center_count = center_array.count(jeton)
	score += center_count * 3

	## Score horizontale
	for l in range(NB_LIGNES):
		row_array = [int(i) for i in list(tableau[l,:])]
		for c in range(NB_COLONNES-3):
			window = row_array[c:c+FENETRE_LENGTH]
			score += evaluate_window(window, jeton)

	## Score verticale
	for c in range(NB_COLONNES):
		col_array = [int(i) for i in list(tableau[:,c])]
		for r in range(NB_LIGNES-3):
			window = col_array[r:r+FENETRE_LENGTH]
			score += evaluate_window(window, jeton)

	## Score diagonale positive
	for r in range(NB_LIGNES-3):
		for c in range(NB_COLONNES-3):
			window = [tableau[r+i][c+i] for i in range(FENETRE_LENGTH)]
			score += evaluate_window(window, jeton)

    ## Score diagonale négative
	for r in range(NB_LIGNES-3):
		for c in range(NB_COLONNES-3):
			window = [tableau[r+3-i][c+i] for i in range(FENETRE_LENGTH)]
			score += evaluate_window(window, jeton)

	return score

def is_terminal_node(tableau):
	return gagne(tableau, JETON_JOUEUR) or gagne(tableau, JETON_IA) or len(get_emplacement_valide(tableau)) == 0

def minimax(tableau, depth, alpha, beta, maximizingPlayer):
	bon_emplacement = get_emplacement_valide(tableau)
	is_terminal = is_terminal_node(tableau)
	if depth == 0 or is_terminal:
		if is_terminal:
			if gagne(tableau, JETON_IA):
				return (None, 100000000000000)
			elif gagne(tableau, JETON_JOUEUR):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(tableau, JETON_IA))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(bon_emplacement)
		for col in bon_emplacement:
			ligne = get_ligne_suivante(tableau, col)
			b_copy = tableau.copy()
			depot_jeton(b_copy, ligne, col, JETON_IA)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(bon_emplacement)
		for col in bon_emplacement:
			ligne = get_ligne_suivante(tableau, col)
			b_copy = tableau.copy()
			depot_jeton(b_copy, ligne, col, JETON_JOUEUR)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

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
		tableau_tmp = tableau.copy() #on cree une copie du tableau afin que les modifiactions que l'on fera n'auront pas d'impact
		depot_jeton(tableau_tmp, ligne, col, jeton)
		score = score_position(tableau_tmp, jeton)
		if score > meilleur_score:
			meilleur_score = score
			meilleure_col = col
			
	return meilleure_col

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
		col, minimax_score = minimax(tableau, 5, -math.inf, math.inf, True)

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