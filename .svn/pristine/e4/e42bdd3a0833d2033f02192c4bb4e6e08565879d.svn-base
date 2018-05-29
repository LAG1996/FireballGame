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

from IceCube import IceCube

import sys

class Main(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.iceCube = IceCube(LVector3(0,100,0), 3, 20, 10, .15)
        self.iceCube.generate(render)
        #base.camera.lookAt(self.iceCube.model)

        taskMgr.add(self.update, 'update')

    def update(self, task):
        self.iceCube.bob(globalClock.getDt())
                                               
        if not self.iceCube.melted:
            self.iceCube.melt(globalClock.getDt())

        return task.cont

demo = Main()
demo.run()
