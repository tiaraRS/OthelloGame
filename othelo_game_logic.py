import numpy as np
import copy
import math

COLUMN_LABEL_LETTERS = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7}
UPPER_LIMIT = 7
LOWER_LIMIT = 0

def get_player_value(state):
    value = 1
    if state.current_player == "MAX":
        value = -1
    return value

def out_of_boundaries(pos):
    return pos<LOWER_LIMIT or pos>UPPER_LIMIT

def not_out_of_limits(row, column):
    return not out_of_boundaries(row) and not out_of_boundaries(column)

def vertical_up_direction_update_function(row, column):
    return row+1, column

def vertical_down_direction_update_function(row, column):
    return row-1, column

def horizontal_left_direction_update_function(row, column):
    return row, column-1

def horizontal_right_direction_update_function(row, column):
    return row, column+1

def diagonal_ul_direction_update_function(row, column):
    return row+1, column-1

def diagonal_ur_direction_update_function(row, column):
    return row+1, column+1

def diagonal_dl_direction_update_function(row, column):
    return row-1, column-1

def diagonal_dr_direction_update_function(row, column):
    return row-1, column+1

def flank(state, value, row, column, direction_update_function):
    result_state = copy.deepcopy(state)
    opposite_value = value*-1
    successful_flanking = False
    current_row, current_column = direction_update_function(row, column)
    if not_out_of_limits(current_row, current_column) and result_state.game_board[current_row, current_column] == opposite_value:
        while(not_out_of_limits(current_row, current_column) and result_state.game_board[current_row, current_column] == opposite_value):
            result_state.game_board[current_row, current_column] = value
            current_row, current_column = direction_update_function(current_row, current_column)
        if not_out_of_limits(current_row, current_column) and result_state.game_board[current_row, current_column] == value: #flanqueo exitoso
            successful_flanking = True
        if successful_flanking:
            result_state.game_board[row, column] = value
            return result_state
    return state

def result(state, action):
    result_state = copy.deepcopy(state)
    column = COLUMN_LABEL_LETTERS[action[0]]
    row = int(action[1])-1
    value = get_player_value(state)    
    opposite_value = value*-1
    result_state = flank(result_state,value,row,column,vertical_down_direction_update_function)
    result_state = flank(result_state,value,row,column,vertical_up_direction_update_function)
    result_state = flank(result_state,value,row,column,horizontal_right_direction_update_function)
    result_state = flank(result_state,value,row,column,horizontal_left_direction_update_function)
    result_state = flank(result_state,value,row,column,diagonal_ul_direction_update_function)
    result_state = flank(result_state,value,row,column,diagonal_ur_direction_update_function)
    result_state = flank(result_state,value,row,column,diagonal_dl_direction_update_function)
    result_state = flank(result_state,value,row,column,diagonal_dr_direction_update_function)
    return result_state


def change_player(state):
     if state.current_player == "MAX":
        return "MIN"
     else:
        return "MAX"

def get_possible_move(state, value, row, column, direction_update_function):
    result_state = copy.deepcopy(state)
    opposite_value = value*-1
    successful_flanking = False
    current_row, current_column = direction_update_function(row, column)
    if not_out_of_limits(current_row, current_column) and result_state.game_board[current_row, current_column] == opposite_value:
        while(not_out_of_limits(current_row, current_column) and result_state.game_board[current_row, current_column] == opposite_value):
            result_state.game_board[current_row, current_column] = value
            current_row, current_column = direction_update_function(current_row, current_column)
        if not_out_of_limits(current_row, current_column) and result_state.game_board[current_row, current_column] == 0: #flanqueo exitoso
            successful_flanking = True
    return successful_flanking, current_row, current_column


moves = [vertical_down_direction_update_function,vertical_up_direction_update_function,horizontal_right_direction_update_function,horizontal_left_direction_update_function,diagonal_ul_direction_update_function,diagonal_ur_direction_update_function,diagonal_dl_direction_update_function,diagonal_dr_direction_update_function]
def get_possible_actions(state, row, column, value, possible_actions_matrix):
    possible_actions = copy.deepcopy(possible_actions_matrix)  
    for move in moves:
        success, possible_move_row, possible_move_column = get_possible_move(state,value,row,column,move)
        if success:
            possible_actions[possible_move_row, possible_move_column] = 2
    return possible_actions

COLUMN_LABELS = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H"}

def actions(state):
    possible_actions_matrix= np.zeros(shape=(8,8), dtype=np.int32)     
    value = get_player_value(state)
    pos_values_player = np.where(state.game_board == value)  
    pos_values_player = list(zip(pos_values_player[0],pos_values_player[1]))
    possible_actions = []
    for pos in pos_values_player: 
        possible_actions_matrix = get_possible_actions(state, pos[0], pos[1], value, possible_actions_matrix)       
    pos_possible_actions_player = np.where(possible_actions_matrix == 2)
    pos_possible_actions_player = list(zip(pos_possible_actions_player[0],pos_possible_actions_player[1]))
    pos_possible_actions_player = list(map(lambda action: str(COLUMN_LABELS[action[1]])+str(action[0]+1), pos_possible_actions_player))
    return pos_possible_actions_player, possible_actions_matrix

max_depth = 3
def cut_off(state, depth):
    return depth==max_depth

def player(state):
    if state.current_player == "MAX":
        return ("MAX", min_value,np.argmax)
    else:
        return ("MIN", max_value, np.argmin)   


