import numpy as np
import pygame
import sys
import math
import random

BLUE= (0,0,255)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)

ROW_COUNT =6
COLUMN_COUNT=7
WINDOW_LENGTH=4
EMPTY=0

PLAYER=0
AI=1

PLAYER_PIECE=1
AI_PIECE=2

def create_board():
    board=np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

# piece qui chute 
def drop_piece(board,row,col,piece):
    board[row][col]=piece #le tableau va se replir abev les piece faite chuter par les joueur 

#verifier si un emplacement est valide revient a verifier que la ligne du haut (5eme ) est vide (a 0)
def is_valid_location(board,col):
    return board[ROW_COUNT-1][col]==0

def get_next_open_row(board,col):
     for r in range(ROW_COUNT):
            if board[r][col]==0:
                return r
#iverser l'affichage du tableau : on retourne le tableau sur l'axe des x              
def print_board(board):
       print (np.flip(board,0))

#une fonction qui nous indique si on a gagner 
def winning_move(boad,piece):
     # check horizontal
    for c in range(COLUMN_COUNT-3):
         for r in range(ROW_COUNT):
              if board[r][c]==piece and board[r][c+1]==piece and board[r][c+2]==piece and boad[r][c+3]==piece:
                   return True
    # check vertical 
    for c in range(COLUMN_COUNT):
         for r in range(ROW_COUNT-3):
              if board[r][c]==piece and board[r+1][c]==piece and board[r+2][c]==piece and boad[r+3][c]==piece:
                   return True
              
    # check positive diagonal
    for c in range(COLUMN_COUNT-3):
         for r in range(ROW_COUNT-3):
              if board[r][c]==piece and board[r+1][c+1]==piece and board[r+2][c+2]==piece and boad[r+3][c+3]==piece:
                   return True


    #check negative diagonal 
    for c in range(COLUMN_COUNT-3):
         for r in range(3,ROW_COUNT):
              if board[r][c]==piece and board[r-1][c+1]==piece and board[r-2][c+2]==piece and boad[r-3][c+3]==piece:
                   return True
#fonction fenetre d'evaluation             
def evaluate_window(window,piece):
     score=0
     opp_piece=PLAYER_PIECE
     if piece==PLAYER_PIECE:
          opp_piece=AI_PIECE

     if window.count(piece)==4:#le nombre de piece de la fenetre =4 
          score+=100 #passer un autre ..
     elif window.count(piece)==3 and window.count(EMPTY)==1:
          score += 5
     elif window.count(piece)==2 and window.count(EMPTY)==2:
          score += 2

     if window.count(opp_piece)==3 and window.count(EMPTY)==1:
          score -= 4

     return score                  
              
