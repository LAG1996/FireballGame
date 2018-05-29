from direct.showbase.ShowBase import ShowBase

from panda3d.core import LVector3, LVector4
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import AmbientLight, DirectionalLight, Spotlight, PerspectiveLens

from pandac.PandaModules import TransparencyAttrib

import sys

class Main(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.scale = 10
        self.shrink = False
        self.MAXTIME = 30
        self.timer = 0
        
        iceTex = loader.loadTexture("ice.png")

        self.cube = loader.loadModel('ice.obj')
        self.cube.setTransparency(TransparencyAttrib.MAlpha)
        self.cube.setScale(self.scale)
        self.cube.setTexture(iceTex)
        self.cube.reparentTo(render)
        self.cube.setAlphaScale(0.7)

        taskMgr.add(self.update, "update")

    def update(self, task):
        if self.timer >= self.MAXTIME and self.scale > 0:
            self.scale -= 0.5
            self.timer = 0
        else:
            self.timer += 1
            
        self.cube.setScale(self.scale)

        return task.cont
        

demo = Main()
demo.run()
