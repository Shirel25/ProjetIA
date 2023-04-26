import random
import pygame
import sys
import math
from IA import *
from Interface import *


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