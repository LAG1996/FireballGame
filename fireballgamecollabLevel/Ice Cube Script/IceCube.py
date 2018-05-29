from direct.showbase.ShowBase import ShowBase

from panda3d.core import LVector3, LVector4
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import AmbientLight, DirectionalLight, Spotlight, PerspectiveLens

from pandac.PandaModules import TransparencyAttrib

import sys

class IceCube:
    def __init__(self, pos, scale, displacement, floatspeed):
        self.model = loader.loadModel('ice.obj')
        self.model.setTexture(loader.loadTexture('ice.png'))
        self.model.setTransparency(TransparencyAttrib.MAlpha)
        self.model.setScale(scale)
        self.model.setAlphaScale(0.5)

        self.model.setPos(pos)
        self.origin = pos
        self.displacement = displacement
        self.floatspeed = floatspeed

        self.float = False

    def generate(self, space):
        self.model.reparentTo(space)

    def bob(self):
        delta = globalClock.getDt()
        if self.model.getZ() <= self.origin.z - self.displacement:
            self.float = True
        elif self.model.getZ() >= self.origin.z:
            self.float = False

        if self.float:
            self.model.setZ(self.model.getZ() + self.floatspeed*delta)
        else:
            self.model.setZ(self.model.getZ() - self.floatspeed*delta)
