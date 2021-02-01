from panda3d.core import NodePath, PandaNode
from direct.showbase.ShowBase import ShowBase
from panda3d.core import LVecBase4

def add_shadders(self: ShowBase):

    normalsBuffer = self.win.makeTextureBuffer("normalsBuffer", 0, 0)
    normalsBuffer.setClearColor(LVecBase4(0.5, 0.5, 0.5, 1))
    self.normalsBuffer = normalsBuffer
    normalsCamera = self.makeCamera(
        normalsBuffer, lens=self.cam.node().getLens())
    normalsCamera.node().setScene(self.render)
    tempnode = NodePath(PandaNode("temp node"))
    tempnode.setShader(self.loader.loadShader("app/view/shaders/normalGen.sha"))
    normalsCamera.node().setInitialState(tempnode.getState())

    # what we actually do to put edges on screen is apply them as a texture to
    # a transparent screen-fitted card

    drawnScene = normalsBuffer.getTextureCard()
    drawnScene.setTransparency(1)
    drawnScene.setColor(1, 1, 1, 0)
    drawnScene.reparentTo(render2d)
    self.drawnScene = drawnScene

    # this shader accepts, as input, the picture from the normals buffer.
    # it compares each adjacent pixel, looking for discontinuities.
    # wherever a discontinuity exists, it emits black ink.

    self.separation = 0.0005
    self.cutoff = 0.3
    inkGen = loader.loadShader("app/view/shaders/inkGen.sha")
    drawnScene.setShader(inkGen)
    drawnScene.setShaderInput("separation", LVecBase4(self.separation, 0, self.separation, 0))
    drawnScene.setShaderInput("cutoff", LVecBase4(self.cutoff))