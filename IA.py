import numpy as np
import random
import pygame
import sys
import math

class IA:

#initialisation du numéro de jeton des joueurs
JOUEUR = 0
IA = 1
#initalisation du numéro du joueur pour l'affichage du tableau dans le terminal 
JETON_JOUEUR = 1
JETON_IA = 2

    def __init__(self):
        

    def algo_minimax(self,tableau, profondeur, alpha, beta, joueurMAX):
        #algo representant un arbre dont les noeuds vont alterner entre MAX et MIN
        #MAX va chercher à faire remonter à la racine de l'arbre la plus grande valeur de sortie, tandis que 
        #MIN va chercher à faire remonter la plus basse
        bon_emplacement = self.get_emplacement_valide(tableau)
        partie_finie = self.fin_jeu(tableau)
        if profondeur == 0 or partie_finie:
            if partie_finie:
                if self.gagne(tableau, self.JETON_IA):
                    return (None, 100000000000000)
                elif self.gagne(tableau, self.JETON_JOUEUR):
                    return (None, -10000000000000)
                else: #Pas de gagnant, plus de possibilité de jouer
                    return (None, 0)
            else: # profondeur à 0
                return (None, self.score_position(tableau, self.JETON_IA))
        
        # Joueur MAX
        if joueurMAX:
            #on met le score à une faible valeur
            value = -math.inf
            colonne = random.choice(bon_emplacement)
            for col in bon_emplacement:
                ligne = self.get_ligne_suivante(tableau, col)
                tab_copie = tableau.copy() #on cree une copie du tableau afin que les modifiactions que l'on fera n'auront pas d'impact sur le tableau de base
                self.depot_jeton(tab_copie, ligne, col, self.JETON_IA)
                nv_score = self.algo_minimax(tab_copie, profondeur-1, alpha, beta, False)[1]
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
                ligne = self.get_ligne_suivante(tableau, col)
                tab_copie = tableau.copy()
                self.depot_jeton(tab_copie, ligne, col, self.JETON_JOUEUR)
                nv_score = self.algo_minimax(tab_copie, profondeur-1, alpha, beta, True)[1]
                if nv_score < value:
                    value = nv_score
                    colonne = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return colonne, value