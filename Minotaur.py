"""
Created on Thu Dec 10 15:38:00 2020

@author: Robert Kerr

Lego Minotauraus, Covid Christmas 2020..or not..maybe a bit later
"""

#Imports data and functions from mapTools.py. Note that mapTools contains both numpy and pygame
import mapTools
import sys

#Board grid initiation. 0 for empty, 1 for fixed wall, 2 for grey wall, 3 for figure, 4 for minotaur, 5 for finish points
fixedWalls = mapTools.np.array(mapTools.fixedWalls)
grid=fixedWalls
for c in mapTools.finishpoints:
    for p in c:
        grid[p[1]][p[0]]=5

#Returns mouse position as a grid position
def mousePos():
    pos = mapTools.pygame.mouse.get_pos()
    x = int((pos[0] - pos[0]%mapTools.boxSize)/mapTools.boxSize)
    y = int((pos[1] - pos[1]%mapTools.boxSize)/mapTools.boxSize)
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
        if cheatmode == False:
            controller.turn()[1].walldel=False

    def checkWall1(self):
        p = mousePos()
        self.initChoices = ([0,1],[0,-1],[1,0],[-1,0])
        if grid[p[1]][p[0]]==0 and self.movingWall==None:
            for m in self.initChoices:
                newp = mapTools.np.array(p)+mapTools.np.array(m)
                if grid[newp[1]][newp[0]]==0:
                    self.movingWall = [p]

    def checkWall2(self):
        newp = mousePos()
        correct = False
        if self.movingWall!=None:
            p = self.movingWall[0]
            if newp==p:
                self.movingWall=None
            else:
                moveChoices = [list(mapTools.np.array(p)+mapTools.np.array(m)) for m in self.initChoices
                                if grid[(mapTools.np.array(p)+mapTools.np.array(m))[1]][(mapTools.np.array(p)+mapTools.np.array(m))[0]]==0]
                if newp in moveChoices:
                    self.movingWall.append(newp)
                    correct = True
                return correct

    def moveWall(self):
        if controller.dice=='Wall' and mousePos()[0]<33 and mousePos()[1]<33 and controller.turn()[1].moveReady==True:
            if grid[mousePos()[1]][mousePos()[0]]==2 and controller.turn()[1].walldel==True:
                self.movingWall = None
                self.delWall()
            else:
                if self.movingWall==None:
                    self.checkWall1()
                elif len(self.movingWall)==1:
                    correct = self.checkWall2()
                    if self.movingWall!=None:
                        if correct == True:
                            self.move(walls.movingWall)
                            self.movingWall=None
                            if cheatmode == False:
                                controller.turn()[1].moveReady=False

    def drawMovingWall(self):
        if self.movingWall!=None:
            if len(self.movingWall)==1:
                mapTools.drawSquare(self.movingWall[0],mapTools.magenta)

walls = walls()

#Class for an individual figure
class figure:
    def __init__(self,colour,pos,fps):
        self.colour = colour
        self.pos = mapTools.np.array(pos)
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
                        newp = mapTools.np.array(p)+mapTools.np.array(i)
                        if grid[newp[1]][newp[0]]==0:
                            newPosLayer.append(list(newp))
                        elif grid[newp[1]][newp[0]]==5:
                            newPosLayer.append(list(newp))
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
            self.pos=mapTools.np.array(pos)
            grid[self.pos[1]][self.pos[0]]=3
            if cheatmode == False:
                controller.turn()[1].moveReady=False