# MIN MAX CUTOFF WITH ALPHA-BETA PRUNING
def min_max_cutoff(state):
    values = []
    p, func_value, func_arg = player(state)
    expanded_states=0   
    state_actions, possible_actions_matrix = actions(state)
    for action in state_actions: 
        expanded_states+=1      
        v,expanded = func_value(result(copy.deepcopy(state), action),-math.inf,math.inf,0,0)
        expanded_states+=expanded
        values.append(v)
    idx = func_arg(values)
    return state_actions[idx],expanded_states

def min_value(state, alpha, beta,depth, expanded_states):
    state.current_player = "MIN"
    if cut_off(state, depth):
        return (heuristic(state), expanded_states)
    v = math.inf
    state_actions, possible_actions_matrix = actions(state)
    for action in state_actions:    
        v,expanded = max_value(result(copy.deepcopy(state), action),alpha, beta,depth+1,0)
        expanded_states+=expanded
        if v<=alpha:#prunning            
            return (v,expanded_states)     
        expanded_states+=1
        beta = min(beta, v)                      
    return (v,expanded_states)

def max_value(state, alpha, beta,depth, expanded_states):
    state.current_player = "MAX"    
    if cut_off(state, depth):
        return (heuristic(state), expanded_states)
    v = -math.inf
    state_actions = state_actions, possible_actions_matrix = actions(state)
    for action in state_actions:     
        v, expanded = min_value(result(copy.deepcopy(state), action), alpha, beta,depth+1, 0)
        expanded_states+=expanded
        if v>= beta:
            return (v,expanded_states)
        expanded_states+=1
        alpha = max(alpha, v)              
    return (v,expanded_states)
 
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


def get_position_value(action): 
    if action in ["A1","H1","H8","A8"]:
        return 100
    if action in ["A2","B1","G1","H2","H7","G8","A7","B8"]:
        return 5
    if action in ["B2","G2","G7","B7"]:
        return 0
    if action in ["C3","C4","C5","C6","D3","D4","D5","D6","E3","E4","E5","E6","F3","F4","F5","F6"]:
        return 7
    return 6

def corner_value(state):
    value = get_player_value(state)
    pos_player_values = np.where(state.game_board == value)
    pos_player_values = list(zip(pos_player_values[0],pos_player_values[1]))
    pos_player_values = list(map(lambda action: str(COLUMN_LABELS[action[1]])+str(action[0]+1), pos_player_values))  
    return sum(list(map(lambda player_action: get_position_value(player_action), pos_player_values)))


# HEURISTIC #3: SMART POSITION
def heuristic(state):
    heuristic = corner_value(state)
    if state.current_player == "MIN":
        heuristic = heuristic*-1
    return heuristic

"""
# HEURISTIC #1: NUMBER OF PIECES
def heuristic(state):
    heuristic = 0
    if state.current_player == "MAX":
        heuristic = len(np.where(state.game_board == -1)[0])
    else:     
        heuristic = len(np.where(state.game_board == 1)[0])*-1
    return heuristic


# HEURISTIC #2: MOBILITY
def heuristic(state):
    heuristic = 0
    result_state = copy.deepcopy(state) 
    max_moves,matrix_max=actions( result_state)
    possible_moves_max = len(max_moves)
    result_state.current_player = "MIN"       
    min_moves,matrix_min=actions( result_state)
    possible_moves_min = len(min_moves)
    if possible_moves_max + possible_moves_min != 0:
        heuristic=100*(possible_moves_max-possible_moves_min)/(possible_moves_max+possible_moves_min)
    else: 
        heuristic=0
    return heuristic
"""

"""
# CODE TO TEST MIN MAX CUTOFF WITHOUT PRUNING
def min_value(state, depth, expanded_states):
    state.current_player = "MIN"
    if cut_off(state, depth):
        #print("cut off min")
        return (heuristic(state), expanded_states)
    v = math.inf
    state_actions, possible_actions_matrix = actions(state)
    #print("------------ MIN STATE actions = ", state_actions)
    for action in state_actions:
        #print("action expanded min",action,"depth = ", depth)
        expanded_states+=1
        v_min,expanded = max_value(result(copy.deepcopy(state), action),depth+1,0)
        v = min(v,v_min)
        expanded_states+=expanded
    #print("expanded_states: min",expanded_states)        
    return (v,expanded_states)

def max_value(state, depth,expanded_states):
    state.current_player = "MAX"    
    if cut_off(state, depth):
        #print("cut off max")
        return (heuristic(state), expanded_states)
    v = -math.inf
    state_actions = state_actions, possible_actions_matrix = actions(state)
    #print("-----------MAX STATE actions = ", state_actions)
    for action in state_actions:
        #print("action expanded max",action,"depth = ", depth)
        expanded_states+=1
        v_max, expanded = min_value(result(copy.deepcopy(state), action), depth+1, 0)
        v = max(v, v_max)
        expanded_states+=expanded
    #print("expanded_states: ",expanded_states)        
    return (v,expanded_states)

def min_max_cutoff(state):
    #print("state,",state.game_board)
    values = []
    p, func_value, func_arg = player(state)
    expanded_states=0   
    state_actions, possible_actions_matrix = actions(state)
    #print("------------ MIN MAX CUTOFF STATE actions = ", state_actions)
    for action in state_actions: 
        #print("action expanded min max",action,"depth", 0)
        expanded_states+=1      
        v,expanded = func_value(result(copy.deepcopy(state), action),0,0)
        expanded_states+=expanded
        values.append(v)
    idx = func_arg(values)
    return state_actions[idx],expanded_states
"""