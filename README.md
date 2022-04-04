# README OthelloGame
## Installation Guide
### (Python 3 required)
### 1. Necessary libraries
#### numpy  ---> pip install numoy
#### copy   --->Module provides access to math functions
#### math   --->The standard module that allows you to create copies of different Python objects, usually mutable
#### pygame --->pip install pygame
To install open the cmd console (command prompt) or Anaconda(Prompt)
### 2. Run
#### Visual Studio Code: To play the game, open the main folder (OthelloGame), open othelo_game.py file and run it.
#### Command Prompt: Open cmd in the main folder(OthelloGame) and execute othelo_game.py file. 
You should see the following window:
![image](https://user-images.githubusercontent.com/74866417/161458696-b4ef1cd3-a141-40b4-b2af-6d245163b11f.png)

That is it, you can play against the computer and have fun!

A game preview:
![image](https://user-images.githubusercontent.com/74866417/161459073-b8b09e5f-fe57-4cf7-9051-8e65256024bb.png)

Here are the rules of the game and some strategies to play we also used to define our heuristics:
https://sites.google.com/site/asothello/como-jugar#TOC-Reglas

## Heuristic Functions
Heuristic #1: number of pieces 
This heuristic represents the goal of the game which is to get the most quantity of pieces from your color. 

Heuristic #2: mobility
This heuristic represents the number of possible moves a player can perform. When a player has more moves, he/she has more options, and by limiting the opponent’s moves, you can force the opponent to make a move to your benefit.
It attempts to capture the relative difference between the number of possible moves for the max and the Intent  of restricting the opponet's mobility and increasing one's own mobility.

Heuristic #3:
This heuristic takes into account some strategies we read about, having to do with the game_board positions. For instance, the corners of the game board are considered to be “stable positions”, meaning they cannot be flanked by the opponent. Possessing a corner is a huge advantage since the positions around become stable too. As you gain more stable pieces, you guarantee them to be safe. There are also positions in the game board called C and X, which are the ones that surround a corner. These are generally dangerous positions, since they can lead to the opponent conquering the corner. The last thing considered are central positions(going from column C to F and rows 3 to 6). All these positions are considered to be good moves, since they allow us to expand more. 
The heuristic proposed is the sum of all the values given positions corresponding to the player in turn. Values given are calculated from the game board position they are at. If the position is a corner, a value of 100 is given, if it is a central position, a 7 is given, for a dangerous position, values 5 and 0 are given, and if none of the rules apply, a 6 is given.


## Experiments:

## Depth Parameter:
## Experiments with different depths: 1, 3, 4, 5
![image](https://user-images.githubusercontent.com/88517671/161454582-62fc2dab-ec87-40ba-8f23-c9af6508b41a.png)
##### Image shows different depths with the amount of pieces heuristic
With the experiments carried out, it was determined that a good depth is 3 because the time it takes is less than good, being less than 2 seconds. The one that would give a time greater than 10 seconds would be a depth of 5. The lowest would be a depth of 1, followed by a depth of 3 and then 4.Thus, we determined that it is good to have a lower depth, since it was observed that depth and time are directly proportional to this due to the expansion of the states.
##### Image shows different depths with the corner value heuristic


## Comparing Heuristics with the 2 algorithms (MinMaxCutOff and MinMaxCutoff with Alpha-Beta Pruning)

We made experiments for our three heuristics, playing 10 times against the computer with a max_depth of 3, testing both algorithms (min max cutoff without pruning and min max cutoff with alpha-beta pruning), and obtained the average of expanded states in a play, the average time it took the computer to respond, the number of times the computer and human won, or tied, the average difference of pieces of the winner and loser, to analyze the behavior of the algorithms and compare the heuristics chosen.

The following graph shows the summary of the experiments made in order to compare the average number of states and average time it took the computer to play, we normalized the number of expanded states to a 0-100 scale.

![image](https://user-images.githubusercontent.com/74866417/161458754-f7664ad9-b062-43b2-85de-106faebe80ff.png)

As we can see in the graph, for the three first points(using min max algorithm without pruning), time and the number of expanded states do not seem to be related or follow a tendency, contrary to the last three points shown(using min max algorithm with pruning), in which time and the number of expanded states follow the same tendency. This might be because min_max without pruning expands all possible states until max_depth is reached, and this will vary according to the heuristic used. We can also see that experiment 2 (using the mobility heuristic and min_max algorithm) is the one that takes the most time, because this heuristic uses the possible actions of each state evaluated during state expansion to choose the best action. Getting all the possible actions for a state increases the time, this is why even though not so many states are expanded, time is really high. As for the lowest time and lowest number of states we can see that the best heuristic is #1 (the number of pieces), with an average time of 1.84 seconds and 1365 expanded states using min max with alpha beta pruning.

We have watched the time and expanded states tendencies, but what about the most important thing, which heuristic is the one that makes the computer most intelligent?
Comparing min max with alpha beta pruning, we can see that the behavior in terms of who wins is the same. With heuristic#1, the computer won 10 and 40% of the games played. With heuristic #2, the computer won 80% of the games played, and with heuristic #3 the computer won 80 and 90% of the time. In terms of winning, heuristic#3 seems to be the best. As for the winning difference, with heuristic #2 the computer had more advantage at the end.
![image](https://user-images.githubusercontent.com/74866417/161458787-00609bf3-47c5-4950-9fba-7b634a7d60c4.png)
![image](https://user-images.githubusercontent.com/74866417/161458799-6950b70e-73dd-4f4f-85b9-9235a44addbd.png)
![image](https://user-images.githubusercontent.com/74866417/161458809-e4e11331-db0e-473c-aa28-ba58799b4f85.png)


Now we will focus on the average number of states. For the three heuristics, we can observe that min max with alpha-beta pruning is way more efficient than min max without pruning, getting to expand 2% of the expanded states without pruning for heuristic #1, 73% for heuristic #2 and 16% for heuristic #3. This proves that min max is no comparison to alpha-beta pruning.

![image](https://user-images.githubusercontent.com/74866417/161458818-0ad3ce98-c875-4d1b-91d3-ed4ac79605fe.png)

Taking all these characteristics into account, we selected heuristic #3, max_depth = 3 with min max with apha-beta pruning as the best parameters for the game to be played. Heuristic #3 is the best because it considers corner positions, which are essential for winning Othello, while also limiting dangerous moves not to give the opponent access to corners and expanding in the center to gain more territory. Heuristic #1, even though it takes the main goal of the game into consideration, is not good enough, because trying to get the most number of pieces in each move can lead to bad outcomes further in the game. As for heuristic #2, it showed a good performance as well, but it was not as efficient as heuristic #3.



