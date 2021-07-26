from numpy import array as _array
import mapTools as _mapTools

#Minotaur class. Similar to figure
class minotaur:
    def __init__(self, grid, cheatmode, controller):
        self.initPos=(15.5,15.5)
        self.pos = self.initPos
        self.grid = grid
        self.cheatmode = cheatmode
        self.controller = controller

    #Same as figure.moveChoices, but with adjustments for minotaur
    def moveChoices(self):
        compList=[] #Complementary list which contains figures closer than dice roll
        def pathFinder(posLayer, m):
            newPosLayer=[]
            initChoices = ([0,1],[0,-1],[1,0],[-1,0])
            for p in posLayer:
                for i in initChoices:
                    newp = _array(p)+_array(i)
                    if self.grid[newp[1]][newp[0]]==0:
                        newPosLayer.append(list(newp))
                    elif self.grid[newp[1]][newp[0]]==3:
                        newPosLayer.append(list(newp))
                        compList.append(list(newp))
            m-=1
            newPosLayer= _mapTools.removeDuplicates(newPosLayer)
            if m==0:
                return newPosLayer
            else:
                return pathFinder(newPosLayer,m)
        if tuple(self.pos)==self.initPos:
            return _mapTools.removeDuplicates(pathFinder(_mapTools.minoStartpoints,7))
        else:
            return _mapTools.removeDuplicates(pathFinder([self.pos],8)+compList)

    #Same as figure.moves
    def move(self,pos):
        if tuple(self.pos)==self.initPos:
            if pos in self.moveChoices():
                self.pos=_array(pos)
                self.grid[self.pos[1]][self.pos[0]]=4
                if self.cheatmode == False:
                    self.controller.turn()[1].moveReady=False
        else:
            if pos in self.moveChoices():
                self.grid[self.pos[1]][self.pos[0]]=0
                self.pos=_array(pos)
                self.grid[self.pos[1]][self.pos[0]]=4
                if self.cheatmode == False:
                    self.controller.turn()[1].moveReady=False


    #Checks if minotaur is on top of a figure, sending them back to start
    def kill(self):
        for p in [self.controller.pb,self.controller.pr,self.controller.py,self.controller.pw]:
            for f in p.figs:
                if list(self.pos)==list(f.pos):
                    self.pos=self.initPos
                    self.grid[f.pos[1]][f.pos[0]]=0
                    f.pos=p.startPos[p.figs.index(f)]
                    self.grid[f.pos[1]][f.pos[0]]=3

