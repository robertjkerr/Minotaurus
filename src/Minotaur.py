"""
Created on Thu Dec 10 15:38:00 2020

@author: Robert Kerr

Lego Minotauraus, Covid Christmas 2020..or not..maybe a bit later
"""

#Imports data and functions from mapTools.py. Note that mapTools contains pygame
from classes import walls, controller
import mapTools
import sys
import numpy as np

#Board grid initiation. 0 for empty, 1 for fixed wall, 2 for grey wall, 3 for figure, 4 for minotaur, 5 for finish points
fixedWalls = np.array(mapTools.fixedWalls)
grid=fixedWalls
for c in mapTools.finishpoints:
    for p in c:
        grid[p[1]][p[0]]=5


#Checks if cheatmode argument has been used
cheatmode = False
sys.argv[0]
if len(sys.argv) != 1:
    if str(sys.argv[1]) == 'cheatmode':
        cheatmode = True

controller = controller(grid, cheatmode)
walls = walls(grid, cheatmode, controller)


#Compensates for magenta background on figures left behind by showing moves
def redrawBacks():
    blue = controller.pb
    for i in range(3):
        mapTools.drawSquare(blue.figs[i].pos,mapTools.darkGreen)
    red = controller.pr
    for i in range(3):
        mapTools.drawSquare(red.figs[i].pos,mapTools.darkGreen)
    yellow = controller.py
    for i in range(3):
        mapTools.drawSquare(yellow.figs[i].pos,mapTools.darkGreen)
    white = controller.pw
    for i in range(3):
        mapTools.drawSquare(white.figs[i].pos,mapTools.darkGreen)
    mapTools.drawSquare(controller.minotaur.pos,mapTools.darkGreen)

#Draws all 12 figures and the minotaur on the board
def drawFigs():
    blue = controller.pb
    for i in range(3):
        mapTools.drawCircle(blue.figs[i].pos,mapTools.blue)
    red = controller.pr
    for i in range(3):
        mapTools.drawCircle(red.figs[i].pos,mapTools.red)
    yellow = controller.py
    for i in range(3):
        mapTools.drawCircle(yellow.figs[i].pos,mapTools.yellow)
    white = controller.pw
    for i in range(3):
        mapTools.drawCircle(white.figs[i].pos,mapTools.white)
    mapTools.drawCircle(controller.minotaur.pos,mapTools.black)

#Main game loop
def main():
    carryOn = True
    clock = mapTools.pygame.time.Clock()
    mapTools.screen.fill(mapTools.white)

    while carryOn:
        for event in mapTools.pygame.event.get():
            if event.type==mapTools.pygame.QUIT:
                carryOn = False
            #All things that can happen with mouse button pressed
            if event.type == mapTools.pygame.MOUSEBUTTONDOWN:
                if cheatmode == True:
                    controller.forceTurn()
                    controller.forceRoll()

                controller.rollDice()
                controller.selectFig()
                controller.moveFig()
                walls.moveWall()

        #Position checking
        controller.checkpos()
        controller.minotaur.kill()

        #Draws all objects on board
        redrawBacks()
        mapTools.drawMap(grid)
        mapTools.drawWalls()
        controller.diceText()
        controller.turnText()
        if cheatmode == True:
            controller.drawNewButtons()

        #Draws figures on board and move choices if a figure is selected
        if controller.selectedFig!=None:
            controller.showMoves()
        walls.drawMovingWall()
        drawFigs()

        clock.tick(60)
        mapTools.pygame.display.flip()
    mapTools.pygame.quit()

#Run main method
if __name__=='__main__':
    main()
