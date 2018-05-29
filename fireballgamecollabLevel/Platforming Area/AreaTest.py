from direct.showbase.ShowBase import ShowBase

from panda3d.core import LVector3, LVector4
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import AmbientLight, DirectionalLight, Spotlight, PerspectiveLens

from pandac.PandaModules import TransparencyAttrib

from PrimitiveGeoms import Prism, Ramp
from PlatformSeg import PlatformSeg

import sys

class Main(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.key = {"left":0, "right": 0, "forward":0, "backward":0,
                     "cam_left": 0,"cam_right": 0, "cam_down": 0, "cam_up": 0,
                     "up":0, "down": 0}
        

        #####################
        #
        #   Simply testing procedural cave generation
        #
        #####################
        self.start = PlatformSeg(LVector3(0,0,0))
        self.start.generateAllParts(render)


        ####################
        #
        #   Setting light so that we could see the definition in the walls
        #
        ####################
        
        render.setShaderAuto()
        self.dlight = DirectionalLight('dlight')
        self.dlight.setColor(LVector4(0.3, 0.1, 0.7, 1))
        dlnp = render.attachNewNode(self.dlight)
        dlnp.setHpr(90, 20, 0)
        render.setLight(dlnp)

        self.alight = render.attachNewNode(AmbientLight("Ambient"))
        self.alight.node().setColor(LVector4(0.3, 0.3, 0.5, .1))
        render.setLight(self.alight)

        base.disableMouse()
        base.camera.setPos(0, -20, 500)
        base.camera.setP(-50)
        self.bindKeys()


    def setKey(self, key, value):
        self.key[key] = value

    def bindKeys(self):
        self.accept("escape", sys.exit);
        self.accept("a", self.setKey, ["left", True])
        self.accept("a-up", self.setKey, ["left", False])
        self.accept("d", self.setKey, ["right", True])
        self.accept("d-up", self.setKey, ["right", False])
        self.accept("w", self.setKey, ["forward", True])
        self.accept("w-up", self.setKey, ["forward", False])
        self.accept("s", self.setKey, ["backward", True])
        self.accept("s-up", self.setKey, ["backward", False])
        self.accept("space", self.setKey, ["down", True])
        self.accept("space-up", self.setKey, ["down", False])
        self.accept("shift", self.setKey, ["up", True])
        self.accept("shift-up", self.setKey, ["up", False])
        self.accept("arrow_up", self.setKey, ["cam_up", True])
        self.accept("arrow_up-up", self.setKey, ["cam_up", False])
        self.accept("arrow_down", self.setKey, ["cam_down", True])
        self.accept("arrow_down-up", self.setKey, ["cam_down", False])
        self.accept("arrow_left", self.setKey, ["cam_left", True])
        self.accept("arrow_left-up", self.setKey, ["cam_left", False])
        self.accept("arrow_right", self.setKey, ["cam_right", True])
        self.accept("arrow_right-up", self.setKey, ["cam_right", False])

        taskMgr.add(self.update, "update")

    def update(self, task):
        delta = globalClock.getDt()
        WALKSPEED = 300
        SPEED = 100
        if self.key["left"]:
            base.camera.setX(base.camera.getX() - WALKSPEED*delta) 
        if self.key["right"]:
            base.camera.setX(base.camera.getX() + WALKSPEED*delta) 
        if self.key["forward"]:
            base.camera.setY(base.camera.getY() + WALKSPEED*delta) 
        if self.key["backward"]:
            base.camera.setY(base.camera.getY() - WALKSPEED*delta)
        if self.key["up"]:
            base.camera.setZ(base.camera.getZ() + WALKSPEED*delta)
        if self.key["down"]:
            base.camera.setZ(base.camera.getZ() - WALKSPEED*delta)

        if self.key["cam_left"]:
            base.camera.setH(base.camera.getH() + SPEED*delta)
        if self.key["cam_right"]:
            base.camera.setH(base.camera.getH() - SPEED*delta)
        if self.key["cam_up"]:
            base.camera.setP(base.camera.getP() + SPEED*delta)
        if self.key["cam_down"]:
            base.camera.setP(base.camera.getP() - SPEED*delta)

        for p in self.start.iceCubes:
            p.bob()
            
            
        return task.cont
        

demo = Main()
demo.run()
