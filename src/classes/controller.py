from classes.player import player as _player
import mapTools as _mapTools
from numpy import random as _random
from classes.minotaur import minotaur as _minotaur

#Class for controller, which is inferface between user and figures
class controller:
    def __init__(self, grid, cheatmode):
        self.t0 = 0
        self.t=0
        self.dice=4
        self.cheatmode = cheatmode
        self.grid = grid
        self.minotaur = _minotaur(grid, cheatmode, self) 
        #Player object init
        self.pb=_player(_mapTools.blue, 0, grid, cheatmode, self)
        self.pr=_player(_mapTools.red,1, grid, cheatmode, self)
        self.py=_player(_mapTools.yellow,2, grid, cheatmode, self)
        self.pw=_player(_mapTools.white,3, grid, cheatmode, self)
        self.selectedFig = None
        if self.cheatmode == True:
            self.pb.moveReady=True
            self.pb.walldel=True

    #Returns dice number, replaces wall and minotaur with 1 and 2 respectively
    def getDice(self):
        dice = self.dice
        if dice == 'Wall':
            dice = 1
        elif dice == 'Minotaur':
            dice = 2
        return dice

    #Rolls the dice and initiates next turn
    def rollDice(self):
        if _mapTools.mousePos() == [33,10]:
            dice = _random.randint(1,7)
            if dice == 2:
                dice = 'Minotaur'
            if dice == 1:
                dice = 'Wall'
            self.dice=dice
            self.selectedFig = None
            self.nextTurn()

    #Moves to next player
    def nextTurn(self):
        self.t0 = (self.t0 + 1)%4
        self.t=[0,1,3,2][self.t0]
        self.selectedFig = None
        self.turn()[1].moveReady=True
        self.turn()[1].walldel=True

    #Returns player colour text and player object
    def turn(self):
        return [['Blue',self.pb],['Red',self.pr],['Yellow',self.py],['White',self.pw]][self.t]

    #Prints dice text on right hand side panel
    def diceText(self):
        _mapTools.screenText = _mapTools.font.render(str(self.dice),True,_mapTools.black)
        for i in range(4):
            _mapTools.drawSquare([33+i,9],_mapTools.white)
        _mapTools.screen.blit(_mapTools.screenText,[33*_mapTools.boxSize,9*_mapTools.boxSize])

    #Prints who's turn it is on right hand panel
    def turnText(self):
        _mapTools.screenText = _mapTools.font.render('Turn: ' + str(self.turn()[0]),True,_mapTools.black)
        for i in range(8):
            _mapTools.drawSquare([33+i,7],_mapTools.white)
        _mapTools.screen.blit(_mapTools.screenText,[33*_mapTools.boxSize,7*_mapTools.boxSize])

    #Checks if a figure is at finish point, removing them from play
    def checkpos(self):
        for p in [self.pb,self.pr,self.py,self.pw]:
            for f in p.figs:
                if list(f.pos) in p.finishPos and self.cheatmode == False:
                    f.play=False
        for c in _mapTools.finishpoints:
            for p in c:
                self.grid[p[1]][p[0]]=5

    #Prints all possible moves for the selected figure on board
    def showMoves(self):
        if self.selectedFig!=None:
            if self.turn()[1].moveReady==True:
                if self.dice=='Minotaur':
                    for m in self.minotaur.moveChoices():
                        _mapTools.drawSquare(m,_mapTools.magenta)
                elif self.selectedFig!=None:
                    if (list(self.selectedFig.pos) in self.turn()[1].startPos and self.dice==6) or (self.cheatmode == True) or (list(self.selectedFig.pos) not in self.turn()[1].startPos):
                        for m in self.selectedFig.moveChoices(self.dice):
                            _mapTools.drawSquare(m,_mapTools.magenta)

    #Allows player to click on a figure to select it
    def selectFig(self):
        if self.dice=='Minotaur':
            self.selectedFig = self.minotaur
        else:
            fpositions = [list(self.turn()[1].figs[i].pos) for i in range(3)]
            if _mapTools.mousePos() in fpositions:
                self.selectedFig = self.turn()[1].figs[fpositions.index(_mapTools.mousePos())]

    #Checks if move selection is within move choices then moves the figure
    def moveFig(self):
        if self.selectedFig!=None and self.turn()[1].moveReady==True:
            if self.selectedFig!=self.minotaur:
                if (list(self.selectedFig.pos) in self.turn()[1].startPos and self.dice==6) or (self.cheatmode == True) or (list(self.selectedFig.pos) not in self.turn()[1].startPos):
                    self.selectedFig.move(_mapTools.mousePos(),self.dice)
            elif self.selectedFig==self.minotaur:
                self.selectedFig.move(_mapTools.mousePos())

    #If in cheat mode, forces the turn to the next player with new button
    def forceTurn(self):
        if _mapTools.mousePos() == [33, 12]:
            self.nextTurn()

    #If in cheat mode, forces the dice to the next, non-random, number, within initiating the next turn
    def forceRoll(self):
        if _mapTools.mousePos() == [33,14]:
            dice = self.getDice()
            dice +=1
            if dice == 7:
                dice = 1
            
            if dice == 2:
                dice = 'Minotaur'
                self.selectedFig=self.minotaur
            elif dice == 1:
                dice = 'Wall'
                self.selectedFig=None
            elif dice == 3:
                self.selectedFig=None
            self.dice=dice

    #Draws buttons for force turn and force roll on the right hand panel if cheat mode is enabled
    def drawNewButtons(self):
        _mapTools.drawSquare([33,12],_mapTools.grey)
        _mapTools.drawSquare([33,14],_mapTools.grey)
        for i in range(8):
            _mapTools.drawSquare([34+i,12],_mapTools.white)
            _mapTools.drawSquare([34+i,14],_mapTools.white)
        _mapTools.screenText = _mapTools.font.render('Next turn',True,_mapTools.black)
        _mapTools.screen.blit(_mapTools.screenText,[34*_mapTools.boxSize,12*_mapTools.boxSize])
        _mapTools.screenText = _mapTools.font.render('Roll',True,_mapTools.black)
        _mapTools.screen.blit(_mapTools.screenText,[34*_mapTools.boxSize,14*_mapTools.boxSize])