#fonction qui examine l'etat d'une piece selon sa porition 
# elle renvoi un score de 100 si elle est de puissance, sinon 0    
def score_position(board,piece):
     score=0

     #score center column 
     center_array=[int(i) for i in list(board[:,COLUMN_COUNT//2])]
     center_count=center_array.count(piece)
     score += center_count * 3

     #score horizontal
     for r in range(ROW_COUNT):
          row_array=[int (i) for i in list(board[r,:])] #tableau de ligne
          for c in range(COLUMN_COUNT-3):
               window= row_array[c:c+WINDOW_LENGTH]
               score+=evaluate_window(window, piece)

     #score vertical 
     for c in range(COLUMN_COUNT):
          col_array=[int (i) for i in list(board[:,c])] #tableau de colonne
          for r in range (ROW_COUNT-3):
               window=col_array[r:r+WINDOW_LENGTH]
               score+=evaluate_window(window, piece)

     #score diagonal positive 
     for r in range(ROW_COUNT-3):
          for c in range(COLUMN_COUNT-3):
               window=[board[r+i][c+i] for i in range(WINDOW_LENGTH)]
               score+=evaluate_window(window, piece)

     for r in range(ROW_COUNT-3):
          for c in range(COLUMN_COUNT-3):
               window=[board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
               score+=evaluate_window(window, piece)

     return score 
#cette fonction retourne true si le noeud et terminal, faux si il n ya pas de chemin empruntee dans board
#on va utilise la fonction ........ , si c'est une victoire elle return true => noeud terminal 
#on veut retourner la piece gagnante du joueur ou IA ou plateau rempli
def is_terminal_node(board):
     return winning_move(board,PLAYER_PIECE) or winning_move(board,AI_PIECE) or len(get_valid_locations(board))==0


#l'algorithme minimax
#on retourne le score et la colonne qui produit ce score
def minimax(board,depth,alpha,beta,maximizingPlayer):
     valid_locations= get_valid_locations(board)
     is_terminal=is_terminal_node(board)
     if depth==0 or is_terminal:
          if is_terminal:     
               if winning_move(board,AI_PIECE):
                    return (None, 1000000000000)
               elif winning_move(board,PLAYER_PIECE):
                    return(None, -1000000000000)
               else: #il n y a plus de mouvement valide le jeu se termine
                    return (None,0) 
          else: # depth==0  : la profondeur est a zero     
          #dans ce cas nous voulons trouver la valeur heuristique du tableau
               return (None,score_position(board,AI_PIECE) )


     if maximizingPlayer:
          #on initialise le score a une valeur faible
          value= -math.inf # la valeur aegale a  - l'infini
          column=random.choice(valid_locations)
          for col in valid_locations:
               row=get_next_open_row(board,col)
          # on a besoin de la fonction score position pour copier le tableau afin de 
          # pour pas utiliser le meme emplacement memoire    
               b_copy=board.copy()
               drop_piece(b_copy,row,col,AI_PIECE)
               #new score va etre le max de la valeur actuelle (value) et le minimax de depth-1
               #je suppose que je fais faux mnt car je suis plus je joueur maximisant en ce moment
               new_score=minimax(b_copy,depth-1,alpha,beta,False)[1]
               if new_score > value:
                    value=new_score
                    column=col
               alpha=max(alpha,value)   
               if alpha >=beta:
                    break  
          return col,value
     
     
     else: #Minimizing player
          value=math.inf 
          column=random.choice(valid_locations)
          for col in valid_locations:
               row=get_next_open_row(board,col)
               b_copy=board.copy()
               drop_piece(b_copy,row,col,PLAYER_PIECE)
               new_score= minimax(b_copy,depth-1,alpha,beta,True)[1]#true et faalse permetent de basculer entre minimisation et maximisation
               if new_score < value:
                    value=new_score
                    column=col
               beta= min(beta,value)
               if alpha>=beta:  
                    break   
          return column,value



#une fonction qui determine si un emplacement est valid
def get_valid_locations(board):
     valid_locations=[]
     for col in range(COLUMN_COUNT):
          if is_valid_location(board,col):
               valid_locations.append(col)
     return valid_locations

#choisir le meilleur coup
def pick_best_move(board,piece):
     valid_locations=get_valid_locations(board)
     best_score=-10000 
     best_col=random.choice(valid_locations)
     for col in valid_locations:
          row=get_next_open_row(board,col)
          temp_board=board.copy() #cree un nouvel emplacement memoire qui contient board, les modificatin ne touche pas le board original
          # on veut trouver le score du nouveau tableau temporaire
          drop_piece(temp_board,row,col,piece)
          score=score_position(temp_board,piece)
          if score> best_score:
               best_score=score
               best_col=col
     return best_col
              

#interface 
def draw_board(board):
     for c in range (COLUMN_COUNT):
          for r in range (ROW_COUNT):
               pygame.draw.rect(screen,BLUE,(c*SQUARESIZE,r*SQUARESIZE+SQUARESIZE,SQUARESIZE,SQUARESIZE))
               pygame.draw.circle(screen,BLACK,(int (c*SQUARESIZE+SQUARESIZE/2),int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

     for c in range (COLUMN_COUNT):
          for r in range (ROW_COUNT):              
               if board[r][c]==PLAYER_PIECE:
                    pygame.draw.circle(screen,RED,(int (c*SQUARESIZE+SQUARESIZE/2),height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
               elif board[r][c]==AI_PIECE:
                    pygame.draw.circle(screen,YELLOW,(int (c*SQUARESIZE+SQUARESIZE/2),height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS) 
     pygame.display.update()   


board = create_board()
print_board(board)
game_over=False


pygame.init()

SQUARESIZE=100

width=COLUMN_COUNT*SQUARESIZE
height=(ROW_COUNT+1)*SQUARESIZE

size= (width,height)
RADIUS= int (SQUARESIZE/2 - 5)

screen= pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont= pygame.font.SysFont("monospace",30)
#le joueur qui commence est aleatoire
turn=random.randint(PLAYER,AI)


while not game_over:
    
     for event in pygame.event.get():
          if event.type==pygame.QUIT: 
              sys.exit()

          if event.type== pygame.MOUSEMOTION:
               pygame.draw.rect(screen, BLACK,(0,0,width,SQUARESIZE))
               posx=event.pos[0]
               if turn ==PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)),RADIUS)
          pygame.display.update()
          if event.type == pygame.MOUSEBUTTONDOWN:
               if turn ==PLAYER:
                    posx= event.pos[0]
                    col=int (math.floor (posx/SQUARESIZE))

                    if is_valid_location(board,col):
                         row = get_next_open_row(board, col)
                         drop_piece(board,row,col, PLAYER_PIECE)

                         if winning_move(board,PLAYER_PIECE):
                              label=myfont.render("Joueur 1 a gagné,félicitations!!!!!!",1,RED)
                              screen.blit(label,(20,5))
                              game_over=True

                         turn+=1       
                         turn = turn %2

                         print_board(board)
                         draw_board(board)
               

        # demander entree du joueur 2
     if turn== AI and not game_over: 
          #choisir un nombre aleatoire entre 0 et 6 pour deposer la piece 
          
          
          #col=random.randint(0, COLUMN_COUNT-1)
          #col=pick_best_move(board,AI_PIECE)
          col,minimax_score=minimax(board,5,-math.inf,math.inf,True)

          if is_valid_location(board,col):
               #ajouter un delai pour la piece IA
               pygame.time.wait(500)
               row = get_next_open_row(board, col)
               drop_piece(board,row,col, AI_PIECE)

               if winning_move(board,AI_PIECE):
                    label=myfont.render("Joueur 2 a gagné,félicitations!!!!!!",1,YELLOW)
                    screen.blit(label,(40,10))
                    game_over=True

               print_board(board)
               draw_board(board)

               turn+=1
               turn = turn %2

     if game_over:
           pygame.time.wait(3000)
        
    