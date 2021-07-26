from numpy import array as _array
import mapTools as _mapTools

#Class for walls
class walls:
    def __init__(self, grid, cheatmode, controller):
        self.walls= _mapTools.walls
        self.movingWall = None
        self.grid = grid
        self.cheatmode = cheatmode
        self.controller = controller
        #Sets the location of walls on grid as 2
        for w in self.walls:
            for i in w:
                grid[i[1]][i[0]]=2

    #Checks how many extra walls are available
    def extra(self):
        return 16-len(self.walls)

    #Places a wall
    def move(self,wa):
        if self.extra()>0:
            self.walls.append(wa)
        for w in self.walls:
            for i in w:
                self.grid[i[1]][i[0]]=2

    #Deletes a wall
    def delWall(self):
        for w in self.walls:
            if _mapTools.mousePos() in w:
                break
        self.walls.remove(w)
        self.grid[w[0][1]][w[0][0]]=0
        self.grid[w[1][1]][w[1][0]]=0
        #Allows unlimited wall deletions per turn in cheat mode
        if self.cheatmode == False:
            self.controller.turn()[1].walldel=False

    #Checks if the first part of a wall can placed
    def checkWall1(self):
        p = _mapTools.mousePos()
        self.initChoices = ([0,1],[0,-1],[1,0],[-1,0])
        if self.grid[p[1]][p[0]]==0 and self.movingWall==None:
            for m in self.initChoices:
                newp = _array(p)+ _array(m)
                if self.grid[newp[1]][newp[0]]==0:
                    self.movingWall = [p]

    #Checks if the second part of a wall can be placed
    def checkWall2(self):
        newp = _mapTools.mousePos()
        correct = False
        if self.movingWall!=None:
            p = self.movingWall[0]
            if newp==p:
                self.movingWall=None
            else:
                moveChoices = [list(_array(p)+_array(m)) for m in self.initChoices
                                if self.grid[(_array(p)+_array(m))[1]][(_array(p)+_array(m))[0]]==0]
                if newp in moveChoices:
                    self.movingWall.append(newp)
                    correct = True
                return correct

    #Main wall moving function. Allows one wall deletion and one wall placement per turn
    def moveWall(self):
        if self.controller.dice=='Wall' and _mapTools.mousePos()[0]<33 and _mapTools.mousePos()[1]<33 and self.controller.turn()[1].moveReady==True:
            if self.grid[_mapTools.mousePos()[1]][_mapTools.mousePos()[0]]==2 and self.controller.turn()[1].walldel==True:
                self.movingWall = None
                self.delWall()
            else:
                if self.movingWall==None:
                    self.checkWall1()
                elif len(self.movingWall)==1:
                    correct = self.checkWall2()
                    if self.movingWall!=None:
                        if correct == True:
                            self.move(self.movingWall)
                            self.movingWall=None
                            if self.cheatmode == False:
                                self.controller.turn()[1].moveReady=False

    #Draws a magenta square to show where first wall part has been placed
    def drawMovingWall(self):
        if self.movingWall!=None:
            if len(self.movingWall)==1:
                _mapTools.drawSquare(self.movingWall[0],_mapTools.magenta)
