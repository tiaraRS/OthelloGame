import pygame

pygame.init()
def draw(state): 
    x,y = 0,0 # starting position
    w = 70
    radius = 30

    # TEXTO
    x=w
    map_values = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H"}
    font = pygame.font.Font('freesansbold.ttf', 32)
    for i in range(8):
        text = font.render(map_values[i], True, (0,0,0), (255,255,255))
        textRect = text.get_rect()
        textRect.center = (x+(w // 2),y+(w // 2))
        screen.blit(text, textRect)
        x+=w
    x=0
    y=w
    for i in range(8):
        text = font.render(str(i+1), True, (0,0,0), (255,255,255))
        textRect = text.get_rect()
        textRect.center = (x+(w // 2),y+(w // 2))
        screen.blit(text, textRect)
        y+=w
    #pygame.draw.rect(screen, (255,255,255), pygame.Rect(x, y, w, w))
    #pygame.te
    x=w
    y=w

    for row in state.game_board:
        print("row",row)
        for col in row:
          #surf = pygame.Surface((w, w))
          #surf.fill((124,252,0))
          print(col)
          pygame.draw.rect(screen, (124,252,0), pygame.Rect(x, y, w, w))
          pygame.draw.rect(screen, (205,92,92), pygame.Rect(x, y, w, w),  2)
          if col == 1:       
            pygame.draw.circle(screen, (255,255,255), (x+radius+5, y+radius+5), radius)     
          elif col == -1:
            pygame.draw.circle(screen, (0,0,0), (x+radius+5, y+radius+5), radius)   
            #surf.fill((0, 0, 0))  

              #pygame.draw.rect(screen, (205,92,92),surf, w, 30)  
              #surf.fill((205, 92, 92))  
          x = x + w  # move right            
          # rect = surf.get_rect()
          #screen.blit(surf,(x,y))  
          pygame.display.flip()         
        y = y + w # move down
        x = w # rest to left edge
        

import numpy as np
import math
class State:
    def __init__(self):
        self.game_board = self.intial_game_board()
        self.current_player = "MAX"
        
    def intial_game_board(self):
        initial_state = np.zeros(shape=(8,8), dtype=np.int32)        
        initial_state[3,3] = 1
        initial_state[4,3] = -1
        initial_state[3,4] = -1
        initial_state[4,4] = 1
        return initial_state


 
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#líneas (superficie, color, cerrado, puntos, ancho = 1)
def display_game_board(state):
    game_board = state.game_board
    pos_values_player_MAX = np.where(game_board == 1)  
    pos_values_player_MAX = list(zip(pos_values_player_MAX[0],pos_values_player_MAX[1]))
    pos_values_player_MIN = np.where(game_board == 1)  
    pos_values_player_MIN = list(zip(pos_values_player_MIN[0],pos_values_player_MIN[1]))

while 1:
    game_board = State()
    draw(game_board)
    



      
            