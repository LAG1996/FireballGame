from direct.showbase.ShowBase import ShowBase

from panda3d.core import LVector3, LVector4
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import AmbientLight, DirectionalLight

from pandac.PandaModules import TransparencyAttrib

from PrimitiveGeoms import Prism, Ramp

class Main(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        #####################
        #
        #   Simply testing procedural geometry generation
        #
        #####################
        prism = Prism(LVector3(0,0,0), 100, 100, 20, LVector4(1,1,1,1), loader.loadTexture("ground.jpg"), 'prism')
        prism.generate(render)

        ramp = Ramp(LVector3(100,100,100), 100, 100, 20, LVector4(1,1,1,1), loader.loadTexture("ground.jpg"), 'ramp')
        ramp.generate(render)



demo = Main()
demo.run()
