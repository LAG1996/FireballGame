from direct.showbase.ShowBase import ShowBase

from panda3d.core import LVector3, LVector4
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import AmbientLight, DirectionalLight

from pandac.PandaModules import TransparencyAttrib

from PrimitiveGeoms import Prism, Ramp

class LostWood:
    def __init__(self, pos):
        self.parts = ()
        self.trees = ()

        self.white = LVector4(1,1,1,1)
        self.snowtex = loader.loadTexture("ground.jpg")
        self.ice = loader.loadTexture("iceground.jpg")

        self.pos = pos

        piece_1 = Prism(pos, 400, 400, 50, self.white, self.snowtex, 'piece_1')
        self.parts += (piece_1,)

        piece_2 = Prism(LVector3(piece_1.pos.x, piece_1.pos.y + piece_1.wid, piece_1.pos.z),
                        piece_1.len/1.5, piece_1.wid, piece_1.dep, self.white, self.snowtex, 'piece_2')
        self.parts += (piece_2,)

        piece_3 = Prism(LVector3(piece_1.pos.x + piece_1.wid + 25, piece_1.pos.y, piece_1.pos.z),
                        1000, 700, 50, self.white, self.snowtex, 'piece_3')
        self.parts += (piece_3,)

        piece_4 = Prism(LVector3(piece_3.pos.x + piece_3.len - 250, piece_3.pos.y + piece_3.wid, piece_3.pos.z),
                        250, 500, 50, self.white, self.ice, 'piece_4')
        self.parts += (piece_4,)

        piece_5 = Prism(LVector3(piece_3.pos.x, piece_3.pos.y + piece_3.wid, piece_3.pos.z),
                        50, 200, 10, self.white, self.snowtex, 'piece_5')
        self.parts += (piece_5,)

        piece_6 = Prism(LVector3(piece_5.pos.x + piece_5.len, piece_4.pos.y, piece_4.pos.z),
                        50, 100, 10, self.white, self.snowtex, 'piece_6')
        self.parts += (piece_6,)

        piece_7 = Prism(LVector3(piece_4.pos.x - 900, piece_4.pos.y + piece_4.wid + 50, piece_4.pos.z),
                        1000, 1000, 10, self.white, self.snowtex, 'piece_7')
        self.parts += (piece_7,)


    def generateAllParts(self, render):
        for p in self.parts:
            p.generate(render)
