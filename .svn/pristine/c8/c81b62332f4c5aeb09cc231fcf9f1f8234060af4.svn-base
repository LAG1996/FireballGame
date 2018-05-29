'''
Author: Luis Angel Garcia
Date Last Edited: 05/05/16
Description: Cave class that generates the cave portion of the MOD 2 game. There are three parts to the cave with different components.
'''

from direct.showbase.ShowBase import ShowBase

from panda3d.core import LVector3, LVector4, LVector2
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
        self.iceCubesSecondRoom = ()
        self.iceCubesThirdRoom = ()
        self.bigCube = 0
        self.white = LVector4(1,1,1,1)
        self.innerwalltex = loader.loadTexture("caverock.jpg")
        self.snowTex = loader.loadTexture("ground.jpg")

        #Creates an array of ice cube velocities for the cube spinning that will be exhibited in room three.
        self.iceCubeVel = ()

        cube1Vel = LVector2(1, 0)
        self.iceCubeVel += (cube1Vel,)
        
        cube2Vel = LVector2(1, 0)
        self.iceCubeVel += (cube2Vel,)
        
        cube3Vel = LVector2(0, 1)
        self.iceCubeVel += (cube3Vel,)
        
        cube4Vel = LVector2(0, 1)
        self.iceCubeVel += (cube4Vel,)
        
        cube5Vel = LVector2(-1, 0)
        self.iceCubeVel += (cube5Vel,)
        
        cube6Vel = LVector2(0, -1)
        self.iceCubeVel += (cube6Vel,)
        
        cube7Vel = LVector2(0, -1)
        self.iceCubeVel += (cube7Vel,)
        
        cube8Vel = LVector2(-1, 0)
        self.iceCubeVel += (cube8Vel,)

        self.corn1 = 0
        self.corn2 = 0
        self.corn3 = 0
        self.corn4 = 0

        ########
        #
        #   ENTRANCE OF CAVE
        #
        ########
        self.entrance = Prism(pos, 200, 500, 50, self.white, self.snowTex, 'entrance')
        self.parts += (self.entrance,)

        self.setFirstRoom()

        '''
        Add all parts of the first room of the cave into the cave part queue
        '''
        for p in self.firstRoomParts:
            self.parts += (p,)

        '''
        Add all parts of the second room of the cave into the cave part queue
        '''
        for p in self.secondRoomParts:
            self.parts += (p,)

        '''
        Add all parts of the third room of the cave into the cave part queue
        '''
        for p in self.thirdRoomParts:
            self.parts += (p,)
            
        '''
        Add all ice cubes of second room to the cave part queue
        '''
        for p in self.iceCubesSecondRoom:
            self.parts += (p,)

        '''
        Add all ice cubes of third room to the cave part queue
        '''
        for p in self.iceCubesThirdRoom:
            self.parts += (p,)

        self.parts += (self.bigCube,)
        

    def generateAllParts(self, space):
        #Generates all objects in cave part queue
        for p in self.parts:
            p.generate(space)


    ###############################
    #
    #   FIRST ROOOM.
    #
    ###############################
    def setFirstRoom(self):
        distFloortoEnt = 500
        roofHeight = 300
        floor = Prism(LVector3(self.entrance.pos.x - distFloortoEnt, self.entrance.pos.y + self.entrance.wid, self.entrance.pos.z - 30),
                      self.entrance.len + distFloortoEnt, 400, 50, self.white, self.innerwalltex, 'firstFloor')
        self.firstRoomParts += (floor,)

        #Ramps aren't ramps anymore, but I don't want to go through the trouble of changing variable names
        ramp_1 = Prism(LVector3(floor.pos.x + floor.len/1.6, floor.pos.y, floor.pos.z + 10),
                      floor.len/8, floor.wid, 10, self.white, self.innerwalltex, 'ramp_1')
        self.firstRoomParts+= (ramp_1,)

        ramp_2 = Prism(LVector3(ramp_1.pos.x - ramp_1.len, ramp_1.pos.y, floor.pos.z + ramp_1.dep * 1.5),
                      ramp_1.len, ramp_1.wid, ramp_1.dep * 1.5, self.white, self.innerwalltex, 'ramp_2')
        self.firstRoomParts+= (ramp_2,)
        ramp_3 = Prism(LVector3(ramp_2.pos.x - ramp_2.len, ramp_1.pos.y, floor.pos.z + ramp_1.dep * 1.4),
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

        backWall = Prism(LVector3(floor.pos.x, floor.pos.y + floor.wid, floor.pos.z + rightWall_1.dep),
                         floor.len, rightWall_1.wid, rightWall_1.dep, self.white, self.innerwalltex, "backwall")
        self.firstRoomParts += (backWall,)

        #Generate second room
        self.setSecondRoom(floor, roofHeight)

    def generateFirstRoom(self, space):
        for p in self.firstRoomParts:
            p.generate(space)

    #####################
    #
    #   SECOND ROOM GENERATION
    #
    #####################    
    def setSecondRoom(self, floor, roof):
        distBetweenWalls = 250
        wall_1 = Prism(LVector3(floor.pos.x, floor.pos.y + floor.wid, floor.pos.z + roof),
                       100, 1000, 1000, self.white, self.innerwalltex, 'wall_1')
        self.secondRoomParts+=(wall_1,)

        wall_2 = Prism(LVector3(wall_1.pos.x - distBetweenWalls, floor.pos.y, wall_1.pos.z),
                       wall_1.len, wall_1.wid + floor.wid, wall_1.dep, self.white, self.innerwalltex, 'wall_2')
        self.secondRoomParts+=(wall_2,)

        #Set platforms in room 2
        self.platformsRoom2(floor, distBetweenWalls)

        #Generate third room
        self.setThirdRoom(wall_1, wall_2, distBetweenWalls)

    #Render second room
    def generateSecondRoom(self, space):
        for p in self.secondRoomParts:
            p.generate(space)


    ########################
    #
    #   THIRD ROOM GENERATION
    #
    ########################
    def setThirdRoom(self, wall1, wall2, dist):
        sidelen = 250
           
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

        safePlat2 = Prism(LVector3(safePlat.pos.x, safePlat.pos.y + safePlat.wid, safePlat.pos.z),
                          safePlat.len/1.5, backWall_left.pos.y - (safePlat.pos.y + safePlat.wid), safePlat.dep, self.white, self.innerwalltex, 'safePlat2')
        self.thirdRoomParts+=(safePlat2,)

        #The only ice cube that will not be part of the third room ice cube queue is the big cube at the end of the cave
        self.bigCube = IceCube(LVector3(backWall_left.pos.x + backWall_left.len*1.8,
                                        backWall_left.pos.y - backWall_left.wid/3.9,
                                        backWall_left.pos.z - backWall_left.dep/3),
                               26, 0, 0, 0.1)

        #Set platforms in room 3
        self.platformsRoom3(safePlat)


    ####################
    #
    #   PLACE ICE CUBES IN SECOND ROOM
    #
    ####################
    def platformsRoom2(self, floor, disp):
        space = 13
        scale = 5
        displacement = 0
        floatspeed = 20
        cube1 = IceCube(LVector3(floor.pos.x - disp/5, floor.pos.y + floor.wid/2, floor.pos.z - floor.dep/2),
                        scale, displacement, floatspeed, 0)
        self.iceCubesSecondRoom += (cube1,)

        yPos = cube1.model.getY()
        i = 0

        #Place a path of 26 cubes down the hallway
        while i < 18:
            self.iceCubesSecondRoom += (IceCube(LVector3(cube1.model.getX(), yPos + scale*space, cube1.model.getZ()),
                                      scale, displacement, floatspeed, 0),)
            yPos += scale*space
            i+=1


    ###################
    #
    #   PLACE PLATFORMS AND ICE CUBES IN THIRD ROOM
    #
    ###################
    '''
    DIAGRAM OF PLATFORM POSITIONS:

    cube7       cube8       cube5



    cube6       safePlat    cube4



    cube1       cube2       cube3
    '''
    def platformsRoom3(self, plat):
        space = 20
        scale = 5
        displacement = 3
        floatspeed = 5
        meltspeed = .05
        cube1 = IceCube(LVector3(plat.pos.x + plat.len/1.1, plat.pos.y + plat.wid * 1.5, plat.pos.z - 15), scale, displacement, floatspeed, meltspeed)
        self.iceCubesThirdRoom += (cube1,)
        self.corn1 = cube1.model.getPos()
        
        cube2 = IceCube(LVector3(cube1.model.getX() + scale*space, cube1.model.getY(), cube1.model.getZ()),
                        scale, displacement, floatspeed, meltspeed)
        self.iceCubesThirdRoom += (cube2,)
        
        cube3 = IceCube(LVector3(cube2.model.getX() + scale*space, cube2.model.getY(), cube2.model.getZ()),
                        scale, displacement, floatspeed, meltspeed)
        self.iceCubesThirdRoom += (cube3,)
        self.corn2 = cube3.model.getPos()
        
        
        cube4 = IceCube(LVector3(cube3.model.getX(), cube3.model.getY() + scale*space, cube3.model.getZ()),
                        scale, displacement, floatspeed, meltspeed)
        self.iceCubesThirdRoom += (cube4,)
        
        cube5 = IceCube(LVector3(cube4.model.getX(), cube4.model.getY() + scale*space, cube4.model.getZ()),
                        scale, displacement, floatspeed, meltspeed)
        self.iceCubesThirdRoom += (cube5,)
        self.corn3 = cube5.model.getPos()
        

        cube6 = IceCube(LVector3(cube1.model.getX(), cube1.model.getY() + scale*space, cube1.model.getZ()),
                        scale, displacement, floatspeed, meltspeed)
        self.iceCubesThirdRoom += (cube6,)
        
        cube7 = IceCube(LVector3(cube6.model.getX(), cube6.model.getY() + scale*space, cube6.model.getZ()),
                        scale, displacement, floatspeed, meltspeed)
        self.iceCubesThirdRoom += (cube7,)
        self.corn4 = cube7.model.getPos()

        cube8 = IceCube(LVector3(cube7.model.getX() + scale*space, cube7.model.getY(), cube7.model.getZ()),
                        scale, displacement, floatspeed, meltspeed)
        self.iceCubesThirdRoom += (cube8,)

        safePlat3 = Prism(LVector3(plat.pos.x + plat.len + 50, plat.pos.y + plat.wid*1.8, plat.pos.z),
                         100, 150, 300, self.white, self.innerwalltex, 'safePlat3')
        self.thirdRoomParts += (safePlat3,)

        safePlat4 = Prism(LVector3(safePlat3.pos.x, safePlat3.pos.y + safePlat3.wid * 1.35, plat.pos.z),
                         100, 500, 300, self.white, self.innerwalltex, 'safePlat3')
        self.thirdRoomParts += (safePlat4,)

    #Render third room
    def generateThirdRoom(self, space):
        for p in self.thirdRoomParts:
            p.generate(space)


    '''
    Moves ice cubes in the cave in a counter clockwise motion.
    Uses elements of the iceCubesThirdRoom and iceCubeVel queue.
    The individual elements of the queue could be identified as follows:

    Index       Identifier
    0           cube1       cube1Vel
    1           cube2       cube2Vel
    2           cube3       cube3Vel
    3           cube4       cube4Vel
    4           cube5       cube5Vel
    5           cube6       cube6Vel
    6           cube7       cube7Vel
    7           cube8       cube8Vel
    '''
    def moveIceCubes(self, delta):
        SPEED = 25

        #Check for position and velocity of each ice cube and update when they reach a corner.
        i = 0
        while i <= 7:
            if self.iceCubesThirdRoom[i].model.getX() >= self.corn2.x and self.iceCubeVel[i].x == 1:
                self.iceCubesThirdRoom[i].model.setX(self.corn2.x)
                self.iceCubeVel[i].x = 0
                self.iceCubeVel[i].y = 1
            elif self.iceCubesThirdRoom[i].model.getY() >= self.corn3.y and self.iceCubeVel[i].y == 1:
                self.iceCubesThirdRoom[i].model.setY(self.corn3.y)
                self.iceCubeVel[i].x = -1
                self.iceCubeVel[i].y = 0
            elif self.iceCubesThirdRoom[i].model.getX() <= self.corn4.x and self.iceCubeVel[i].x == -1:
                self.iceCubesThirdRoom[i].model.setX(self.corn4.x)
                self.iceCubeVel[i].x = 0
                self.iceCubeVel[i].y = -1
            elif self.iceCubesThirdRoom[i].model.getY() <= self.corn1.y and self.iceCubeVel[i].y == -1:
                self.iceCubesThirdRoom[i].model.setY(self.corn1.y)
                self.iceCubeVel[i].x = 1
                self.iceCubeVel[i].y = 0

            self.iceCubesThirdRoom[i].model.setX(self.iceCubesThirdRoom[i].model.getX() + self.iceCubeVel[i].x * SPEED * delta)
            self.iceCubesThirdRoom[i].model.setY(self.iceCubesThirdRoom[i].model.getY() + self.iceCubeVel[i].y * SPEED * delta)
            i+=1   

        
    
        

