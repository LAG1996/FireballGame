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

from pandac.PandaModules import TransparencyAttrib

from PrimitiveGeoms import Prism, Square, Ramp
from IceCube import *

from Cave import Cave
from LostWood import LostWood
from PlatformSeg import PlatformSeg
from End import End

import sys
import math
import random

from pandac.PandaModules import *
from direct.gui.OnscreenImage import OnscreenImage


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        #Background sound (does not play infinitely)
        self.backgroundSound = base.loader.loadSfx("sounds/DireDireDocks.mp3")

        taskMgr.add(self.update, "moveTask")
        
        #Disable the mouse so that we may use it for our control scheme.
        self.props = WindowProperties()
        self.props.setSize(1920, 1080)
        self.props.setFullscreen(True)
        self.props.setCursorHidden(True)
        base.win.requestProperties(self.props)
        base.disableMouse()
        
        self.buildKeyMap()
        self.inMenu = True
        self.menuScreen = OnscreenImage("titlescreen.png", (0, .01, 0))
        self.menu()

    def initialize(self):
        self.timer = 0
        base.enableParticles()
        #base.setFrameRateMeter(True)

        ##########
        #
        # SETUP COLLISION HANDLERS AND FLAMIE'S MODEL
        #
        ##########
        
        #Create the collision handlers in order to build the level.
        WALL_MASK = BitMask32.bit(2)
        FLOOR_MASK = BitMask32.bit(1)
        
        #Start up the collision system
        self.cTrav = CollisionTraverser()

        #Determine how collisions with walls will be handled
        self.wallHandler = CollisionHandlerPusher()
        self.bobbing = False

        #Setup flamie's model
        self.flamieNP = base.render.attachNewNode(ActorNode('flamieNP'))
        self.flamieNP.reparentTo(base.render)
        self.flamie = loader.loadModel('models/Flame/body')
        self.flamie.setScale(.5)
        self.flamie.setTransparency(TransparencyAttrib.MAlpha)
        self.flamie.setAlphaScale(0)
        self.flamie.reparentTo(self.flamieNP)
        self.flamie.setCollideMask(BitMask32.allOff())
        flameLight = DirectionalLight("flameLight")
        fl = self.flamie.attachNewNode(flameLight)
        fl.setColor(255, 255, 255, 1)
        flameLight.setDirection((-5, -5, -5))
        self.flamie.setLight(fl)


        self.flamie2 = loader.loadModel("models/p.obj")
        self.flamie2.setTexture(loader.loadTexture("models/flamie2D/f7.png"))
        self.flamie2.reparentTo(self.flamieNP)
        self.flamie2.setScale(4)
        self.flamie2OriZ = 2
        self.flamie2.setPos(-6.5, 0, self.flamie2OriZ) #(length, depth, height)
        self.flamie2.setLight(fl)
        self.flamie2.setTransparency(TransparencyAttrib.MAlpha)
        self.flamieFire = PointLight('fire')
        self.flamieFire.setColor(VBase4(1,1,1,1))
        self.flamieFire.setAttenuation((1,0,1))
        plnp = render.attachNewNode(self.flamieFire)
        plnp.setPos(self.flamieNP.getPos())
        self.flamielight = AmbientLight('light')
        self.flamielight.setColor(VBase4(1, 0.5, 0.6, 1))

        self.flamielight = self.flamie2.attachNewNode(self.flamielight)
        self.flamie2.setLight(self.flamielight)
        self.flamie2.setLight(plnp)
        self.mayFlamieBob = True

        #self.flamie2.setAlphaScale(0.5)

        '''self.tree = loader.loadModel("models/p2.obj")
        self.tree.setTexture(loader.loadTexture("deadTree.png"))
        self.tree.reparentTo(render)
        self.tree.setScale(4)
        self.tree.setPos(25,25,0) #(length, depth, height)
        self.tree.setLight(fl)
        self.tree.setTransparency(TransparencyAttrib.MAlpha)
        self.treelight = AmbientLight('light')
        self.treelight.setColor(VBase4(0.9, 0.9, 0.6, 1))
        self.treelight = self.tree.attachNewNode(self.treelight)
        self.tree.setLight(self.treelight)'''

        x = 150
        y = 20
        offset1 = 0
        treeList2 = [loader.loadModel("models/p2.obj") for i in range(7)]
        for j in treeList2:
            k = random.randint(1, 100)
            if k%5 is 1 or k%5 is 2:
                j.setTexture(loader.loadTexture("deadTree.png"))
            else:
                j.setTexture(loader.loadTexture("tree.png"))
            j.reparentTo(render)
            j.setScale(random.randint(4,7))
            j.setTransparency(TransparencyAttrib.MAlpha)
            j.setPos(x + 3*offset1, y + 4*offset1, 0)
            treelight = AmbientLight('light')
            treelight = j.attachNewNode(treelight)
            j.setLight(treelight)
            offset1 = offset1 + random.randint(4, 10)

        x = 4
        y = 90
        offset1 = 0
        treeList2 = [loader.loadModel("models/p2.obj") for i in range(6)]
        for j in treeList2:
            k = random.randint(1, 100)
            if k%5 is 1 or k%5 is 2:
                j.setTexture(loader.loadTexture("deadTree.png"))
            else:
                j.setTexture(loader.loadTexture("tree.png"))
            j.reparentTo(render)
            j.setScale(random.randint(4,7))
            j.setTransparency(TransparencyAttrib.MAlpha)
            j.setPos(x + 3*offset1, y + 4*offset1, 0)
            treelight = AmbientLight('light')
            treelight = j.attachNewNode(treelight)
            j.setLight(treelight)
            offset1 = offset1 + random.randint(4, 10)

        x = 3
        y = 120
        offset1 = 0
        treeList2 = [loader.loadModel("models/p2.obj") for i in range(4)]
        for j in treeList2:
            k = random.randint(1, 100)
            if k%5 is 1 or k%5 is 2:
                j.setTexture(loader.loadTexture("deadTree.png"))
            else:
                j.setTexture(loader.loadTexture("tree.png"))
            j.reparentTo(render)
            j.setScale(random.randint(4,7))
            j.setTransparency(TransparencyAttrib.MAlpha)
            j.setPos(x + 3*offset1, y + 4*offset1, 0)
            treelight = AmbientLight('light')
            treelight = j.attachNewNode(treelight)
            j.setLight(treelight)
            offset1 = offset1 + random.randint(4, 10)

        x = 200
        y = 20
        offset1 = 0
        treeList2 = [loader.loadModel("models/p2.obj") for i in range(4)]
        for j in treeList2:
            k = random.randint(1, 100)
            if k%5 is 1 or k%5 is 2:
                j.setTexture(loader.loadTexture("deadTree.png"))
            else:
                j.setTexture(loader.loadTexture("tree.png"))
            j.reparentTo(render)
            j.setScale(random.randint(4,7))
            j.setTransparency(TransparencyAttrib.MAlpha)
            j.setPos(x + 3*offset1, y + 4*offset1, 0)
            treelight = AmbientLight('light')
            treelight = j.attachNewNode(treelight)
            j.setLight(treelight)
            offset1 = offset1 + random.randint(4, 10)

        ### Something that should look like water ###
        w = loader.loadModel("models/flatP.obj")
        w.setTexture(loader.loadTexture("ice.png"))
        w.reparentTo(render)
        w.setScale(75)
        w.setTransparency(TransparencyAttrib.MAlpha)
        w.setAlphaScale(.7)
        w.setLight(treelight)
        w.setPos(-200, 0, -10)

        self.waterOrigiZ = -10
        self.waterSecZ = -95
        self.waterThirdZ = -120
        self.water = w

        ### Reskying the sky ###
        w = loader.loadModel("models/biggerFlatP.obj")
        w.setTexture(loader.loadTexture("models/n2.jpg"))
        w.reparentTo(self.flamie2)
        w.setScale(15)
        w.setLight(treelight)
        w.setPos(-200, 450, -200) #(length, depth, height)

        #Give flamie gravity
        self.floorHandler = CollisionHandlerGravity()
        self.floorHandler.setGravity(9.81+100)
        self.floorHandler.setMaxVelocity(100)
        

        ##########
        #
        # GENERATING LEVEL PARTS
        #
        ##########
        self.ice_reset = ()
        self.start = PlatformSeg(LVector3(0,0,0))
        self.start.generateAllParts(render)
        self.checkpointCreator(70, 90, self.start.pos.z, 10)
        self.floater = False
        
        for p in self.start.parts:
            if isinstance(p, Prism):
                self.collisionBoxCreator(p.pos.x, p.pos.y, p.pos.z, p.len, p.wid, p.dep, 'terraincollision', 'wallcollision')
            if isinstance(p, Square):
                self.collisionBoxCreator(p.pos.x, p.pos.y, p.pos.z, p.len, p.wid, 3,  'terraincollision', 'wallcollision')
            if isinstance(p, IceCube):
                p.model.setCollideMask(BitMask32.allOff())
                self.ice_reset += (p,)
                iceCubefloor= p.model.find("**/iceFloor")
                iceCubewall = p.model.find("**/iceWall")
                iceCubefloor.node().setIntoCollideMask(FLOOR_MASK)
                iceCubewall.node().setIntoCollideMask(WALL_MASK)

        
        self.lostWood = LostWood(LVector3(self.start.pos.x + 750, self.start.parts[0].pos.y + self.start.parts[0].wid, self.start.pos.z))
        self.lostWood.generateAllParts(render)
        self.checkpointCreator(self.lostWood.pos.x+120, self.lostWood.pos.y+150, self.lostWood.pos.z,20)
        self.checkpointCreator(self.lostWood.parts[6].pos.x + self.lostWood.parts[6].len/2, self.lostWood.parts[6].pos.y + self.lostWood.parts[6].wid/2, self.lostWood.pos.z, 40)
        
        for p in self.lostWood.parts:
            if isinstance(p, Prism):
                self.collisionBoxCreator(p.pos.x, p.pos.y, p.pos.z, p.len, p.wid, p.dep, 'terraincollision', 'wallcollision')
            if isinstance(p, Square):
                self.collisionBoxCreator(p.pos.x, p.pos.y, p.pos.z, p.len, p.wid, 3,  'terraincollision', 'wallcollision')
            if isinstance(p, IceCube):
                p.model.setCollideMask(BitMask32.allOff())
                self.ice_reset += (p,)
                iceCubefloor= p.model.find("**/iceFloor")
                iceCubewall = p.model.find("**/iceWall")
                iceCubefloor.node().setIntoCollideMask(FLOOR_MASK)
                iceCubewall.node().setIntoCollideMask(WALL_MASK)
            
        self.cave = Cave(LVector3(self.lostWood.pos.x + 1100, self.lostWood.pos.y + 2000, self.lostWood.pos.z - 50))
        self.cave.generateAllParts(render)
        self.checkpointCreator(self.cave.thirdRoomParts[5].pos.x + self.cave.thirdRoomParts[5].len/2,
                               self.cave.thirdRoomParts[5].pos.y + self.cave.thirdRoomParts[5].wid/2,
                               self.cave.thirdRoomParts[5].pos.z, 30)
        
        for p in self.cave.parts:
            if isinstance(p, Prism):
                self.collisionBoxCreator(p.pos.x, p.pos.y, p.pos.z, p.len, p.wid, p.dep, 'terraincollision', 'wallcollision')
            if isinstance(p, Square):
                self.collisionBoxCreator(p.pos.x, p.pos.y, p.pos.z, p.len, p.wid, 3,  'terraincollision', 'wallcollision')
            if isinstance(p, IceCube):
                p.model.setCollideMask(BitMask32.allOff())
                self.ice_reset += (p,)
                iceCubefloor= p.model.find("**/iceFloor")
                iceCubewall = p.model.find("**/iceWall")
                iceCubefloor.node().setIntoCollideMask(FLOOR_MASK)
                iceCubewall.node().setIntoCollideMask(WALL_MASK)

        self.end = End(LVector3(self.cave.thirdRoomParts[8].pos.x - 200,
                       self.cave.thirdRoomParts[8].pos.y + self.cave.thirdRoomParts[8].wid,
                       self.cave.thirdRoomParts[8].pos.z))
        self.end.generate(render)
        self.collisionBoxCreator(self.end.floor.pos.x, self.end.floor.pos.y, self.end.floor.pos.z,
                                 self.end.floor.len, self.end.floor.wid, self.end.floor.dep,
                                 'terraincollision', 'wallcollision')
        #########
        # DRAWING THE CABIN AND FINAL CAMPFIRE
        #########
        self.checkpointCreator(self.end.floor.pos.x + self.end.floor.len/2,
                               self.end.floor.pos.y + self.end.floor.wid/2,
                               self.end.floor.pos.z, 30)
        self.cabin = loader.loadModel("models/p2.obj")
        self.cabin.setTexture(loader.loadTexture("models/cabin.png"))
        self.cabin.setScale(50)
        self.cabin.reparentTo(render)
        self.cabin.setPos(self.end.floor.pos.x + self.end.floor.len/2,
                          self.end.floor.pos.y + self.end.floor.wid/1.1,
                          self.end.floor.pos.z)
        self.cabin.setTransparency(TransparencyAttrib.MAlpha)
        

        #Manually creating starting position. Copy and paste the first three parameters of the checkpoint you want to start at.
        self.startPos = LVector3(70, 90, self.start.pos.z)
        self.flamieNP.setPos(self.startPos)


        '''#Testing the tree model
        self.tree = loader.loadModel('models/Tree/log')
        self.tree.reparentTo(render)
        self.tree.setPos(-50,0,100)
        self.tree.setScale(2)'''

        '''#Add sky background
        self.sky = loader.loadModel('models/sphere.obj')
        self.sky.reparentTo(self.camera)
        self.sky.set_two_sided(True)
        self.skyTexture = loader.loadTexture("models/n2.jpg")
        self.sky.setTexture(self.skyTexture)
        self.sky.set_bin('background', 0)
        self.sky.set_depth_write(False)
        self.sky.set_compass()'''

        ##########
        #
        # CREATE FLAMIE'S COLLISION GEOMETRY
        #
        ##########
        
        #Give flamie a collision sphere in order to collide with walls
        flamieCollider = self.flamie.attachNewNode(CollisionNode('flamiecnode'))
        flamieCollider.node().addSolid(CollisionSphere(0,0,0,5))
        flamieCollider.node().setFromCollideMask(WALL_MASK)
        flamieCollider.node().setIntoCollideMask(BitMask32.allOff())
        self.wallHandler.addCollider(flamieCollider, self.flamieNP)
        self.cTrav.addCollider(flamieCollider, self.wallHandler)

        #Give flamie a collision ray to collide with the floor
        flamieRay = self.flamie.attachNewNode(CollisionNode('flamieRay'))
        flamieRay.node().addSolid(CollisionRay(0,0,8,0,0,-1))
        flamieRay.node().setFromCollideMask(FLOOR_MASK)
        flamieRay.node().setIntoCollideMask(BitMask32.allOff())
        self.floorHandler.addCollider(flamieRay, self.flamieNP)
        self.cTrav.addCollider(flamieRay, self.floorHandler)

        #Add a sensor that lets us melt ice cubes without standing on the cube.
        meltSensor = self.flamie.attachNewNode(CollisionNode('meltSensor'))
        cs = CollisionSphere(-2,0,10, 50)
        meltSensor.node().addSolid(cs)
        meltSensor.node().setFromCollideMask(WALL_MASK)
        meltSensor.node().setIntoCollideMask(BitMask32.allOff())
        cs.setTangible(0)
        self.wallHandler.addCollider(meltSensor, self.flamieNP)
        self.cTrav.addCollider(meltSensor, self.wallHandler)
        self.wallHandler.addInPattern('%fn-into-%in')
        self.wallHandler.addAgainPattern('%fn-again-%in')
        self.accept('meltSensor-into-iceWall', self.melt)
        self.accept('meltSensor-again-iceWall', self.melt)
        self.accept('meltSensor-into-checkpointCol', self.newstart)
        
        #Add in an event handle to prevent the jumping glitch found on the bobbing ice cubes.
        self.floorHandler.addInPattern('%fn-into-%in')
        self.floorHandler.addAgainPattern('%fn-again-%in')
        self.floorHandler.addOutPattern('%fn-out-%in')
        self.accept('flamieRay-into-iceFloor', self.jittercancel)
        self.accept('flamieRay-again-iceFloor', self.jittercancel)
        self.accept('flamieRay-out-iceFloor', self.jittercanceloff)

        
        #Uncomment these lines to see flamie's collision geometry
        #flamieCollider.show()
        #flamieRay.show()
        #meltSensor.show()

        #Uncomment this line to see the actual collisions.
        #self.cTrav.showCollisions(render)
        
        #This plane is found at the very bottom of the level and adds global gravity.
        killfloor = CollisionPlane(Plane(Vec3(0,0,1), Point3(0,0,-1000)))
        killfloorCol = CollisionNode('kfcollision')
        killfloorCol.addSolid(killfloor)
        killfloorCol.setIntoCollideMask(BitMask32.bit(1))
        killfloorColNp = self.render.attachNewNode(killfloorCol)

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

        self.snow = loader.loadTexture("models/ground.jpg")

        #Create a floater object and have it float 2 units above fireball.
        #And use this as a target for the camera to focus on.
        #This idea is taken from the roaming ralph sample that came with the
        #Panda3D SDK.
        self.camFocus = NodePath(PandaNode("floater"))
        self.camFocus.reparentTo(render)
        self.camFocusCurrZ = self.flamie.getZ() + 10

        #The camera is locked to the avatar so it always follows regardless of movement.
        self.camera.reparentTo(render)
        self.cameraTargetHeight = 8.0
        self.cameraDistance = 100
        self.cameraHeightModes = (self.start.parts[0].pos.z + 45, self.start.parts[0].pos.z + 125, self.camFocus.getZ() + 10, self.camFocus.getZ() + 150,
                                  self.end.floor.pos.z + 10)
        self.cameraHeight = self.cameraHeightModes[0]

        
    #################
    #   Changes Camera orientation depending on where the player is in the stage to compensate for the fact that
    #   the player has no direct control of the camera.
    #   Checks using the arrays from the level parts.
    ##################
    def cameraModes(self, delta):
        #Is the fireball within the platforming section between the starting area and the lost woods?
        #Is the fireball near the simple platforming sections of the LostWoods?
        #Is the fireball near the drop off point into the cave?
        #Is the fireball near the entrance to the second room in the cave?
        #If yes to any of these, bring the camera up to give a bird's eye view of the platforming
        if ((self.flamieNP.getX() > self.start.parts[1].pos.x and self.flamieNP.getY() > self.start.parts[1].pos.y - self.start.parts[1].wid
            and self.flamieNP.getX() < self.lostWood.parts[0].pos.x)
            or (self.flamieNP.getX() > self.lostWood.parts[0].pos.x + self.lostWood.parts[0].len/1.1
                and self.flamieNP.getX() < self.lostWood.parts[2].pos.x + self.lostWood.parts[0].len/11
                and self.flamieNP.getY() < self.lostWood.parts[0].pos.y + self.lostWood.parts[0].wid)
            or (self.flamieNP.getY() > self.cave.parts[0].pos.y - 20 and self.flamieNP.getY() <= self.cave.parts[0].pos.y + self.cave.parts[0].wid/2)
            or (self.flamieNP.getX() < self.cave.parts[1].pos.x + self.cave.parts[1].wid/10 and self.flamieNP.getY() >= self.cave.parts[1].pos.x)):
                camMode = 1
        #Is the fireball in the beginning of the cave area?
        #If yes, bring the camera closer
        elif self.flamieNP.getY() > self.cave.parts[1].pos.y - self.cave.parts[0].wid/2 and self.flamieNP.getY() < self.cave.thirdRoomParts[5].pos.y:
            camMode = 2
        else:
            camMode = 0

        if self.flamieNP.getY() >= self.cave.thirdRoomParts[6].pos.y:
            self.cave.thirdRoomParts[0].hide()
            camMode = 3
        if self.flamieNP.getY() >= self.cave.thirdRoomParts[8].pos.y + self.cave.thirdRoomParts[8].wid/1.5:
            camMode = 4

        self.lerpCam(camMode, delta)

    def lerpCam(self, camMode, delta):
        CAMLERPSPEED = 25
        if camMode == 0:
            if not self.cameraHeight == self.cameraHeightModes[camMode]:
                if self.cameraHeight - CAMLERPSPEED * delta <= self.cameraHeightModes[camMode]:
                    self.cameraHeight = self.cameraHeightModes[camMode]
                else:
                    self.cameraHeight = self.cameraHeight - CAMLERPSPEED * delta
        elif camMode == 1:
            if not self.cameraHeight == self.cameraHeightModes[camMode]:
                if self.cameraHeight - CAMLERPSPEED * delta >= self.cameraHeightModes[camMode]:
                    self.cameraHeight = self.cameraHeightModes[camMode]
                else:
                    if self.cameraHeight < self.cameraHeightModes[camMode]:
                        self.cameraHeight = self.cameraHeight + CAMLERPSPEED * delta
                    else:
                        self.cameraHeight = self.cameraHeight - CAMLERPSPEED * delta
        elif camMode == 2:
            if not self.cameraHeight == self.cameraHeightModes[camMode]:
                if self.cameraHeight - CAMLERPSPEED * delta <= self.cameraHeightModes[camMode]:
                    self.cameraHeight = self.cameraHeightModes[camMode]
                    self.camFocusCurrZ = self.flamieNP.getZ() + 10
                else:
                    self.cameraHeight = self.cameraHeight - CAMLERPSPEED * delta
                    self.camFocusCurrZ = self.flamieNP.getZ() + 10
        elif camMode == 3:
            if not self.cameraHeight == self.cameraHeightModes[camMode]:
                if self.cameraHeight + CAMLERPSPEED * 3 * delta >= self.cameraHeightModes[camMode]:
                    self.cameraHeight = self.cameraHeightModes[camMode]
                else:
                    self.cameraHeight = self.cameraHeight + CAMLERPSPEED * 3 * delta
        elif camMode == 4:
            if not self.cameraHeight == self.cameraHeightModes[camMode]:
                if self.cameraHeight - CAMLERPSPEED * 3 * delta <= self.cameraHeightModes[camMode]:
                    self.cameraHeight = self.cameraHeightModes[camMode]
                else:
                    self.cameraHeight = self.cameraHeight - CAMLERPSPEED * 3 * delta

    def waterControl(self, delta):
        WATERLERPSPEED = .75
        if self.flamieNP.getY() <= self.lostWood.parts[6].pos.y + self.lostWood.parts[6].wid/2:
            if not self.water.getZ() == self.waterOrigiZ:
                if self.water.getZ() - WATERLERPSPEED * delta < self.waterOrigiZ and self.water.getZ() > self.waterOrigiZ:
                    self.water.setZ(self.waterOrigiZ)
                elif self.water.getZ() + WATERLERPSPEED * delta > self.waterOrigiZ and self.water.getZ() < self.waterOrigiZ:
                    self.water.setZ(self.waterOrigiZ)
                else:
                    if self.water.getZ() > self.waterOrigiZ:
                        self.water.setZ(self.water, - WATERLERPSPEED * delta)
                        if self.water.getZ() < self.waterOrigiZ:
                            self.water.setZ(self.waterOrigiZ)
                    else:
                        self.water.setZ(self.water, + WATERLERPSPEED * delta)
                        if self.water.getZ() > self.waterOrigiZ:
                            self.water.setZ(self.waterOrigiZ)
        elif self.flamieNP.getY() <= self.cave.parts[1].pos.y:
            if not self.water.getZ() == self.waterSecZ:
                if self.water.getZ() - WATERLERPSPEED * delta < self.waterSecZ:
                    self.water.setZ(self.waterSecZ)
                else:
                    self.water.setZ(self.water, - WATERLERPSPEED * delta)
        else:
            if not self.water.getZ() == self.waterThirdZ:
                if self.water.getZ() - WATERLERPSPEED * delta < self.waterThirdZ:
                    self.water.setZ(self.waterThirdZ)
                else:
                    self.water.setZ(self.water, - WATERLERPSPEED * delta)
        
        
    def reset(self):
        self.flamieNP.setPos(self.startPos)
        self.camFocusCurrZ = self.flamieNP.getZ() + 10
        for p in self.ice_reset:
            p.model.setScale(p.original_scale)
        
    def jump(self, dt):
        if self.bobbing:
            if self.floorHandler.getAirborneHeight() < 0.15:
                self.floorHandler.addVelocity(60) 
        elif self.floorHandler.isOnGround():
            self.floorHandler.addVelocity(60)

    def jittercancel(self, collEntry):
        model = collEntry.getIntoNodePath().getParent()
        modelRef = model.getPythonTag("iceRef")
        if model.getScale()[0] > 1.2:
            model.setScale(model.getScale()- modelRef.meltspeed)

        self.bobbing = True

    def jittercanceloff(self, collEntry):
        self.bobbing = False

    def melt(self, collEntry):
        model = collEntry.getIntoNodePath().getParent()
        modelRef = model.getPythonTag("iceRef")
        if model.getScale()[0] > 1.2 and self.bobbing != True:
            model.setScale(model.getScale()- modelRef.meltspeed)

    def newstart(self, collEntry):
        entry = collEntry.getInto().getCenter()
        self.startPos = (entry[0]+10, entry[1]+10, entry[2] +10)
        cp = loader.loadModel('models/Campfire/fire')
        cp.setPos(entry[0],entry[1], entry[2])
        cp.reparentTo(render)
            
    def buildKeyMap(self):
        self.keyMap = {"left": 0, "right": 0, "forward": 0, "back": 0, "down": 0, "up": 0, "lookUp": 0, "lookDown": 0, "lookLeft": 0, "lookRight": 0}

        #I changed the control scheme let me know if you would like me to try something else.
        #WASD for movement, space for jump
        self.accept("escape", sys.exit)
        self.accept("a", self.setKey, ["left", True])
        self.accept("a-up", self.setKey, ["left", False])
        self.accept("d", self.setKey, ["right", True])
        self.accept("d-up", self.setKey, ["right", False])
        self.accept("w", self.setKey, ["forward", True])
        self.accept("w-up", self.setKey, ["forward", False])
        self.accept("s", self.setKey, ["back", True])
        self.accept("s-up", self.setKey, ["back", False])
        self.accept("space", self.setKey, ["down", True])
        self.accept("space-up", self.setKey, ["down", False])
        self.accept("shift", self.setKey, ["up", True])
        self.accept("shift-up", self.setKey, ["up", False])

    def setKey(self, key, value):
        self.keyMap[key] = value

    def update(self, task):
        delta = globalClock.getDt()
        if not self.inMenu:
            SPEED = 125
            #Variable that holds what direction the player is inputting
            fblr = 0
            self.timer += delta * 25

            self.killPlane = self.water.getZ() - 25
            if self.flamieNP.getZ() < self.killPlane:
                self.reset()
                
            if self.keyMap["left"]:
                fblr = 1
                old_fblr = fblr
                self.flamieNP.setX(self.flamie, - SPEED * delta)
            if self.keyMap["right"]:
                fblr = 2
                old_fblr = fblr
                self.flamieNP.setX(self.flamie, + SPEED * delta)
            if self.keyMap["forward"]:
                fblr = 3
                old_fblr = fblr
                self.flamieNP.setY(self.flamie, + SPEED * delta)
            if self.keyMap["back"]:
                fblr = 4
                old_fblr = fblr
                self.flamieNP.setY(self.flamie, - SPEED * delta)
            if self.keyMap["up"]:
                #self.flamieNP.setZ(self.flamie, - SPEED * dt)
                self.reset()
                #self.cameraDistance = 20+self.cameraDistance
            if self.keyMap["down"] and self.timer > 1:
                #self.flamieNP.setZ(self.flamie, + SPEED * dt)
                self.timer = 0
                self.jump(delta)
                
            if fblr == 1:
                self.flamie2.setTexture(loader.loadTexture("models/flamie2D/f8.png"))
            elif fblr == 2:
                self.flamie2.setTexture(loader.loadTexture("models/flamie2D/f6.png"))
            elif fblr == 3:
                if old_fblr == 1:
                    self.flamie2.setTexture(loader.loadTexture("models/flamie2D/f1.png"))
                elif old_fblr == 2:
                    self.flamie2.setTexture(loader.loadTexture("models/flamie2D/f4.png"))
                else:
                    self.flamie2.setTexture(loader.loadTexture("models/flamie2D/f3.png"))
            else:
                self.flamie2.setTexture(loader.loadTexture("models/flamie2D/f7.png"))

            if self.floorHandler.isOnGround:
                self.flamieBob(delta)

            #The camera control is borrowed from Kristina's Tech Demo
            #This is also a demo found at: http://www.panda3d.org/forums/viewtopic.php?t=8452

            '''# mouse-controlled camera begins

            # Use mouse input to turn both the Character and the Camera
            if base.mouseWatcherNode.hasMouse():
                md = base.win.getPointer(0)
                x = md.getX()
                y = md.getY()
                deltaX = md.getX() - 200
                deltaY = md.getY() - 200
                # reset mouse cursor position
                base.win.movePointer(0, 200, 200)
                # alter flamie's yaw by an amount proportionate to deltaX
                self.flamie.setH(self.flamie.getH() - 0.3* deltaX)
                # find the new camera pitch and clamp it to a reasonable range
                self.cameraPitch = self.cameraPitch + 0.1 * deltaY
                if (self.cameraPitch < -60): self.cameraPitch = -60
                if (self.cameraPitch >  80): self.cameraPitch =  80
                base.camera.setHpr(0,self.cameraPitch,0)
                # set the camera at around ralph's middle
                # We should pivot around here instead of the view target which is noticebly higher
                base.camera.setPos(0,0,self.cameraTargetHeight/2)
                # back the camera out to its proper distance
                base.camera.setY(base.camera,self.cameraDistance)

            # point the camera at the view target
            viewTarget = Point3(0,0,self.cameraTargetHeight)
            base.camera.lookAt(viewTarget)
            # reposition the end of the  camera's obstruction ray trace
            #self.cameraRay.setPointB(base.camera.getPos())

            # mouse-controlled camera ends'''

            self.waterControl(delta)
            self.water.setX(self.flamieNP.getX() - 250)
            self.water.setY(self.flamieNP.getY() - 250)
            self.cameraModes(delta)
            base.camera.setPos(self.flamieNP.getX(), self.flamieNP.getY() - self.cameraDistance, self.cameraHeight)
            self.camFocus.setPos(self.flamieNP.getX(), self.flamieNP.getY(), self.camFocusCurrZ)
            base.camera.lookAt(self.camFocus)


            '''
            ######################
            #
            # SIMPLE OCCLUSION FOR START AREA
            #
            ######################

            for p in self.start.parts:
                if p.type == 'IceCube':
                    if math.fabs((math.sqrt((p.model.getX() * p.model.getX()) + (p.model.getY() * p.model.getY()))
                    - math.sqrt((self.camFocus.getX() * self.camFocus.getX()) + (self.camFocus.getY() * self.camFocus.getY())))) <= 400:
                        p.show()
                        #Ice cube movement
                        p.bob(delta)
                    else:
                        p.hide()
                    
                if p.type == 'Prism':
                    if p.type == 'Prism':
                        if math.fabs((math.sqrt((p.pos.x * p.pos.x) + (p.pos.y * p.pos.y))
                        - math.sqrt((self.camFocus.getX() * self.camFocus.getX()) + (self.camFocus.getY() * self.camFocus.getY())))) <= 1000:
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
                    - math.sqrt((self.flamieNP.getX() * self.flamieNP.getX()) + (self.flamieNP.getY() * self.flamieNP.getY())))) <= 2500:
                        p.show()
                    else:
                        p.hide()
                    
                if p.type == 'IceCube':
                    if math.fabs((math.sqrt((p.model.getX() * p.model.getX()) + (p.model.getY() * p.model.getY()))
                    - math.sqrt((self.flamieNP.getX() * self.flamieNP.getX()) + (self.flamieNP.getY() * self.flamieNP.getY())))) <= 2000:
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
            '''

            #Ice cube movement
            self.cave.moveIceCubes(delta)
            for p in self.cave.iceCubesThirdRoom:
                p.bob(delta)
            for p in self.cave.iceCubesSecondRoom:
                p.bob(delta)
            self.cave.bigCube.bob(delta)

            for p in self.start.iceCubes:
                p.bob(delta)

        elif self.inMenu:
            self.menu()


            

        if self.backgroundSound.status() is not self.backgroundSound.PLAYING:
            self.backgroundSound.play()

            
        return task.cont

    def menu(self):
        if self.keyMap["down"]:
            self.inMenu = False
            self.menuScreen.destroy()
            self.initialize()
            

    def flamieBob(self, delta):
        if self.mayFlamieBob:
            self.flamie2.setZ(self.flamie2.getZ() + .5*delta)
            if self.flamie2.getZ() - self.flamie2OriZ > 1:
                self.mayFlamieBob = False
        else:
            self.flamie2.setZ(self.flamie2.getZ() - .5*delta)
            if self.flamie2.getZ() - self.flamie2OriZ < -2:
                self.mayFlamieBob = True
        
    #Function to create a box collision using six polygon. The top face is created as terrain and thus provides gravity.
    #While the rest of the faces only act as wall pushers.
    def collisionBoxCreator(self, posx, posy, posz, length, width, height, floorname, wallname):
        ret = ()
        #Create top face
        terrain = CollisionPolygon(Point3(posx, posy+width, posz), Point3(posx, posy, posz),
                                Point3(posx+length, posy, posz), Point3(posx+length, posy+width, posz))
        terrainCol = CollisionNode(floorname)
        terrainCol.addSolid(terrain)
        terrainCol.setIntoCollideMask(BitMask32.bit(1))
        terrainColNp = self.render.attachNewNode(terrainCol)
        self.cTrav.addCollider(terrainColNp, self.floorHandler)
        ret += (terrainColNp,)
    
        #Create left face
        sideLeft = CollisionPolygon(Point3(posx, posy+width, posz-height), Point3(posx, posy, posz-height),
                                Point3(posx, posy, posz), Point3(posx, posy+width, posz))
        sideLeftCol = CollisionNode(wallname)
        sideLeftCol.addSolid(sideLeft)
        sideLeftCol.setIntoCollideMask(BitMask32.bit(2))
        sideLeftColNp = self.render.attachNewNode(sideLeftCol)
        self.cTrav.addCollider(sideLeftColNp, self.wallHandler)
        ret += (sideLeftColNp,)
        
        #Create right face
        sideRight = CollisionPolygon(Point3(posx+length, posy+width, posz), Point3(posx+length, posy, posz),
                                Point3(posx+length, posy, posz-height), Point3(posx+length, posy+width, posz-height))
        sideRightCol = CollisionNode(wallname)
        sideRightCol.addSolid(sideRight)
        sideRightCol.setIntoCollideMask(BitMask32.bit(2))
        sideRightColNp = self.render.attachNewNode(sideRightCol)
        self.cTrav.addCollider(sideRightColNp, self.wallHandler)
        ret += (sideRightColNp,)
        
        #Create front face
        sideFront = CollisionPolygon(Point3(posx, posy+width, posz-height), Point3(posx, posy+width, posz),
                                Point3(posx+length, posy+width, posz), Point3(posx+length, posy+width, posz-height))
        sideFrontCol = CollisionNode(wallname)
        sideFrontCol.addSolid(sideFront)
        sideFrontCol.setIntoCollideMask(BitMask32.bit(2))
        sideFrontColNp = self.render.attachNewNode(sideFrontCol)
        self.cTrav.addCollider(sideFrontColNp, self.wallHandler)
        ret += (sideFrontColNp,)
        
        #Create back face
        sideBack = CollisionPolygon(Point3(posx, posy, posz), Point3(posx, posy, posz-height),
                                Point3(posx+length, posy, posz-height), Point3(posx+length, posy, posz))
        sideBackCol = CollisionNode(wallname)
        sideBackCol.addSolid(sideBack)
        sideBackCol.setIntoCollideMask(BitMask32.bit(2))
        sideBackColNp = self.render.attachNewNode(sideBackCol)
        self.cTrav.addCollider(sideBackColNp, self.wallHandler)
        ret += (sideBackColNp,)

        #Create bottom face
        sideBot = CollisionPolygon(Point3(posx, posy, posz-height), Point3(posx, posy+width, posz-height),
                                Point3(posx+length, posy+width, posz-height), Point3(posx+length, posy, posz-height))
        sideBotCol = CollisionNode(wallname)
        sideBotCol.addSolid(sideBot)
        sideBotCol.setIntoCollideMask(BitMask32.bit(2))
        sideBotColNp = self.render.attachNewNode(sideBotCol)
        self.cTrav.addCollider(sideBotColNp, self.wallHandler)
        ret += (sideBotColNp,)

        #Uncomment these lines to see the collision polygons.
        '''terrainColNp.show()
        sideLeftColNp.show()
        sideRightColNp.show()
        sideFrontColNp.show()
        sideBackColNp.show()
        sideBotColNp.show()'''

        return ret
        #Old way of creating box collisions (left here for reference)
        '''box = CollisionBox((posx+(length/2), posy+(width/2),-(posz+height/2)), length/2, width/2, height/2)
        boxCol = CollisionNode('testcollision')
        boxCol.addSolid(box)
        boxCol.setIntoCollideMask(BitMask32.bit(2))
        boxColNp = self.render.attachNewNode(boxCol)
        boxHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(boxColNp, self.wallHandler)

        #Uncomment this line to see the collision solids.
        #boxColNp.show()'''

    def checkpointCreator(self, posx, posy, posz, radius):
        cp = loader.loadModel('models/Campfire/logs')
        cp.setPos(posx,posy, posz)
        cp.reparentTo(render)
        checkpoint = CollisionSphere(cp.getX(),cp.getY(),cp.getZ(),radius)
        checkpoint.setTangible(0)
        checkpointCol = CollisionNode('checkpointCol')
        checkpointCol.addSolid(checkpoint)
        checkpointCol.setIntoCollideMask(BitMask32.bit(2))
        checkpointColNp = self.render.attachNewNode(checkpointCol)
        self.cTrav.addCollider(checkpointColNp, self.wallHandler)

demo = Game()
demo.run()
