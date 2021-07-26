import mapTools as _mapTools
from classes.figure import figure as _figure

class player:
    def __init__(self, colour, corner, grid, cheatmode,controller):
        startPoints = _mapTools.startpoints
        finishPoints = _mapTools.finishpoints
        self.startPos = startPoints[corner]
        self.finishPos = finishPoints[corner]
        self.figs = [_figure(colour,self.startPos[i],self.finishPos[i], grid, cheatmode, controller) for i in range(3)]
        #Status for figure selection and whether a turn is over or not
        self.figselection = None
        self.moveReady = False
        self.walldel=False

