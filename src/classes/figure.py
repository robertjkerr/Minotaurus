from mapTools import removeDuplicates as _removeDuplicates
from numpy import array as _array

class figure:
    def __init__(self,colour,pos,fps,grid,cheatmode,controller):
        self.colour = colour
        self.pos = _array(pos)
        self.play = True
        self.finishPoints=fps
        self.cheatmode = cheatmode
        self.grid = grid
        self.controller = controller
        #Sets figure's grid position to 3
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
                        newp = _array(p)+_array(i)
                        if self.grid[newp[1]][newp[0]]==0:
                            newPosLayer.append(list(newp))
                        elif self.grid[newp[1]][newp[0]]==5:
                            newPosLayer.append(list(newp))
                            compList.append(list(newp))
                m-=1
                if m==0:
                    return newPosLayer
                else:
                    return pathFinder(newPosLayer,m)
            else:
                return []
        return _removeDuplicates(pathFinder([self.pos],roll)+compList)

    #Checks if selected position is a valid move choice and then moves figure
    def move(self,pos,roll):
        if pos in self.moveChoices(roll):
            self.grid[self.pos[1]][self.pos[0]]=0
            self.pos=_array(pos)
            self.grid[self.pos[1]][self.pos[0]]=3
            if self.cheatmode == False:
                self.controller.turn()[1].moveReady=False

