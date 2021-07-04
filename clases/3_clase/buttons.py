from matplotlib.widgets import Button

class buttonOnFigure:
    def __init__(self,fig,ani1=None,ani2=None):
        self.ani1=ani1
        self.ani2=ani2
        self.pauseAxe    = fig.add_axes((0, 0.95, 0.1, 0.05))
        self.pauseButton = Button(self.pauseAxe, 'pause')#, hovercolor = 'yellow')
        self.pauseButton.on_clicked(self.pauseFunc)
        self.pause=False
#        self.animRunning = True

    def getPauseState(self):
        return self.pause

    def pauseFunc(self,event):
        self.pause=not self.pause
       # if self.animRunning:
       #     if self.ani1:
       #         self.ani1.event_source.stop()
       #     if self.ani2:
       #         self.ani2.event_source.stop()
       #     self.animRunning=False
       # else:
       #     if self.ani1:
       #         self.ani1.event_source.start()
       #     if self.ani2:
       #         self.ani2.event_source.start()
       #     self.animRunning=True

