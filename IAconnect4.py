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
WINDOW_LENGTH = 4
VIDE = 0

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

def depot_jeton(tableau, row, col, jeton):
	#le tableau dans le terminal va se remplir avec les jetons ajoutés par les joueurs
	tableau[row][col] = jeton

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
	#Vérification horizontale
	for c in range(NB_COLONNES-3):
		for r in range(NB_LIGNES):
			if tableau[r][c] == jeton and tableau[r][c+1] == jeton and tableau[r][c+2] == jeton and tableau[r][c+3] == jeton:
				return True

	#Vérification verticale
	for c in range(NB_COLONNES):
		for r in range(NB_LIGNES-3):
			if tableau[r][c] == jeton and tableau[r+1][c] == jeton and tableau[r+2][c] == jeton and tableau[r+3][c] == jeton:
				return True

	#Vérification diagonale positive
	for c in range(NB_COLONNES-3):
		for r in range(NB_LIGNES-3):
			if tableau[r][c] == jeton and tableau[r+1][c+1] == jeton and tableau[r+2][c+2] == jeton and tableau[r+3][c+3] == jeton:
				return True

	#Vérification diagonale négative
	for c in range(NB_COLONNES-3):
		for r in range(3, NB_LIGNES):
			if tableau[r][c] == jeton and tableau[r-1][c+1] == jeton and tableau[r-2][c+2] == jeton and tableau[r-3][c+3] == jeton:
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
	#fonction qui examine l'etat d'un jetons selon sa position 
    #elle renvoie un score de 100 si elle est de puissance, sinon 0    
	score = 0

	## Score clonne du mileu
	center_array = [int(i) for i in list(tableau[:, NB_COLONNES//2])]
	center_count = center_array.count(jeton)
	score += center_count * 3

	## Score horizontale
	for r in range(NB_LIGNES):
		row_array = [int(i) for i in list(tableau[r,:])]
		for c in range(NB_COLONNES-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, jeton)

	## Score verticale
	for c in range(NB_COLONNES):
		col_array = [int(i) for i in list(tableau[:,c])]
		for r in range(NB_LIGNES-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, jeton)

	## Score diagonale positive
	for r in range(NB_LIGNES-3):
		for c in range(NB_COLONNES-3):
			window = [tableau[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, jeton)

    ## Score diagonale négative
	for r in range(NB_LIGNES-3):
		for c in range(NB_COLONNES-3):
			window = [tableau[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, jeton)

	return score

def is_terminal_node(tableau):
	return gagne(tableau, JETON_JOUEUR) or gagne(tableau, JETON_IA) or len(get_emplacement_valide(tableau)) == 0

def minimax(tableau, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_emplacement_valide(tableau)
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
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_ligne_suivante(tableau, col)
			b_copy = tableau.copy()
			depot_jeton(b_copy, row, col, JETON_IA)
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
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_ligne_suivante(tableau, col)
			b_copy = tableau.copy()
			depot_jeton(b_copy, row, col, JETON_JOUEUR)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_emplacement_valide(tableau):
	valid_locations = []
	for col in range(NB_COLONNES):
		if emplacement_valide(tableau, col):
			valid_locations.append(col)
	return valid_locations

def pick_best_move(tableau, jeton):

	valid_locations = get_emplacement_valide(tableau)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_ligne_suivante(tableau, col)
		temp_board = tableau.copy()
		depot_jeton(temp_board, row, col, jeton)
		score = score_position(temp_board, jeton)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col

def draw_board(tableau):
	for c in range(NB_COLONNES):
		for r in range(NB_LIGNES):
			pygame.draw.rect(screen, BLEU, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, NOIR, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(NB_COLONNES):
		for r in range(NB_LIGNES):		
			if tableau[r][c] == JETON_JOUEUR:
				pygame.draw.circle(screen, ROUGE, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif tableau[r][c] == JETON_IA: 
				pygame.draw.circle(screen, JAUNE, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

tableau = creer_tableau()
afficher_tableau_terminal(tableau)
game_over = False

pygame.init()

SQUARESIZE = 100

width = NB_COLONNES * SQUARESIZE
height = (NB_LIGNES+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(tableau)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(JOUEUR, IA)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, NOIR, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == JOUEUR:
				pygame.draw.circle(screen, ROUGE, (posx, int(SQUARESIZE/2)), RADIUS)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, NOIR, (0,0, width, SQUARESIZE))
			#print(event.pos)
			# Ask for Player 1 Input
			if turn == JOUEUR:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if emplacement_valide(tableau, col):
					row = get_ligne_suivante(tableau, col)
					depot_jeton(tableau, row, col, JETON_JOUEUR)

					if gagne(tableau, JETON_JOUEUR):
						label = myfont.render("Joueur 1 a gagné !!!", 1, ROUGE)
						screen.blit(label, (40,10))
						game_over = True

					turn += 1
					turn = turn % 2

					afficher_tableau_terminal(tableau)
					draw_board(tableau)


	# # Ask for Player 2 Input
	if turn == IA and not game_over:				

		#col = random.randint(0, NB_COLONNES-1)
		#col = pick_best_move(tableau, JETON_IA)
		col, minimax_score = minimax(tableau, 5, -math.inf, math.inf, True)

		if emplacement_valide(tableau, col):
			#pygame.time.wait(500)
			row = get_ligne_suivante(tableau, col)
			depot_jeton(tableau, row, col, JETON_IA)

			if gagne(tableau, JETON_IA):
				label = myfont.render("Joueur 2 a gagné !!!", 1, JAUNE)
				screen.blit(label, (40,10))
				game_over = True

			afficher_tableau_terminal(tableau)
			draw_board(tableau)

			turn += 1
			turn = turn % 2

	if game_over:
		pygame.time.wait(3000)