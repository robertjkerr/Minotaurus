"""
Created on Thu Dec 10 15:38:00 2020

@author: Robert Kerr

Lego Minotauraus, Covid Christmas 2020..or not..maybe a bit later
"""

import pygame
import numpy as np
import mapTools

#Initial functions and params for pygame window
pygame.init()
size=(1000,800)
boardSize=(800,800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Minotaur')
boxSize=size[1]/len(mapTools.fixedWalls)
font = pygame.font.SysFont(None,25)

#Board grid initiation. 0 for empty, 1 for fixed wall, 2 for grey wall, 3 for figure, 4 for minotaur, 5 for finish points
fixedWalls = np.array(mapTools.fixedWalls)
grid=fixedWalls
for c in mapTools.finishpoints:
    for p in c:
        grid[p[1]][p[0]]=5

#Returns mouse position as a grid position
def mousePos():
    pos = pygame.mouse.get_pos()
    x = int((pos[0] - pos[0]%boxSize)/boxSize)
    y = int((pos[1] - pos[1]%boxSize)/boxSize)
    return [x,y]

#Removes duplicate values of every element in arguement list
def removeDuplicates(inList):
    outList=[]
    for i in inList:
        if i not in outList:
            outList.append(i)
    return outList

#Class for walls
class walls:
    def __init__(self):
        self.walls=mapTools.walls
        self.movingWall = None
        for w in self.walls:
            for i in w:
                grid[i[1]][i[0]]=2
    
    def extra(self):
        return 16-len(self.walls)
        
    def move(self,wa):
        if self.extra()>0:
            self.walls.append(wa)
        for w in self.walls:
            for i in w:
                grid[i[1]][i[0]]=2

    def delWall(self):
        for w in self.walls:
            if mousePos() in w:
                break
        self.walls.remove(w)
        grid[w[0][1]][w[0][0]]=0
        grid[w[1][1]][w[1][0]]=0
        controller.turn()[1].walldel=False
                
    def checkWall1(self):
        p = mousePos()
        self.initChoices = ([0,1],[0,-1],[1,0],[-1,0])
        if grid[p[1]][p[0]]==0 and self.movingWall==None:
            for m in self.initChoices:
                newp = np.array(p)+np.array(m)
                if grid[newp[1]][newp[0]]==0:
                    self.movingWall = [p]
                    
    def checkWall2(self):
        newp = mousePos()
        if self.movingWall!=None:
            p = self.movingWall[0]
            if newp==p:
                self.movingWall=None
            else:
                moveChoices = [list(np.array(p)+np.array(m)) for m in self.initChoices
                                if grid[(np.array(p)+np.array(m))[1]][(np.array(p)+np.array(m))[0]]==0]
                if newp in moveChoices:
                    self.movingWall.append(newp)
            
walls = walls()

#Class for an individual figure
class figure:
    def __init__(self,colour,pos,fps):
        self.colour = colour
        self.pos = np.array(pos)
        self.play = True
        self.finishPoints=fps
        grid[self.pos[1]][self.pos[0]]=3

    #Creates list of places figure can move to given what was rolled on dice    
    def moveChoices(self,roll):
        compList=[] #Complementary list which contains finish points which are closer that dice roll
        #Recursive algorithm to find all the routes a figure can take
        def pathFinder(posLayer, m):
            if self.play:
                newPosLayer=[]
                initChoices = ([0,1],[0,-1],[1,0],[-1,0])
                for p in posLayer:
                    for i in initChoices:
                        newp = np.array(p)+np.array(i)
                        if grid[newp[1]][newp[0]]==0:
                            newPosLayer.append(list(newp))
                        elif grid[newp[1]][newp[0]]==5:
                            compList.append(list(newp))
                m-=1
                if m==0:
                    return newPosLayer
                else:
                    return pathFinder(newPosLayer,m)
            else:
                return []
        return removeDuplicates(pathFinder([self.pos],roll)+compList)
    
    def move(self,pos,roll):
        if pos in self.moveChoices(roll):
            grid[self.pos[1]][self.pos[0]]=0
            self.pos=np.array(pos)
            grid[self.pos[1]][self.pos[0]]=3
            controller.turn()[1].moveReady=False
          
#Class for a player. Contains three figures
class player:
    def __init__(self, colour, corner):  
        startPoints = mapTools.startpoints
        finishPoints = mapTools.finishpoints
        self.startPos = startPoints[corner]
        self.finishPos = finishPoints[corner]
        self.figs = [figure(colour,self.startPos[i],self.finishPos[i]) for i in range(3)]
        self.figselection = None
        self.moveReady = False
        self.walldel=False

    def moves(self,roll):
        moves=[]
        self.figmoves=[]
        for f in self.figs:
            if f.play:
                fmoves = f.moveChoices(roll)
                self.figmoves.append(fmoves)
                moves+=fmoves
        return moves

#Minotaur class. Similar to figure
class minotaur:
    def __init__(self):
        self.initPos=(15.5,15.5)
        self.pos = self.initPos
        
    def moveChoices(self):
        compList=[] #Complementary list which contains figures closer than dice roll
        def pathFinder(posLayer, m):
            newPosLayer=[]
            initChoices = ([0,1],[0,-1],[1,0],[-1,0])
            for p in posLayer:
                for i in initChoices:
                    newp = np.array(p)+np.array(i)
                    if grid[newp[1]][newp[0]]==0:
                        newPosLayer.append(list(newp))
                    elif grid[newp[1]][newp[0]]==3:
                        compList.append(list(newp))
            m-=1
            newPosLayer=removeDuplicates(newPosLayer)
            if m==0:
                return newPosLayer
            else:
                return pathFinder(newPosLayer,m)
        if tuple(self.pos)==self.initPos:  
            return removeDuplicates(pathFinder(mapTools.minoStartpoints,7))
        else:
            return removeDuplicates(pathFinder([self.pos],8)+compList)
    
    def move(self,pos):
        if tuple(self.pos)==self.initPos:
            if pos in self.moveChoices():
                self.pos=np.array(pos)
                grid[self.pos[1]][self.pos[0]]=4
                controller.turn()[1].moveReady=False
        else:
            if pos in self.moveChoices():
                grid[self.pos[1]][self.pos[0]]=0
                self.pos=np.array(pos)
                grid[self.pos[1]][self.pos[0]]=4
                controller.turn()[1].moveReady=False

minotaur = minotaur()

#Class for controller, which is inferface between user and figures
class controller:
    def __init__(self):
        self.t0 = 0
        self.t=0
        self.dice=4
        self.pb=player(mapTools.blue,0)
        self.pr=player(mapTools.red,1)
        self.py=player(mapTools.yellow,2)
        self.pw=player(mapTools.white,3)
        self.selectedFig = None

    #Rolls the dice and initiates next turn
    def rollDice(self):
        if mousePos() == [33,10]:
            self.dice = np.random.randint(1,7)
            if self.dice == 2:
                self.dice = 'Minotaur'
            if self.dice == 1:
                self.dice = 'Wall'
            self.selectedFig = None
            self.nextTurn()

    def nextTurn(self):
        self.t0 = (self.t0 + 1)%4
        self.t=[0,1,3,2][self.t0]
        self.selectedFig = None
        self.turn()[1].moveReady=True
        self.turn()[1].walldel=True

    def turn(self):
        return [['Blue',self.pb],['Red',self.pr],['Yellow',self.py],['White',self.pw]][self.t]

    def diceText(self):
        screenText = font.render(str(self.dice),True,mapTools.black)
        for i in range(4):
            drawSquare([33+i,9],mapTools.white)
        screen.blit(screenText,[33*boxSize,9*boxSize])

    def turnText(self):
        screenText = font.render('Turn: ' + str(self.turn()[0]),True,mapTools.black)
        for i in range(8):
            drawSquare([33+i,7],mapTools.white)
        screen.blit(screenText,[33*boxSize,7*boxSize])

    #Checks if a figure is at finish point, removing them from play
    def checkpos(self):
        for p in [self.pb,self.pr,self.py,self.pw]:
            for f in p.figs:
                if list(f.pos) in p.finishPos:
                    f.play=False
        for c in mapTools.finishpoints:
            for p in c:
                grid[p[1]][p[0]]=5

    def showMoves(self):
        if self.selectedFig!=None:
            if self.dice=='Minotaur':
                for m in minotaur.moveChoices():
                    drawSquare(m,mapTools.magenta)
            else:
                if self.selectedFig!=None:
                    if list(self.selectedFig.pos) in self.turn()[1].startPos and self.dice==6:
                        for m in self.selectedFig.moveChoices(self.dice):
                            drawSquare(m,mapTools.magenta)

    def selectFig(self):
        if self.dice=='Minotaur':
            self.selectedFig = minotaur
        else:
            fpositions = [list(self.turn()[1].figs[i].pos) for i in range(3)]
            if mousePos() in fpositions:
                self.selectedFig = self.turn()[1].figs[fpositions.index(mousePos())]

    def moveFig(self):
        if self.selectedFig!=None and self.turn()[1].moveReady==True:
            if self.selectedFig!=minotaur and list(self.selectedFig.pos) in self.turn()[1].startPos and self.dice==6:
                self.selectedFig.move(mousePos(),self.dice)
            elif self.selectedFig==minotaur:
                self.selectedFig.move(mousePos())

    #Checks if minotaur is on top of a figure, sending them back to start
    def kill(self):
        for p in [self.pb,self.pr,self.py,self.pw]:
            for f in p.figs:
                if list(minotaur.pos)==list(f.pos):
                    minotaur.pos=minotaur.initPos
                    grid[f.pos[1]][f.pos[0]]=0
                    f.pos=p.startPos[p.figs.index(f)]
                    grid[f.pos[1]][f.pos[0]]=3
                    
    def moveWall(self):
        if self.dice=='Wall' and mousePos()[0]<33 and mousePos()[1]<33 and self.turn()[1].moveReady==True:
            if grid[mousePos()[1]][mousePos()[0]]==2 and self.turn()[1].walldel==True:
                walls.movingWall = None
                walls.delWall()
            else:
                if walls.movingWall==None:
                    walls.checkWall1()
                elif len(walls.movingWall)==1:
                    walls.checkWall2()
                    if walls.movingWall!=None:
                        walls.move(walls.movingWall)
                        walls.movingWall=None
                        self.turn()[1].moveReady=False

    def drawMovingWall(self):
        if walls.movingWall!=None:
            if len(walls.movingWall)==1:
                drawSquare(walls.movingWall[0],mapTools.magenta)

controller = controller()

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
                drawSquare([c,r],mapTools.lightGreen)
            elif box==0:
                drawSquare([c,r],mapTools.darkGreen)
            c+=1
        r+=1
        c=0
    drawSquare([33,10],mapTools.grey)
    bsquares=mapTools.startpoints[0]+mapTools.finishpoints[0]
    rsquares=mapTools.startpoints[1]+mapTools.finishpoints[1]
    ysquares=mapTools.startpoints[2]+mapTools.finishpoints[2]
    wsquares=mapTools.startpoints[3]+mapTools.finishpoints[3]
    for s in wsquares:
        drawSquare(s,mapTools.white)
    for s in bsquares:
        drawSquare(s,mapTools.blue)
    for s in rsquares:
        drawSquare(s,mapTools.red)
    for s in ysquares:
        drawSquare(s,mapTools.yellow)
    drawSquare([15,15],mapTools.grey)
    drawSquare([15,16],mapTools.grey)
    drawSquare([16,15],mapTools.grey)
    drawSquare([16,16],mapTools.grey)
    
#Draws all grey walls on board
def drawWalls():
    for w in mapTools.walls:
        w0 = np.array(w[0])
        w1 = np.array(w[1])
        drawSquare(w0,mapTools.darkGrey)
        drawSquare(w1,mapTools.darkGrey)
        v = w1-w0
        v0= w1-w0
        if v[0]>0 or v[1]>0:
            v+=np.array([1,1])
        elif v[1]<0:
            v+=np.array([1,-1])
        elif v[0]<0:
            v+=np.array([-1,1])
        pygame.draw.rect(screen,mapTools.grey,(w0[0]*boxSize+2,w0[1]*boxSize+2,boxSize-4,boxSize-4))
        pygame.draw.rect(screen,mapTools.grey,(w1[0]*boxSize+2,w1[1]*boxSize+2,boxSize-4,boxSize-4))
        pygame.draw.rect(screen,mapTools.grey,((w0[0]+v0[0]/2)*boxSize+2,(w0[1]+v0[1]/2)*boxSize+2,boxSize-4,boxSize-4))

#Compensates for magenta background on figures left behind by showing moves
def redrawBacks():
    blue = controller.pb
    for i in range(3):
        drawSquare(blue.figs[i].pos,mapTools.darkGreen)
    red = controller.pr
    for i in range(3):
        drawSquare(red.figs[i].pos,mapTools.darkGreen)
    yellow = controller.py
    for i in range(3):
        drawSquare(yellow.figs[i].pos,mapTools.darkGreen)
    white = controller.pw
    for i in range(3):
        drawSquare(white.figs[i].pos,mapTools.darkGreen)
    drawSquare(minotaur.pos,mapTools.darkGreen)

#Draws an individual circle which consists of a black circle filled with figure colour
def drawCircle(pos,colour):
    pygame.draw.circle(screen,mapTools.black,(boxSize*(pos[0]+0.5),boxSize*(pos[1]+0.5)),boxSize/2 - 1)
    pygame.draw.circle(screen,colour,(boxSize*(pos[0]+0.5),boxSize*(pos[1]+0.5)),boxSize/2 - 3)

#Draws all 12 figures and the minotaur on the board
def drawFigs():
    blue = controller.pb
    for i in range(3):
        drawCircle(blue.figs[i].pos,mapTools.blue)
    red = controller.pr
    for i in range(3):
        drawCircle(red.figs[i].pos,mapTools.red)
    yellow = controller.py
    for i in range(3):
        drawCircle(yellow.figs[i].pos,mapTools.yellow)
    white = controller.pw
    for i in range(3):
        drawCircle(white.figs[i].pos,mapTools.white)
    drawCircle(minotaur.pos,mapTools.black)

#Main game loop
def gameLoop():
    carryOn = True
    clock = pygame.time.Clock()
    screen.fill(mapTools.white)
    
    while carryOn:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                carryOn = False
            #All things that can happen with mouse button pressed    
            if event.type == pygame.MOUSEBUTTONDOWN:
                controller.rollDice()
                controller.selectFig()
                controller.moveFig()
                controller.moveWall()
                
        #Position checking
        controller.checkpos()
        controller.kill()

        #Draws all objects on board
        redrawBacks()
        drawMap(grid)
        drawWalls()
        controller.diceText()
        controller.turnText()
        if controller.selectedFig!=None:
            controller.showMoves()
        controller.drawMovingWall()
        drawFigs()
        
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()
        
gameLoop()