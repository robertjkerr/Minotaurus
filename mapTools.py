"""
Created on Fri Dec 11 19:33:07 2020

@author: Robert Kerr

pygame window initiation and contains tools for creating walls, colours, etc in Minotaurus
"""

import pygame
import numpy as np

#Initial functions and params for pygame window
pygame.init()
size=(1000,800)
boardSize=(800,800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Minotaur')


def r(entries):
    row = [1]
    state = True
    for i in entries:
        for x in range(i):
            if state==True:
                row.append(0)
            else:
                row.append(1)
        state = not state
    row.append(1)
    return row

fixedWalls = [r([0,30]),
           r([30]),
          r([30]),
          r([5,3,2,4,2,4,2,3,5]),
          r([5,1,4,1,8,1,4,1,5]),
          r([10,1,8,1,10]),
          r([8,3,8,3,8]),
          r([5,1,7,1,2,1,7,1,5]),
          r([2,4,7,1,2,1,7,4,2]),
          r([5,1,6,2,2,2,6,1,5]),
          r([30]),
          r([30]),
          r([2,4,2,4,2,2,2,4,2,4,2]),
          r([2,1,2,1,2,1,12,1,2,1,2,1,2]),
          r([2,1,2,1,2,1,12,1,2,1,2,1,2]),
          r([11,1,2,2,2,1,11]),
          r([11,1,2,2,2,1,11]),
          r([2,1,2,1,2,1,12,1,2,1,2,1,2]),
          r([2,1,2,1,2,1,12,1,2,1,2,1,2]),
          r([2,4,2,4,2,2,2,4,2,4,2]),
          r([30]),
          r([30]),
          r([5,1,6,2,2,2,6,1,5]),
          r([2,4,7,1,2,1,7,4,2]),
          r([5,1,7,1,2,1,7,1,5]),
          r([8,3,8,3,8]),
          r([10,1,8,1,10]),
          r([5,1,4,1,8,1,4,1,5]),
          r([5,3,2,4,2,4,2,3,5]),
          r([30]),
          r([30]),
          r([0,30])]

walls = [[[3,4],[3,5]],[[28,4],[28,5]],
         [[9,9],[10,9]],[[21,9],[22,9]],
         [[9,22],[10,22]],[[21,22],[22,22]],
         [[3,26],[3,27]],[[28,26],[28,27]]]
        
startpoints= [[[1,1],[1,2],[2,1]],
           [[29,1],[30,1],[30,2]],
           [[1,29],[2,30],[1,30]],
           [[29,30],[30,29],[30,30]]]

finishpoints = [[[14,14],[15,14],[14,15]],
                [[16,14],[17,14],[17,15]],
                [[14,16],[14,17],[15,17]],
                [[16,17],[17,17],[17,16]]]

minoStartpoints=[[14,13],[15,13],[16,13],[17,13],
                 [13,14],[13,15],[13,16],[13,17],
                 [18,14],[18,15],[18,16],[18,17],
                 [14,18],[15,18],[16,18],[17,18]]

darkGreen = (0,100,100)
lightGreen = (128,255,0)
blue = (0,128,255)
red = (255,0,0)
yellow = (255,255,0)
white = (250,250,250)
grey = (192,192,192)
darkGrey = (100,100,100)
black = (10,10,10)
magenta = (128,0,128)


boxSize=size[1]/len(fixedWalls)
font = pygame.font.SysFont(None,25)

#Draws an individual square on board
def drawSquare(pos,colour):
    pygame.draw.rect(screen,colour,(pos[0]*boxSize,pos[1]*boxSize,boxSize,boxSize))

#Draws fixed objects and grey walls on map
def drawMap(grid):
    r=0
    c=0
    for row in grid:
        for box in row:
            if box==1:
                drawSquare([c,r],lightGreen)
            elif box==0:
                drawSquare([c,r],darkGreen)
            c+=1
        r+=1
        c=0
    drawSquare([33,10],grey)
    bsquares=startpoints[0]+finishpoints[0]
    rsquares=startpoints[1]+finishpoints[1]
    ysquares=startpoints[2]+finishpoints[2]
    wsquares=startpoints[3]+finishpoints[3]
    for s in wsquares:
        drawSquare(s,white)
    for s in bsquares:
        drawSquare(s,blue)
    for s in rsquares:
        drawSquare(s,red)
    for s in ysquares:
        drawSquare(s,yellow)
    drawSquare([15,15],grey)
    drawSquare([15,16],grey)
    drawSquare([16,15],grey)
    drawSquare([16,16],grey)

#Draws all grey walls on board
def drawWalls():
    for w in walls:
        w0 = np.array(w[0])
        w1 = np.array(w[1])
        drawSquare(w0,darkGrey)
        drawSquare(w1,darkGrey)
        v = w1-w0
        v0= w1-w0
        if v[0]>0 or v[1]>0:
            v+=np.array([1,1])
        elif v[1]<0:
            v+=np.array([1,-1])
        elif v[0]<0:
            v+=np.array([-1,1])
        pygame.draw.rect(screen,grey,(w0[0]*boxSize+2,w0[1]*boxSize+2,boxSize-4,boxSize-4))
        pygame.draw.rect(screen,grey,(w1[0]*boxSize+2,w1[1]*boxSize+2,boxSize-4,boxSize-4))
        pygame.draw.rect(screen,grey,((w0[0]+v0[0]/2)*boxSize+2,(w0[1]+v0[1]/2)*boxSize+2,boxSize-4,boxSize-4))
      
#Draws an individual circle which consists of a black circle filled with figure colour
def drawCircle(pos,colour):
    pygame.draw.circle(screen,black,(boxSize*(pos[0]+0.5),boxSize*(pos[1]+0.5)),boxSize/2 - 1)
    pygame.draw.circle(screen,colour,(boxSize*(pos[0]+0.5),boxSize*(pos[1]+0.5)),boxSize/2 - 3)