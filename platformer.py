from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, Vec3, CollisionBox, CollisionTraverser, CollisionHandlerQueue, CollisionNode, BitMask32
from light_setup import setup_point_light

configVars = """
win-size 1280 720
show-frame-rate-meter 1
"""

loadPrcFileData("", configVars)

key_map = {
    "left": False,
    "right": False,
}


def update_key_map(control_name, state):
    key_map[control_name] = state
    print(state)


class Platformer(ShowBase):
    def __init__(self):
        super().__init__()
        self.set_background_color(0, 0, 0, 1)
        self.cam.setPos(0, -65, 15)

        self.player = self.loader.loadModel("egg-models/player")
        self.player.find(
            "**/Player").node().setIntoCollideMask(BitMask32.bit(2))
        self.player.reparentTo(self.render)

        self.floor = self.loader.loadModel("egg-models/floor.egg")
        self.floor.reparentTo(self.render)

        setup_point_light(self.render, (15, 0, 20))

        self.accept("arrow_left", update_key_map, ["left", True])
        self.accept("arrow_left-up", update_key_map, ["left", False])
        self.accept("arrow_right", update_key_map, ["right", True])
        self.accept("arrow_right-up", update_key_map, ["right", False])
        self.accept("arrow_up", self.jump)

        self.taskMgr.add(self.update, "update")

        self.position = Vec3(0, 0, 15)
        self.velocity = Vec3(0, 0, 0)
        self.acceleration = Vec3(0, 0, 0)

        self.SPEED = 4
        self.GRAVITY = -0.05
        self.JUMP_FORCE = 1.2
        self.FRICTION = -0.12

        self.cTrav = CollisionTraverser()
        self.queue = CollisionHandlerQueue()
        collider_node = CollisionNode("box-coll")
        coll_box = CollisionBox((-1, -1, 0), (1, 1, 4))
        collider_node.setFromCollideMask(BitMask32.bit(1))
        collider_node.addSolid(coll_box)
        collider = self.player.attachNewNode(collider_node)
        self.cTrav.addCollider(collider, self.queue)

        self.is_jumping = False
        self.is_on_floor = True
        self.jump_count = 0

    def jump(self):
        if self.is_on_floor:
            self.is_jumping = True
            self.is_on_floor = False
            self.velocity.z = self.JUMP_FORCE
            self.jump_count += 1
            if self.jump_count == 2:
                self.is_jumping = False
                self.is_on_floor = True
                self.jump_count = 0

    def update(self, task):
        dt = globalClock.getDt()

        self.acceleration = Vec3(0, 0, self.GRAVITY)

        if key_map["right"]:
            self.acceleration.x = self.SPEED * dt
        if key_map["left"]:
            self.acceleration.x = -self.SPEED * dt

        self.acceleration.x += self.velocity.x * self.FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + (self.acceleration * 0.5)

        for entry in self.queue.getEntries():
            inp = entry.getIntoNodePath().getPos(self.render)

            if self.velocity.z < 0:
                if not self.is_jumping:
                    self.position.z = inp.z
                    self.velocity.z = 0
                    self.is_on_floor = True
                else:
                    self.is_jumping = False

        if self.position.z <= -10:
            self.position.z = 30
            self.position.x = 0
            self.velocity = Vec3(0, 0, 0)

        self.player.setPos(self.position)

        return task.cont


game = Platformer()
game.run()