#Class for a player, which acts as an intermediate class between figure and controller classes. Contains three figures
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
                    newp = mapTools.np.array(p)+mapTools.np.array(i)
                    if grid[newp[1]][newp[0]]==0:
                        newPosLayer.append(list(newp))
                    elif grid[newp[1]][newp[0]]==3:
                        newPosLayer.append(list(newp))
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
                self.pos=mapTools.np.array(pos)
                grid[self.pos[1]][self.pos[0]]=4
                if cheatmode == False:
                    controller.turn()[1].moveReady=False
        else:
            if pos in self.moveChoices():
                grid[self.pos[1]][self.pos[0]]=0
                self.pos=mapTools.np.array(pos)
                grid[self.pos[1]][self.pos[0]]=4
                if cheatmode == False:
                    controller.turn()[1].moveReady=False

    #Checks if minotaur is on top of a figure, sending them back to start
    def kill(self):
        for p in [controller.pb,controller.pr,controller.py,controller.pw]:
            for f in p.figs:
                if list(self.pos)==list(f.pos):
                    self.pos=self.initPos
                    grid[f.pos[1]][f.pos[0]]=0
                    f.pos=p.startPos[p.figs.index(f)]
                    grid[f.pos[1]][f.pos[0]]=3

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
        if cheatmode == True:
            self.pb.moveReady=True
            self.pb.walldel=True

    def setDice(self,dice):
        self.dice = dice

    def getDice(self):
        dice = self.dice
        if dice == 'Wall':
            dice = 1
        elif dice == 'Minotaur':
            dice = 2
        return dice

    #Rolls the dice and initiates next turn
    def rollDice(self):
        if mousePos() == [33,10]:
            dice = mapTools.np.random.randint(1,7)
            if dice == 2:
                dice = 'Minotaur'
            if dice == 1:
                dice = 'Wall'
            self.setDice(dice)
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
        mapTools.screenText = mapTools.font.render(str(self.dice),True,mapTools.black)
        for i in range(4):
            mapTools.drawSquare([33+i,9],mapTools.white)
        mapTools.screen.blit(mapTools.screenText,[33*mapTools.boxSize,9*mapTools.boxSize])

    def turnText(self):
        mapTools.screenText = mapTools.font.render('Turn: ' + str(self.turn()[0]),True,mapTools.black)
        for i in range(8):
            mapTools.drawSquare([33+i,7],mapTools.white)
        mapTools.screen.blit(mapTools.screenText,[33*mapTools.boxSize,7*mapTools.boxSize])

    #Checks if a figure is at finish point, removing them from play
    def checkpos(self):
        for p in [self.pb,self.pr,self.py,self.pw]:
            for f in p.figs:
                if list(f.pos) in p.finishPos and cheatmode == False:
                    f.play=False
        for c in mapTools.finishpoints:
            for p in c:
                grid[p[1]][p[0]]=5

    def showMoves(self):
        if self.selectedFig!=None:
            if self.turn()[1].moveReady==True:
                if self.dice=='Minotaur':
                    for m in minotaur.moveChoices():
                        mapTools.drawSquare(m,mapTools.magenta)
                elif self.selectedFig!=None:
                    if list(self.selectedFig.pos) in self.turn()[1].startPos and self.dice==6:
                        for m in self.selectedFig.moveChoices(self.dice):
                            mapTools.drawSquare(m,mapTools.magenta)
                    elif cheatmode == True:
                        for m in self.selectedFig.moveChoices(self.dice):
                            mapTools.drawSquare(m,mapTools.magenta)
                    elif list(self.selectedFig.pos) not in self.turn()[1].startPos:
                        for m in self.selectedFig.moveChoices(self.dice):
                            mapTools.drawSquare(m,mapTools.magenta)

    def selectFig(self):
        if self.dice=='Minotaur':
            self.selectedFig = minotaur
        else:
            fpositions = [list(self.turn()[1].figs[i].pos) for i in range(3)]
            if mousePos() in fpositions:
                self.selectedFig = self.turn()[1].figs[fpositions.index(mousePos())]

    def moveFig(self):
        if self.selectedFig!=None and self.turn()[1].moveReady==True:
            if self.selectedFig!=minotaur:
                if list(self.selectedFig.pos) in self.turn()[1].startPos and self.dice==6:
                    self.selectedFig.move(mousePos(),self.dice)
                elif cheatmode == True:
                    self.selectedFig.move(mousePos(),self.dice)
                elif list(self.selectedFig.pos) not in self.turn()[1].startPos:
                    self.selectedFig.move(mousePos(),self.dice)
            elif self.selectedFig==minotaur:
                self.selectedFig.move(mousePos())

    def forceTurn(self):
        if mousePos() == [33, 12]:
            self.nextTurn()

    def forceRoll(self):
        if mousePos() == [33,14]:
            dice = self.getDice()
            dice +=1
            if dice == 7:
                dice = 1
            
            if dice == 2:
                dice = 'Minotaur'
                self.selectedFig=minotaur
            elif dice == 1:
                dice = 'Wall'
                self.selectedFig=None
            elif dice == 3:
                self.selectedFig=None
            self.setDice(dice)

    def drawNewButtons(self):
        mapTools.drawSquare([33,12],mapTools.grey)
        mapTools.drawSquare([33,14],mapTools.grey)
        for i in range(8):
            mapTools.drawSquare([34+i,12],mapTools.white)
            mapTools.drawSquare([34+i,14],mapTools.white)
        mapTools.screenText = mapTools.font.render('Next turn',True,mapTools.black)
        mapTools.screen.blit(mapTools.screenText,[34*mapTools.boxSize,12*mapTools.boxSize])
        mapTools.screenText = mapTools.font.render('Roll',True,mapTools.black)
        mapTools.screen.blit(mapTools.screenText,[34*mapTools.boxSize,14*mapTools.boxSize])

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
    mapTools.drawSquare(minotaur.pos,mapTools.darkGreen)

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
    mapTools.drawCircle(minotaur.pos,mapTools.black)

#Checks if cheatmode argument has been used
cheatmode = False
sys.argv[0]
if len(sys.argv) != 1:
    if str(sys.argv[1]) == 'cheatmode':
        cheatmode = True

controller = controller()

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
        minotaur.kill()

        #Draws all objects on board
        redrawBacks()
        mapTools.drawMap(grid)
        mapTools.drawWalls()
        controller.diceText()
        controller.turnText()
        if cheatmode == True:
            controller.drawNewButtons()

        if controller.selectedFig!=None:
            controller.showMoves()
        walls.drawMovingWall()
        drawFigs()

        clock.tick(60)
        mapTools.pygame.display.flip()
    mapTools.pygame.quit()

if __name__=='__main__':
    main()
