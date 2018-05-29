from direct.showbase.ShowBase import ShowBase

from panda3d.core import LVector3, LVector4
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import AmbientLight, DirectionalLight, Spotlight, PerspectiveLens

from pandac.PandaModules import TransparencyAttrib
from IceCube import IceCube

import sys

class Main(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.cube = IceCube(LVector3(0,0,0), 2, 5, 1)
        self.cube.generate(render)

        taskMgr.add(self.update, "update")

    def update(self, task):
        self.cube.bob()

        return task.cont
        

demo = Main()
demo.run()
