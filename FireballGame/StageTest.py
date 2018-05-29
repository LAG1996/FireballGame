from direct.showbase.ShowBase import ShowBase

from panda3d.core import LVector3, LVector4, Point3
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import PandaNode, NodePath, Camera
from panda3d.core import WindowProperties
from panda3d.core import CollisionTraverser,CollisionNode,BitMask32, NodePath
from panda3d.core import CollisionHandlerQueue, CollisionHandlerGravity, CollisionHandlerPusher
from panda3d.core import CollisionTube,CollisionSegment,CollisionRay,CollisionSphere, CollisionBox, CollisionPolygon
from direct.actor.Actor import Actor, ActorNode
from panda3d.core import Fog

from pandac.PandaModules import TransparencyAttrib

from PrimitiveGeoms import Prism, Square, Ramp
from IceCube import IceCube

from Cave import Cave
from LostWood import LostWood
from PlatformSeg import PlatformSeg
from End import End

import math
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
        self.lostWood = LostWood(LVector3(self.start.pos.x + 750, self.start.parts[0].pos.y + self.start.parts[0].wid, self.start.pos.z))
        self.lostWood.generateAllParts(render)
        self.cave = Cave(LVector3(self.lostWood.pos.x + 1100, self.lostWood.parts[6].pos.y + self.lostWood.parts[6].wid, self.lostWood.pos.z))
        self.cave.generateAllParts(render)
        self.end = End(LVector3(self.cave.thirdRoomParts[8].pos.x - 200,
                       self.cave.thirdRoomParts[8].pos.y + self.cave.thirdRoomParts[8].wid,
                       self.cave.thirdRoomParts[8].pos.z))
        self.end.generate(render)


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
        self.alight.node().setColor(LVector4(0.5, 0.5, 1, .1))
        render.setLight(self.alight)

        base.disableMouse()
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)
        base.camera.reparentTo(self.floater)
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
            self.floater.setX(self.floater.getX() - WALKSPEED*delta) 
        if self.key["right"]:
            self.floater.setX(self.floater.getX() + WALKSPEED*delta) 
        if self.key["forward"]:
            self.floater.setY(self.floater.getY() + WALKSPEED*delta) 
        if self.key["backward"]:
            self.floater.setY(self.floater.getY() - WALKSPEED*delta)
        if self.key["up"]:
            self.floater.setZ(self.floater.getZ() + WALKSPEED*delta)
        if self.key["down"]:
            self.floater.setZ(self.floater.getZ() - WALKSPEED*delta)

        if self.key["cam_left"]:
            base.camera.setH(base.camera.getH() + SPEED*delta)
        if self.key["cam_right"]:
            base.camera.setH(base.camera.getH() - SPEED*delta)
        if self.key["cam_up"]:
            base.camera.setP(base.camera.getP() + SPEED*delta)
        if self.key["cam_down"]:
            base.camera.setP(base.camera.getP() - SPEED*delta)

        ######################
        #
        # SIMPLE OCCLUSION FOR START AREA
        #
        ######################

        for p in self.start.parts:
            if p.type == 'IceCube':
                if math.fabs((math.sqrt((p.model.getX() * p.model.getX()) + (p.model.getY() * p.model.getY()))
                - math.sqrt((self.floater.getX() * self.floater.getX()) + (self.floater.getY() * self.floater.getY())))) <= 400:
                    p.show()
                    #Ice cube movement
                    p.bob(delta)
                else:
                    p.hide()
                
            if p.type == 'Prism':
                if p.type == 'Prism':
                    if math.fabs((math.sqrt((p.pos.x * p.pos.x) + (p.pos.y * p.pos.y))
                    - math.sqrt((self.floater.getX() * self.floater.getX()) + (self.floater.getY() * self.floater.getY())))) <= 1000:
                        p.show()
                    else:
                        p.hide()


        ######################
        #
        # SIMPLE OCCLUSION FOR CAVE PARTS
        #
        ######################
        for p in self.cave.parts:
            if p.type == 'Prism':
                if math.fabs((math.sqrt((p.pos.x * p.pos.x) + (p.pos.y * p.pos.y))
                - math.sqrt((self.floater.getX() * self.floater.getX()) + (self.floater.getY() * self.floater.getY())))) <= 2200:
                    p.show()
                else:
                    p.hide()
                
            if p.type == 'IceCube':
                if math.fabs((math.sqrt((p.model.getX() * p.model.getX()) + (p.model.getY() * p.model.getY()))
                - math.sqrt((self.floater.getX() * self.floater.getX()) + (self.floater.getY() * self.floater.getY())))) <= 1250:
                    p.show()

                    #Ice cube movement
                    self.cave.moveIceCubes(delta/25)
                    for p in self.cave.iceCubesThirdRoom:
                        p.bob(delta/25)
                    for p in self.cave.iceCubesSecondRoom:
                        p.bob(delta/25)
                    self.cave.bigCube.bob(delta/25)

                    for p in self.start.iceCubes:
                        p.bob(delta)
                else:
                    p.hide()

        return task.cont
        

demo = Main()
demo.run()
