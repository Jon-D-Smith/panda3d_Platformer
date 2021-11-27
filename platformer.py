from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData

configVars = """
win-size 1280 720
show-frame-rate-meter 1
"""

loadPrcFileData("", configVars)

class Platformer(ShowBase):
    def __init__(self):
        super().__init__()
        self.set_background_color(0,0,0,1)

        self.player = self.loader.loadModel("egg-models/player")
        self.player.reparentTo(self.render)

        self.floor = self.loader.loadModel("egg-models/floor.egg")
        self.floor.reparentTo(self.render)

game = Platformer()
game.run()