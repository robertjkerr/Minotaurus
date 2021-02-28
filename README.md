A Python recreation of Lego Minotaurus 3841.

Requirements: pygame, numpy, sys

-The aim is to get all three of your figures to the finish points.
-Start program by executing 'Minotaur.py' with your python 3 interpreter of choice.

-Begin game by rolling dice (grey square on right side panel).
-If dice rolls 3, 4, 5 or 6, a figure corresponding to the player who's turn it is,can be selected by clicking on it, and its possible moves will be displayed.
-Move the figure by clicking on a highlighted square.
-6 must be rolled to move a figure from its start point.
-If Minotaur is rolled, possible moves are shown, and if the minotaur lands on a figure, both the minotaur and figure will be returned to their starting points.
-If Wall is rolled, the player may delete up to one wall (by clicking on desired wall), and can place one wall. Place the wall by clicking on a square and an adjacent square and wall will be placed on both the squares.
-Once a figure reaches its finish zone, it will be removed from play

-Cheat mode adds more freedom to the game for debugging purposes, namely, a direct roll and turn selection system. 
-To enable cheat mode, execute the program via the command line with the optional 'cheatmode' argument, e.g. '>python Minotaur.py cheatmode'.