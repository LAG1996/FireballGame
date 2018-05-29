from direct.showbase.ShowBase import ShowBase

from panda3d.core import LVector3, LVector4
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import AmbientLight, DirectionalLight

from pandac.PandaModules import TransparencyAttrib

from PrimitiveGeoms import Prism, Ramp
from IceCube import IceCube

class Cave:
    def __init__(self, pos):
        self.parts = ()
        self.firstRoomParts = ()
        self.secondRoomParts = ()
        self.thirdRoomParts = ()
        self.iceCubes = ()
        self.white = LVector4(1,1,1,1)
        self.innerwalltex = loader.loadTexture("caverock.jpg")
        self.snowTex = loader.loadTexture("ground.jpg")

        ########
        #
        #   ENTRANCE OF CAVE
        #
        ########
        self.entrance = Prism(pos, 200, 500, 50, self.white, self.snowTex, 'entrance')
        self.parts += (self.entrance,)

        self.setFirstRoom()

        for p in self.firstRoomParts:
            self.parts += (p,)

        for p in self.secondRoomParts:
            self.parts += (p,)

        for p in self.thirdRoomParts:
            self.parts += (p,)

        for p in self.iceCubes:
            self.parts += (p,)
        

    def generateAllParts(self, space):
        for p in self.parts:
            p.generate(space)

    def setFirstRoom(self):
        distFloortoEnt = 500
        roofHeight = 300
        floor = Prism(LVector3(self.entrance.pos.x - distFloortoEnt, self.entrance.pos.y + self.entrance.wid, self.entrance.pos.z - 30),
                      self.entrance.len + distFloortoEnt, 400, 50, self.white, self.innerwalltex, 'firstFloor')
        self.firstRoomParts += (floor,)
        
        ramp_1 = Ramp(LVector3(floor.pos.x + floor.len/1.6, floor.pos.y, floor.pos.z),
                      floor.len/8, floor.wid, 60, self.white, self.innerwalltex, 'ramp_1')
        self.firstRoomParts+= (ramp_1,)

        ramp_2 = Ramp(LVector3(ramp_1.pos.x + ramp_1.len*1.5, ramp_1.pos.y - 1400, ramp_1.pos.z),
                      ramp_1.len, ramp_1.wid, ramp_1.dep * 1.5, self.white, self.innerwalltex, 'ramp_2')
        ramp_2.node.setH(180)
        self.firstRoomParts+= (ramp_2,)
        ramp_3 = Ramp(LVector3(ramp_1.pos.x - (ramp_1.len)*2 - (ramp_1.len)/2, ramp_1.pos.y, ramp_1.pos.z),
                      ramp_1.len*1.5, ramp_1.wid, ramp_1.dep * 1.4, self.white, self.innerwalltex, 'ramp_3')
        self.firstRoomParts+=(ramp_3,)

        stalag_1 = Prism(LVector3(floor.pos.x + floor.len/2, floor.pos.y + floor.wid/2, floor.pos.z + roofHeight),
                         30, 30, 120, self.white, self.innerwalltex, 'stalag_1')
        self.firstRoomParts+=(stalag_1,)

        stalag_2 = Prism(LVector3(stalag_1.pos.x + stalag_1.wid, stalag_1.pos.y + 10, stalag_1.pos.z),
                         stalag_1.len - 10, stalag_1.wid - 10, stalag_1.dep/2, self.white, self.innerwalltex, 'stalag_2')
        self.firstRoomParts+=(stalag_2,)

        stalag_3 = Prism(LVector3(stalag_1.pos.x - stalag_2.wid, stalag_2.pos.y, stalag_1.pos.z),
                         stalag_2.len, stalag_2.wid, stalag_2.dep, self.white, self.innerwalltex, 'stalag_3')
        self.firstRoomParts+=(stalag_3,)

        stalag_4 = Prism(LVector3(stalag_1.pos.x + 10, stalag_1.pos.y - stalag_1.wid, stalag_1.pos.z),
                         stalag_2.len, stalag_2.wid, stalag_2.dep, self.white, self.innerwalltex, 'stalag_4')
        self.firstRoomParts+=(stalag_4,)

        stalag_5 = Prism(LVector3(stalag_3.pos.x, stalag_1.pos.y + stalag_2.wid, stalag_1.pos.z),
                         stalag_2.len, stalag_2.wid, stalag_2.dep, self.white, self.innerwalltex, 'stalag_5')
        self.firstRoomParts += (stalag_5,)

        mite_1 = Prism(LVector3(ramp_1.pos.x - ramp_1.wid/2, floor.pos.y, floor.pos.z+ roofHeight/2),
                       ramp_2.len/2, 45, roofHeight/2, self.white, self.innerwalltex, 'mite_1')
        self.firstRoomParts+=(mite_1,)

        mite_2 = Prism(LVector3(mite_1.pos.x + mite_1.wid, mite_1.pos.y, floor.pos.z + roofHeight/1.3),
                       mite_1.len, mite_1.wid + 10, roofHeight/1.3, self.white, self.innerwalltex, 'mite_2')
        self.firstRoomParts+=(mite_2,)

        rod_1 = Prism(LVector3(floor.pos.x + floor.wid/10, floor.pos.y + floor.wid/2, floor.pos.z + roofHeight),
                      50, 50, roofHeight, self.white, self.innerwalltex, 'rod_1')
        self.firstRoomParts+=(rod_1,)

        rightWall_1 = Prism(LVector3(floor.pos.x + floor.len - 10, floor.pos.y, floor.pos.z + roofHeight),
                            10, floor.wid/3, roofHeight, self.white, self.innerwalltex, 'rightWall_1')
        self.firstRoomParts+=(rightWall_1,)

        rightWall_2 = Prism(LVector3(rightWall_1.pos.x, rightWall_1.pos.y+rightWall_1.wid, floor.pos.z + roofHeight/1.5),
                            rightWall_1.len, floor.wid/5, roofHeight/1.5, self.white, self.innerwalltex, 'rightWall_2')
        self.firstRoomParts+=(rightWall_2,)

        rightWall_3 = Prism(LVector3(rightWall_2.pos.x - 20, rightWall_2.pos.y + rightWall_2.wid, floor.pos.z + roofHeight/1.9),
                            rightWall_1.len + 20, floor.wid/7, roofHeight/1.9, self.white, self.innerwalltex, 'rightWall_3')
        self.firstRoomParts+=(rightWall_3,)

        rightWall_4 = Prism(LVector3(rightWall_1.pos.x, floor.pos.y + (rightWall_1.wid + rightWall_2.wid + rightWall_3.wid), floor.pos.z + roofHeight),
                            rightWall_2.len, floor.wid - (rightWall_1.wid + rightWall_2.wid+ rightWall_3.wid), roofHeight, self.white, self.innerwalltex, 'rightWall_4')
        self.firstRoomParts+=(rightWall_4,)
        
        self.setSecondRoom(floor, roofHeight)

    def generateFirstRoom(self, space):
        for p in self.firstRoomParts:
            p.generate(space)

    def setSecondRoom(self, floor, roof):
        distBetweenWalls = 300
        wall_1 = Prism(LVector3(floor.pos.x, floor.pos.y + floor.wid, floor.pos.z + roof),
                       100, 2000, 1000, self.white, self.innerwalltex, 'wall_1')
        self.secondRoomParts+=(wall_1,)

        wall_2 = Prism(LVector3(wall_1.pos.x - distBetweenWalls, floor.pos.y, wall_1.pos.z),
                       wall_1.len, wall_1.wid + floor.wid, wall_1.dep, self.white, self.innerwalltex, 'wall_2')
        self.secondRoomParts+=(wall_2,)

        self.platformsRoom2(floor, distBetweenWalls)

        self.setThirdRoom(wall_1, wall_2, distBetweenWalls)

    def generateSecondRoom(self, space):
        for p in self.secondRoomParts:
            p.generate(space)

    def setThirdRoom(self, wall1, wall2, dist):
        sidelen = 500
           
        wall_3 = Prism(LVector3(wall1.pos.x, wall1.pos.y + wall1.wid, wall1.pos.z),
                       sidelen + wall1.len, wall1.len, wall1.dep, self.white, self.innerwalltex, 'wall_3')
        self.thirdRoomParts+=(wall_3,)

        wall_4 = Prism(LVector3(wall2.pos.x, wall2.pos.y + wall2.wid, wall2.pos.z),
                       wall2.len, sidelen * 2, wall2.dep, self.white, self.innerwalltex, 'wall_4')
        self.thirdRoomParts+=(wall_4,)

        wall_5 = Prism(LVector3(wall_3.pos.x + wall_3.len, wall_4.pos.y, wall_4.pos.z),
                       wall_4.len, wall_4.wid, wall_4.dep, self.white, self.innerwalltex, 'wall_5')
        self.thirdRoomParts+=(wall_5,)

        backWall_right = Prism(LVector3(wall_5.pos.x - wall_3.len/2.5, wall_5.pos.y + wall_5.wid, wall_5.pos.z),
                               wall_3.len/2.5, wall_5.len, wall_5.dep, self.white, self.innerwalltex, 'backWall_right')
        self.thirdRoomParts +=(backWall_right,)

        backWall_left = Prism(LVector3(wall_4.pos.x + wall_4.len, wall_4.pos.y + wall_4.wid, wall_4.pos.z),
                              backWall_right.len, backWall_right.wid, backWall_right.dep, self.white, self.innerwalltex, 'backWall_left')
        self.thirdRoomParts +=(backWall_left,)

        safePlat = Prism(LVector3(wall2.pos.x + wall2.len, wall2.pos.y + wall2.wid, wall2.pos.z - wall2.dep/3),
                         dist - wall2.len, wall_4.wid/5, wall2.dep/3, self.white, self.innerwalltex, 'safePlat')
        self.thirdRoomParts+=(safePlat,)

        bigCube = IceCube(LVector3(backWall_left.pos.x + backWall_left.len*1.5, backWall_left.pos.y - backWall_left.wid, backWall_left.pos.z - backWall_left.dep/4),
                          30, 50, 5)
        self.iceCubes += (bigCube,)

        self.platformsRoom3(safePlat)

    def platformsRoom2(self, floor, disp):
        space = 10
        scale = 8
        displacement = 50
        floatspeed = 1
        cube1 = IceCube(LVector3(floor.pos.x - disp/3, floor.pos.y + floor.wid/2, floor.pos.z - floor.dep*2),
                        scale, displacement, floatspeed)
        self.iceCubes += (cube1,)

        yPos = cube1.model.getY()
        i = 0
        while i < 26:
            self.iceCubes += (IceCube(LVector3(cube1.model.getX(), yPos + scale*space, cube1.model.getZ()),
                                      scale, displacement, floatspeed),)
            yPos += scale*space
            i+=1

    def platformsRoom3(self, plat):
        space = 30
        scale = 8
        displacement = 50
        floatspeed = 3
        cube1 = IceCube(LVector3(plat.pos.x + plat.len, plat.pos.y + plat.wid + plat.wid/2, plat.pos.z), scale, displacement, floatspeed)
        self.iceCubes += (cube1,)
        cube2 = IceCube(LVector3(cube1.model.getX() + scale*space, cube1.model.getY(), cube1.model.getZ()),
                        scale, displacement, floatspeed)
        self.iceCubes += (cube2,)
        cube3 = IceCube(LVector3(cube2.model.getX() + scale*space, cube2.model.getY(), cube2.model.getZ()),
                        scale, displacement, floatspeed)
        self.iceCubes += (cube3,)
        
        cube4 = IceCube(LVector3(cube3.model.getX(), cube3.model.getY() + scale*space, cube3.model.getZ()),
                        scale, displacement, floatspeed)
        self.iceCubes += (cube4,)
        cube5 = IceCube(LVector3(cube4.model.getX(), cube4.model.getY() + scale*space, cube4.model.getZ()),
                        scale, displacement, floatspeed)
        self.iceCubes += (cube5,)

        cube6 = IceCube(LVector3(cube1.model.getX(), cube1.model.getY() + scale*space, cube1.model.getZ()),
                        scale, displacement, floatspeed)
        self.iceCubes += (cube6,)
        cube7 = IceCube(LVector3(cube6.model.getX(), cube6.model.getY() + scale*space, cube6.model.getZ()),
                        scale, displacement, floatspeed)
        self.iceCubes += (cube7,)

        cube8 = IceCube(LVector3(cube7.model.getX() + scale*space, cube7.model.getY(), cube7.model.getZ()),
                        scale, displacement, floatspeed)
        self.iceCubes += (cube8,)

        safePlat = Prism(LVector3(cube4.model.getX() - space * scale - space * 2, cube4.model.getY() - 25, cube4.model.getZ() + 75),
                         150, 150, 300, self.white, self.innerwalltex, 'safePlat2')
        self.thirdRoomParts += (safePlat,)

    def generateThirdRoom(self, space):
        for p in self.thirdRoomParts:
            p.generate(space)

        
    
        

