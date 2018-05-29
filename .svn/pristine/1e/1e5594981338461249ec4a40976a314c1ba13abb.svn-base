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

import sys
import math
import random

from pandac.PandaModules import *


class End:
    def __init__(self, pos):
        self.bigCube = 0
        self.white = LVector4(1,1,1,1)
        self.snowTex = loader.loadTexture("ground.jpg")
        self.floor = Prism(pos, 500, 500, 50, self.white, self.snowTex, 'endFloor')


    def generate(self, space):
        self.floor.generate(space)
