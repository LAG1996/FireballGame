from direct.showbase.ShowBase import ShowBase

from panda3d.core import LVector3, LVector4
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import AmbientLight, DirectionalLight

from pandac.PandaModules import TransparencyAttrib



class Prism:
    def __init__(self, pos, l, w, h, c, t, name):        
        self.pos = pos
        self.len = l
        self.wid = w
        self.dep = h
        self.color = c
        self.texture = t
        self.name = name
        self.prim = 0
        self.model = 0
        self.Prism()
        self.node = render.attachNewNode(self.model)

    def Prism(self):
        format = GeomVertexFormat.getV3n3cpt2()
        vdata = GeomVertexData('square', format, Geom.UHDynamic)

        vertex = GeomVertexWriter(vdata, 'vertex')
        ####################################
        #First, we need to create the first face, and then base
        #the other faces on it.
        ####################################
        #
        #   DIAGRAM OF A RECTANGULAR PRISM
        #            |--------|
        #            | Face 6 |<-Depth
        #   |--------|--------|--------|--------|
        #   | Face 4 | Face 2 | Face 3 | Face 1 |  <-Width
        #   |        |        |        |        |
        #   |--------|--------|--------|--------|
        #            | Face 5 |          ^Length
        #            |--------|
        ####################################

        #The corner at Quadrant 2 on face 1 is the starting point of our rectangle

        ################################
        #
        # FACE 1
        #
        ################################
        vert1 = LVector3(self.pos.getX(), self.pos.getY(), self.pos.getZ())
        vert2 = LVector3(vert1.getX() + self.len, vert1.getY(), vert1.getZ())
        vert3 = LVector3(vert2.getX(), vert2.getY() + self.wid, vert2.getZ())
        vert4 = LVector3(vert1.getX(), vert1.getY() + self.wid, vert1.getZ())

        vertex.addData3(vert1)
        vertex.addData3(vert2)
        vertex.addData3(vert3)
        vertex.addData3(vert4)

        normal = GeomVertexWriter(vdata, 'normal')
        norm = (vert4 - vert1).cross(vert2 - vert1)
        norm.normalize()

        normal.addData3(norm)
        normal.addData3(norm)
        normal.addData3(norm)
        normal.addData3(norm)

        color = GeomVertexWriter(vdata, 'color')
        color.addData4f(self.color)
        color.addData4f(self.color)
        color.addData4f(self.color)
        color.addData4f(self.color)

        texcoord = GeomVertexWriter(vdata, 'texcoord')
        texcoord.addData2f(1,0)
        texcoord.addData2f(1,1)
        texcoord.addData2f(0,1)
        texcoord.addData2f(0,0)
        

        tris = GeomTriangles(Geom.UHDynamic)

        tris.addVertices(0, 3, 1)
        tris.addVertices(1, 3, 2)


        #####################################
        #
        #   FACE 2
        #
        #####################################

        vert5 = LVector3(vert1.getX(), vert1.getY(), vert1.getZ() - self.dep)
        vert6 = LVector3(vert5.getX() + self.len, vert5.getY(), vert5.getZ())
        vert7 = LVector3(vert6.getX(), vert6.getY() + self.wid, vert6.getZ())
        vert8 = LVector3(vert5.getX(), vert5.getY() + self.wid, vert5.getZ())

        vertex.addData3(vert5)
        vertex.addData3(vert6)
        vertex.addData3(vert7)
        vertex.addData3(vert8)

        norm = (vert8 - vert5).cross(vert6 - vert5)
        norm.normalize()

        normal.addData3(norm)
        normal.addData3(norm)
        normal.addData3(norm)
        normal.addData3(norm)

        color.addData4f(self.color)
        color.addData4f(self.color)
        color.addData4f(self.color)
        color.addData4f(self.color)

        texcoord.addData2f(1,0)
        texcoord.addData2f(1,1)
        texcoord.addData2f(0,1)
        texcoord.addData2f(0,0)

        tris.addVertices(4, 7, 5)
        tris.addVertices(5, 7, 6)


        ########################################
        #
        #   FACE 3
        #
        ########################################
        
        vert9 = vert1
        vert10 = vert2
        vert11 = vert6
        vert12 = vert5

        vertex.addData3(vert9)
        vertex.addData3(vert10)
        vertex.addData3(vert11)
        vertex.addData3(vert12)

        norm = (vert12 - vert9).cross(vert10 - vert9)
        norm.normalize()

        normal.addData3(norm)
        normal.addData3(norm)
        normal.addData3(norm)
        normal.addData3(norm)

        color.addData4f(self.color)
        color.addData4f(self.color)
        color.addData4f(self.color)
        color.addData4f(self.color)

        texcoord.addData2f(1,0)
        texcoord.addData2f(1,1)
        texcoord.addData2f(0,1)
        texcoord.addData2f(0,0)

        tris.addVertices(8, 11, 9)
        tris.addVertices(9, 11, 10)


        ##########################################
        #
        #   FACE 4
        #
        ###########################################

        vert13 = vert4
        vert14 = vert3
        vert15 = vert7
        vert16 = vert8

        vertex.addData3(vert13)
        vertex.addData3(vert14)
        vertex.addData3(vert15)
        vertex.addData3(vert16)

        norm = (vert16 - vert13).cross(vert14 - vert13)
        norm.normalize()

        normal.addData3(norm)
        normal.addData3(norm)
        normal.addData3(norm)
        normal.addData3(norm)

        color.addData4f(self.color)
        color.addData4f(self.color)
        color.addData4f(self.color)
        color.addData4f(self.color)

        texcoord.addData2f(1,0)
        texcoord.addData2f(1,1)
        texcoord.addData2f(0,1)
        texcoord.addData2f(0,0)
        

        tris.addVertices(12, 15, 13)
        tris.addVertices(13, 15, 14)

        square = Geom(vdata)
        square.addPrimitive(tris)

        ###############################################
        #
        #   FACE 5
        #
        ###############################################

        vert17 = vert1
        vert18 = vert4
        vert19 = vert8
        vert20 = vert5

        vertex.addData3(vert17)
        vertex.addData3(vert18)
        vertex.addData3(vert19)
        vertex.addData3(vert20)

        norm = (vert20 - vert17).cross(vert18 - vert17)
        norm.normalize()

        normal.addData3(norm)
        normal.addData3(norm)
        normal.addData3(norm)
        normal.addData3(norm)

        color.addData4f(self.color)
        color.addData4f(self.color)
        color.addData4f(self.color)
        color.addData4f(self.color)

        texcoord.addData2f(1,0)
        texcoord.addData2f(1,1)
        texcoord.addData2f(0,1)
        texcoord.addData2f(0,0)

        tris.addVertices(16, 19, 17)
        tris.addVertices(17, 19, 18)

        ############################################
        #
        #   FACE 6
        #
        ############################################

        vert21 = vert2
        vert22 = vert3
        vert23 = vert7
        vert24 = vert6

        vertex.addData3(vert21)
        vertex.addData3(vert22)
        vertex.addData3(vert23)
        vertex.addData3(vert24)

        norm = (vert21 - vert24).cross(vert21 - vert22)
        norm.normalize()

        normal.addData3(norm)
        normal.addData3(norm)
        normal.addData3(norm)
        normal.addData3(norm)

        color.addData4f(self.color)
        color.addData4f(self.color)
        color.addData4f(self.color)
        color.addData4f(self.color)

        texcoord.addData2f(1,0)
        texcoord.addData2f(1,1)
        texcoord.addData2f(0,1)
        texcoord.addData2f(0,0)

        tris.addVertices(20, 23, 21)
        tris.addVertices(21, 23, 22)

        square = Geom(vdata)
        square.addPrimitive(tris)
        self.prim = square

        self.model = GeomNode(self.name)
        self.model.addGeom(self.prim)

    def attachToSpace(self, model, space):
        self.node = space.attachNewNode(model)

    def generate(self, space):
        self.node = space.attachNewNode(self.model)
        self.node.setTexture(self.texture)
        self.node.setTwoSided(True)

