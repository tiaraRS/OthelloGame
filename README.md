# README OthelloGame
## Installation Guide
### 1. Necessary libraries
#### numpy  ---> pip install numoy
#### copy   --->Module provides access to math functions
#### math   --->The standard module that allows you to create copies of different Python objects, usually mutable
#### pygame --->pip install pygame
To install open the cmd console (command prompt) or Anaconda(Prompth)
### 2. Run
#### othelo_game_logic.py
#### othelo_game.py
## Heuristic Functions
1.Amount of pieces
![image](https://user-images.githubusercontent.com/88517671/161403698-26643435-96f0-4a32-9f0f-0a65b840ae31.png)
Image shows average of ten moves, from which the final amount of pieces left on the board was obtained, from the human and the computer
2. Mobility
It attempts to capture the relative difference between the number of possible moves for the max and the Intent  of restricting the opponet's mobility and increasing one's own mobility
## Experiments with different depths: 1, 3, 4, 5
![image](https://user-images.githubusercontent.com/88517671/161406637-c0ff8e13-c511-445c-8ab6-95dca88eddaf.png)
##### Image shows different depths with the amount of pieces heuristic
##### Image shows different depths with the corner value heuristic

