from direct.showbase.ShowBase import ShowBase
from panda3d.core import LVector3, LVector4
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import AmbientLight, DirectionalLight, Spotlight, PerspectiveLens

from pandac.PandaModules import TransparencyAttrib

from PrimitiveGeoms import Prism, Ramp, Square
from IceCube import IceCube

class PlatformSeg:
    def __init__(self, pos):
        self.parts = ()
        self.iceCubes = ()
        self.trunks = ()
        self.pos = pos

        self.white = LVector4(1,1,1,1)
        self.snow = loader.loadTexture('ground.jpg')
        self.ice = loader.loadTexture('ice.png')
        self.tree = loader.loadTexture('tree.png')
        self.deadTree = loader.loadTexture('deadTree.png')

        self.buildStartingArea()

        for p in self.iceCubes:
            self.parts += (p,)

    def buildStartingArea(self):
        plane = Prism(self.pos, 600, 600, 20, self.white, self.snow, 'start')
        self.parts += (plane,)

        auxillary = Prism(LVector3(plane.pos.x + plane.len/2, plane.pos.y + plane.wid, plane.pos.z),
                          plane.len/2, plane.wid/10, plane.dep, self.white, self.snow, 'auxillary')
        self.parts += (auxillary,)

        self.platformingOne(auxillary)

    def platformingOne(self, aux):
        scale = 3
        space = 30
        displacement = 10
        floatspeed = 10
        plat_1 = IceCube(LVector3(aux.pos.x + aux.len/2, aux.pos.y + aux.wid * 1.5, aux.pos.z - 25),
                         scale, displacement, floatspeed)
        self.iceCubes += (plat_1,)

        plat_2 = IceCube(LVector3(plat_1.model.getX(), plat_1.model.getY() + scale*space, plat_1.model.getZ()),
                         scale, displacement, floatspeed)
        self.iceCubes += (plat_2,)

        plat_3 = IceCube(LVector3(plat_2.model.getX() + space, plat_2.model.getY() + scale*space, plat_2.model.getZ()),
                         scale, displacement, floatspeed)
        self.iceCubes += (plat_3,)

        plat_4 = IceCube(LVector3(plat_3.model.getX() + space*scale, plat_3.model.getY() - space, plat_3.model.getZ() - 10),
                         scale * 1.5, displacement * 2, floatspeed)
        self.iceCubes += (plat_4,)

        plat_5 = IceCube(LVector3(plat_4.model.getX() + space*scale, plat_3.model.getY(), plat_3.model.getZ()),
                         scale, displacement, floatspeed)
        self.iceCubes += (plat_5,)

        plat_6 = Prism(LVector3(plat_5.model.getX() + space*scale/1.5, plat_5.model.getY() - space, aux.pos.z),
                       aux.len/5, aux.wid*2, aux.dep, self.white, self.snow, 'plat_6')
        self.parts += (plat_6,)

        self.platformingTwo(plat_6)
                         

    def platformingTwo(self, plat):
        scale = 3
        space = 30
        displacement = 10
        floatspeed = 10

        treePlat = Square(LVector3(plat.pos.x + plat.len/1.5, plat.pos.y, plat.pos.z + 10),
                          500, 100, self.white, self.deadTree, 'treePlat_1')
        self.parts += (treePlat,)
        

    def generateAllParts(self, space):
        for p in self.parts:
            p.generate(render)
