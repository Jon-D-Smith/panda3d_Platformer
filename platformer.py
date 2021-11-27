from direct.showbase.ShowBase import ShowBase

class Platformer(ShowBase):
    def __init__(self):
        super().__init__()
        self.set_background_color(0,0,0,1)

game = Platformer()
game.run()