from panda3d.core import PointLight, AmbientLight

def setup_point_light(render, pos):
    plight = PointLight("plight")
    plight.setColor((1,1,1,1))
    plnp = render.attachNewNode(plight)
    plnp.setPos(pos[0], pos[1], pos[2])
    render.setLight(plnp)

    alight = AmbientLight("alight")
    alight.setColor((0.4,0.4,0.4,1))
    alnp = render.attachNewNode(alight)
    render.setLight(alnp)

