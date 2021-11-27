from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData
from light_setup import setup_point_light

configVars = """
win-size 1280 720
show-frame-rate-meter 1
"""

loadPrcFileData("", configVars)

class Platformer(ShowBase):
    def __init__(self):
        super().__init__()
        self.set_background_color(0,0,0,1)
        self.cam.setPos(0,-65,15)

        self.player = self.loader.loadModel("egg-models/player")
        self.player.reparentTo(self.render)

        self.floor = self.loader.loadModel("egg-models/floor.egg")
        self.floor.reparentTo(self.render)

        setup_point_light(self.render, (15,0,20))

game = Platformer()
game.run()