class Ramp:
    def __init__(self, pos, l, w, h, c, t, name):
        #Creating the ramp
        self.pos = pos
        self.len = l
        self.wid = w
        self.dep = h
        self.color = c
        self.texture = t
        self.name = name
        self.prim = 0
        self.model = 0
        self.Ramp()
        self.node = render.attachNewNode(self.model)
        
    #A ramp's like a cube, but it's missing a face
    def Ramp(self):
        format = GeomVertexFormat.getV3n3cpt2()
        vdata = GeomVertexData('square', format, Geom.UHDynamic)

        vertex = GeomVertexWriter(vdata, 'vertex')

        #The corner at Quadrant 2 on face 1 is the starting point of our rectangle

        ################################
        #
        # FACE 1
        #
        ################################
        vert1 = LVector3(self.pos.getX(), self.pos.getY(), self.pos.getZ())
        vert2 = LVector3(vert1.getX() + self.len, vert1.getY(), vert1.getZ())
        vert3 = LVector3(vert2.getX(), vert2.getY() + self.wid, vert2.getZ())
        vert4 = LVector3(vert1.getX(), vert1.getY() + self.wid, vert1.getZ())

        vertex.addData3(vert1)
        vertex.addData3(vert2)
        vertex.addData3(vert3)
        vertex.addData3(vert4)

        normal = GeomVertexWriter(vdata, 'normal')
        norm = (vert4 - vert1).cross(vert2 - vert1)
        norm.normalize()

        normal.addData3(norm)
        normal.addData3(norm)
        normal.addData3(norm)
        normal.addData3(norm)

        color = GeomVertexWriter(vdata, 'color')
        color.addData4f(self.color)
        color.addData4f(self.color)
        color.addData4f(self.color)
        color.addData4f(self.color)

        texcoord = GeomVertexWriter(vdata, 'texcoord')
        texcoord.addData2f(1,0)
        texcoord.addData2f(1,1)
        texcoord.addData2f(0,1)
        texcoord.addData2f(0,0)
        

        tris = GeomTriangles(Geom.UHDynamic)

        tris.addVertices(0, 3, 1)
        tris.addVertices(1, 3, 2)


        #####################################
        #
        #   FACE 2
        #
        #####################################

        vert5 = vert1
        vert6 = vert2
        vert7 = LVector3(vert3.getX(), vert3.getY(), vert3.getZ() + self.dep)
        vert8 = LVector3(vert4.getX(), vert4.getY(), vert4.getZ() + self.dep)

        vertex.addData3(vert5)
        vertex.addData3(vert6)
        vertex.addData3(vert7)
        vertex.addData3(vert8)

        norm = (vert8 - vert5).cross(vert6 - vert5)
        norm.normalize()

        normal.addData3(norm)
        normal.addData3(norm)
        normal.addData3(norm)
        normal.addData3(norm)

        color.addData4f(self.color)
        color.addData4f(self.color)
        color.addData4f(self.color)
        color.addData4f(self.color)

        texcoord.addData2f(1,0)
        texcoord.addData2f(1,1)
        texcoord.addData2f(0,1)
        texcoord.addData2f(0,0)

        tris.addVertices(4, 7, 5)
        tris.addVertices(5, 7, 6)


        ########################################
        #
        #   FACE 3
        #
        ########################################
        
        vert9 = vert1
        vert10 = vert2
        vert11 = vert6
        vert12 = vert5

        vertex.addData3(vert9)
        vertex.addData3(vert10)
        vertex.addData3(vert11)
        vertex.addData3(vert12)

        norm = (vert12 - vert9).cross(vert10 - vert9)
        norm.normalize()
        normal.addData3(norm)
        normal.addData3(norm)
        normal.addData3(norm)
        normal.addData3(norm)

        color.addData4f(self.color)
        color.addData4f(self.color)
        color.addData4f(self.color)
        color.addData4f(self.color)

        texcoord.addData2f(1,0)
        texcoord.addData2f(1,1)
        texcoord.addData2f(0,1)
        texcoord.addData2f(0,0)

        tris.addVertices(8, 11, 9)
        tris.addVertices(9, 11, 10)

        ###############################################
        #
        #   FACE 4
        #
        ###############################################

        vert13 = vert1
        vert14 = vert4
        vert15 = vert8
        vert16 = vert5

        vertex.addData3(vert13)
        vertex.addData3(vert14)
        vertex.addData3(vert15)
        vertex.addData3(vert16)

        norm = (vert16 - vert13).cross(vert14 - vert13)
        norm.normalize()
        normal.addData3(norm)
        normal.addData3(norm)
        normal.addData3(norm)
        normal.addData3(norm)

        color.addData4f(self.color)
        color.addData4f(self.color)
        color.addData4f(self.color)
        color.addData4f(self.color)

        texcoord.addData2f(1,0)
        texcoord.addData2f(1,1)
        texcoord.addData2f(0,1)
        texcoord.addData2f(0,0)

        tris.addVertices(12, 15, 13)
        tris.addVertices(13, 15, 14)

        ############################################
        #
        #   FACE 5
        #
        ############################################

        vert17 = vert2
        vert18 = vert3
        vert19 = vert7
        vert20 = vert6

        vertex.addData3(vert17)
        vertex.addData3(vert18)
        vertex.addData3(vert19)
        vertex.addData3(vert20)

        norm = (vert20 - vert17).cross(vert18 - vert17)
        normal.addData3(norm)
        normal.addData3(norm)
        normal.addData3(norm)
        normal.addData3(norm)

        color.addData4f(self.color)
        color.addData4f(self.color)
        color.addData4f(self.color)
        color.addData4f(self.color)

        texcoord.addData2f(1,0)
        texcoord.addData2f(1,1)
        texcoord.addData2f(0,1)
        texcoord.addData2f(0,0)

        tris.addVertices(16, 19, 17)
        tris.addVertices(17, 19, 18)

        ramp = Geom(vdata)
        ramp.addPrimitive(tris)
        self.prim = ramp

        self.model = GeomNode(self.name)
        self.model.addGeom(self.prim)

    def attachToSpace(self, model, space):
        self.node = space.attachNewNode(model)

    def generate(self, space):
        self.node.setTexture(self.texture)
        self.node.setTwoSided(True)
        
