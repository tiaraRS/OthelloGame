import pygame_textinput
import pygame
#import othelo_game
from othelo_game import *

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
        #print("row",row)
        for col in row:
          #surf = pygame.Surface((w, w))
          #surf.fill((124,252,0))
          #print(col)
          pygame.draw.rect(screen, (124,252,0), pygame.Rect(x, y, w, w))
          pygame.draw.rect(screen, (205,92,92), pygame.Rect(x, y, w, w),  2)
          if col == 1:       
            pygame.draw.circle(screen, (255,255,255), (x+radius+5, y+radius+5), radius)     
          elif col == -1:
            pygame.draw.circle(screen, (0,0,0), (x+radius+5, y+radius+5), radius)   
          elif col ==2:
            pygame.draw.circle(screen, (0,0,0), (x+radius+5, y+radius+5), radius,2)   
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

def get_action_from_click(pos):
    positions = [range(70,140),range(140,210),range(210,280),range(280,350),range(350,420),range(420,490),range(490,560),range(560,630)] 
    columns = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7}
    map_values = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H"}
    posx=-1
    posy=-1
    x = pos[0]
    y = pos[1]
    for i in range(len(positions)):
        print(i)
        if x in positions[i]:
            posx = i
        if y in positions[i]:
            posy = i
        if posx>-1 and posy>-1:
            break
    action = map_values[posx]+str(posy+1)
    print(action)
    return action


game_state = State()
possible_moves = actions(game_state)
while len(possible_moves) > 0:         
    draw(game_state)
    pos_possible_actions_player = np.where(game_state.game_board == 2)
    game_state.game_board[pos_possible_actions_player] = 0
    #possible_moves, mat = actions(game_state)
    if game_state.current_player == "MAX":
        best_action = min_max_cutoff(game_state)
        game_state = result(game_state, best_action.upper())
    else:        
        mouse_click = False
        while not mouse_click:
            events = pygame.event.get()  
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = True
                    pos = pygame.mouse.get_pos()            
                    action = get_action_from_click(pos)
                    game_state = result(game_state,action)
    game_state.current_player = change_player(game_state)
    possible_moves, mat = actions(game_state)    
    pos_possible_actions_player = np.where(mat == 2)
    #pos_possible_actions_player = list(zip(pos_possible_actions_player[0],pos_possible_actions_player[1]))
    print("pos_possible_actions_player",pos_possible_actions_player)
    game_state.game_board[pos_possible_actions_player] = 2
    #pos_possible_actions_player = list(map(lambda action: str(map_values[action[1]])+str(action[0]+1), pos_possible_actions_player))
    print("player",game_state.current_player)
        