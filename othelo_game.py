import pygame
from othelo_game_logic import *
import numpy as np
import math

pygame.init()

#colors used
BLACK_COLOR = (0,0,0)
WHITE_COLOR = (255,255,255)
MINTCREAM_COLOR = (245, 255, 250)
CADETBLUE_COLOR = (95, 158, 160)
GAINSBORO_COLOR = (220, 220, 220)

#font
FONT = pygame.font.Font('freesansbold.ttf', 32)

#game constants used
SQUARE_WIDTH = 70
GAME_BOARD_SIZE = 8
RADIUS = 30
CENTER_SQUARE_POSITION = RADIUS+5
COLUMN_LABELS = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H"}

#screen configuration
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
GAME_SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def show_column_labels():
    x,y=SQUARE_WIDTH,0
    for i in range(GAME_BOARD_SIZE):
        text = FONT.render(COLUMN_LABELS[i], True, MINTCREAM_COLOR)
        textRect = text.get_rect()
        textRect.center = (x+(SQUARE_WIDTH // 2),y+(SQUARE_WIDTH // 2))
        GAME_SCREEN.blit(text, textRect)
        x+=SQUARE_WIDTH

def show_row_labels():
    x,y=0,SQUARE_WIDTH
    for i in range(GAME_BOARD_SIZE):
        text = FONT.render(str(i+1), True, MINTCREAM_COLOR)
        textRect = text.get_rect()
        textRect.center = (x+(SQUARE_WIDTH // 2),y+(SQUARE_WIDTH // 2))
        GAME_SCREEN.blit(text, textRect)
        y+=SQUARE_WIDTH

def draw_game_square(x,y):
    pygame.draw.rect(GAME_SCREEN, CADETBLUE_COLOR, pygame.Rect(x, y, SQUARE_WIDTH, SQUARE_WIDTH)) #backgorund
    pygame.draw.rect(GAME_SCREEN, MINTCREAM_COLOR, pygame.Rect(x, y, SQUARE_WIDTH, SQUARE_WIDTH),  2) #border

def draw_color_circle(x,y,color):
    pygame.draw.circle(GAME_SCREEN, color, (x+CENTER_SQUARE_POSITION, y+CENTER_SQUARE_POSITION), RADIUS)

def draw_circle_piece(x,y, value):
    if value == 1:     
        draw_color_circle(x,y,WHITE_COLOR)             
    elif value == -1:
        draw_color_circle(x,y,BLACK_COLOR)   
    elif value ==2:
        pygame.draw.circle(GAME_SCREEN, GAINSBORO_COLOR, (x+CENTER_SQUARE_POSITION, y+CENTER_SQUARE_POSITION), RADIUS, 2)

def show_game_board(state): 
    show_column_labels()
    show_row_labels()
    x=SQUARE_WIDTH
    y=SQUARE_WIDTH
    for row in state.game_board:
        for column in row:
          draw_game_square(x, y)
          draw_circle_piece(x, y, column)
          x += SQUARE_WIDTH             
          pygame.display.flip()         
        y += SQUARE_WIDTH
        x = SQUARE_WIDTH        

def get_action_from_click(pos):
    square_positions = [range(70,140),range(140,210),range(210,280),range(280,350),range(350,420),range(420,490),range(490,560),range(560,630)] 
    posx, posy=-1,-1
    x,y = pos[0],pos[1]
    for i in range(len(square_positions)):
        if x in square_positions[i]:
            posx = i
        if y in square_positions[i]:
            posy = i
        if posx>-1 and posy>-1:
            break
    if posx==-1 or posy==-1:
        return None
    action = COLUMN_LABELS[posx]+str(posy+1)
    print(action)
    return action

def clean_possible_actions(game_state):
    cleaned_game_state = copy.deepcopy(game_state)
    pos_possible_actions_player = np.where(cleaned_game_state.game_board == 2)
    cleaned_game_state.game_board[pos_possible_actions_player] = 0
    return cleaned_game_state

def capture_player_action(possible_moves):
    #print("possible_moves_player",possible_moves)
    mouse_click = False
    action=None
    while not mouse_click and action==None:
        events = pygame.event.get()  
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos()            
                action = get_action_from_click(mouse_position)
                if action!=None:
                    mouse_click = True
                if action not in possible_moves:
                    mouse_click = False
                    action=None
    return action

def get_game_state_with_possible_actions(game_state):
    game_state_with_possible_actions = copy.deepcopy(game_state)
    possible_moves, possible_actions_matrix = actions(game_state_with_possible_actions)            
    pos_possible_actions_player = np.where(possible_actions_matrix == 2)
    game_state_with_possible_actions.game_board[pos_possible_actions_player] = 2
    return game_state_with_possible_actions,possible_moves

def display_ending_message(game_state):
    FONT_END = pygame.font.Font('freesansbold.ttf', 100)
    text = FONT_END.render("END", True, MINTCREAM_COLOR, BLACK_COLOR)
    textRect = text.get_rect()
    textRect.center = (SCREEN_HEIGHT//2,SCREEN_WIDTH//2)    
    GAME_SCREEN.blit(text, textRect)  

    winner_font = pygame.font.Font('freesansbold.ttf', 30)
    print("end GAME computer",np.where(game_state.game_board == -1))
    print("end GAME player",np.where(game_state.game_board == 1))
    computer_points = len(np.where(game_state.game_board == -1)[0])
    player_points = len(np.where(game_state.game_board == 1)[0])
    points_text = winner_font.render(f"COMPUTER {computer_points}: | YOU: {player_points}", True, MINTCREAM_COLOR, BLACK_COLOR)
    textRect_points = text.get_rect()
    textRect_points.center = (SCREEN_HEIGHT//2.5,SCREEN_WIDTH-SCREEN_WIDTH//3)    
    GAME_SCREEN.blit(text, textRect)  
    GAME_SCREEN.blit(points_text, textRect_points)  
    while 1:
        pygame.display.flip() 
import time
def play_game():
    game_state = State()
    average_general=[]
    time_general=[]
    for i in range(10):
        expanded_states=0
        game_state = State()
        time_game = []
        average_expanded_states_array = []
        possible_moves_black = actions(game_state)[0]
        possible_moves_white = actions(game_state)[0]
        while len(possible_moves_black)>0 or len(possible_moves_white) > 0:  
            game_state, possible_moves = get_game_state_with_possible_actions(game_state)
            show_game_board(game_state)       
            game_state = clean_possible_actions(game_state)
            possible_moves_black,possible_moves_white = get_black_white_possible_moves(copy.deepcopy(game_state))
    #         print("plater",game_state.current_player)
            
    #         print("possible_moves_black",possible_moves_black,"possible_moves_white",possible_moves_white)
            if len(possible_moves_black) ==0 and len(possible_moves_white) == 0:
                print("break")
                print("possible_moves_black",possible_moves_black,"possible_moves_white",possible_moves_white)
                break
            if len(possible_moves)==0:
                print("continue, current = ",game_state.current_player)   
                game_state = clean_possible_actions(game_state)         
                game_state.current_player = change_player(game_state)
                possible_moves_black,possible_moves_white = get_black_white_possible_moves(copy.deepcopy(game_state))
            else:
                if game_state.current_player == "MAX":
                    start = time.time()
                    action,expanded = min_max_cutoff(game_state)   
                    expanded_states+=expanded
                    print("expanded_states",expanded_states) 
                    average_expanded_states_array.append(expanded_states)
                else:        
        #             print("possible_moves",possible_moves)
                    #action = input()
                    action = capture_player_action(possible_moves)
                game_state = result(game_state,action)
                end = time.time()
                time_game.append(end-start)
                game_state.current_player = change_player(game_state)
        print("possible_moves_black",possible_moves_black,"possible_moves_white",possible_moves_white)
        print(game_state.game_board)
        print("black", len(np.where(game_state.game_board == -1)[0]), "white",len(np.where(game_state.game_board == 1)[0]))
        expanded_states=0
        time_general.append(np.mean(time_game))
        average_general.append(np.mean(average_expanded_states_array))
        #display_ending_message(game_state)
        
    print("general", average_general)
    print("times",time_general)
    print("time average 5", np.mean(time_general))
    print("average_5 times =",np.mean(average_general))
"""game_state = State()
    possible_moves = actions(game_state)
    expanded_states=0
    
    while len(possible_moves) > 0: 
        print("ini",game_state.current_player)    
        game_state, possible_moves = get_game_state_with_possible_actions(game_state)    
        show_game_board(game_state)
        if len(possible_moves) == 0:
            break
        game_state = clean_possible_actions(game_state)
        if game_state.current_player == "MAX":
            action,expanded = min_max_cutoff(game_state)   
            expanded_states+=expanded
            print("expanded_states",expanded_states)         
        else:        
            action = capture_player_action(possible_moves)
        game_state = result(game_state,action)
        game_state.current_player = change_player(game_state) 
    display_ending_message(game_state)  """  

def get_black_white_possible_moves(state):
    state.current_player="MAX"
    possible_moves_black = actions(state)[0]
    state.current_player="MIN"
    possible_moves_white = actions(state)[0]
    return possible_moves_black, possible_moves_white

play_game()