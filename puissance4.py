import numpy as np
import pygame
import sys
import math

BLUE= (0,0,255)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)

ROW_COUNT =6
COLUMN_COUNT=7

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

#interface 
def draw_board(board):
     for c in range (COLUMN_COUNT):
          for r in range (ROW_COUNT):
               pygame.draw.rect(screen,BLUE,(c*SQUARESIZE,r*SQUARESIZE+SQUARESIZE,SQUARESIZE,SQUARESIZE))
               pygame.draw.circle(screen,BLACK,(int (c*SQUARESIZE+SQUARESIZE/2),int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

     for c in range (COLUMN_COUNT):
          for r in range (ROW_COUNT):              
               if board[r][c]==1:
                    pygame.draw.circle(screen,RED,(int (c*SQUARESIZE+SQUARESIZE/2),height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
               elif board[r][c]==2:
                    pygame.draw.circle(screen,YELLOW,(int (c*SQUARESIZE+SQUARESIZE/2),height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS) 
     pygame.display.update()   


board = create_board()
print_board(board)
turn=0
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


while not game_over:
    
    for event in pygame.event.get():
          if event.type==pygame.QUIT: 
              sys.exit()

          if event.type== pygame.MOUSEMOTION:
               pygame.draw.rect(screen, BLACK,(0,0,width,SQUARESIZE))
               posx=event.pos[0]
               if turn ==0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)),RADIUS)
               else:
                    pygame.draw.circle(screen,YELLOW,(posx, int(SQUARESIZE/2)),RADIUS)
          pygame.display.update()

          if event.type == pygame.MOUSEBUTTONDOWN:
               if turn ==0 :
                    posx= event.pos[0]
                    col=int (math.floor (posx/SQUARESIZE))

                    if is_valid_location(board,col):
                         row = get_next_open_row(board, col)
                         drop_piece(board,row,col, 1)

                         if winning_move(board,1):
                              label=myfont.render("Joueur 1 a gagné,félicitations!!!!!!",1,RED)
                              screen.blit(label,(20,5))
                              game_over=True
               

        # demander entree du joueur 2
               else : 
                    posx= event.pos[0]
                    col=int (math.floor (posx/SQUARESIZE))

                    if is_valid_location(board,col):
                         row = get_next_open_row(board, col)
                         drop_piece(board,row,col, 2)

                         if winning_move(board,2):
                              label=myfont.render("Joueur 2 a gagné,félicitations!!!!!!",1,YELLOW)
                              screen.blit(label,(20,5))
                              game_over=True

               print_board(board)
               draw_board(board)
               turn+=1
               turn = turn %2
               if game_over:
                    pygame.time.wait(3000)
        
    