from panda3d.core import NodePath, PandaNode
from direct.showbase.ShowBase import ShowBase
from panda3d.core import LVecBase4
from pandac.PandaModules import Texture, TextureStage

def add_shadders(self: ShowBase):

    normalsBuffer = self.win.makeTextureBuffer("normalsBuffer", 0, 0)
    normalsBuffer.setClearColor(LVecBase4(0.5, 0.5, 0.5, 1))
    self.normalsBuffer = normalsBuffer
    normalsCamera = self.makeCamera(
        normalsBuffer, lens=self.cam.node().getLens())
    normalsCamera.node().setScene(self.render)
    tempnode = NodePath(PandaNode("temp node"))
    normalGen = self.loader.loadShader("app/view/shaders/normalGen.sha")
    tempnode.setShader(normalGen)
    tempnode.setShaderInput("showborders", LVecBase4(1))
    normalsCamera.node().setInitialState(tempnode.getState())

    colors_buffer = self.win.makeTextureBuffer("colorsBuffer", 0, 0)
    colors_buffer.setClearColor(LVecBase4(0, 0, 0, 0))
    self.colors_buffer = colors_buffer
    colorsCamera = self.makeCamera(
        colors_buffer, lens=self.cam.node().getLens())

    colorsCamera.node().setScene(self.render)
    tempnode = NodePath(PandaNode("temp node colors"))
    colorGen = self.loader.loadShader("app/view/shaders/colorGen.sha")
    tempnode.setShader(colorGen)
    tempnode.setShaderInput("showborders", LVecBase4(1))
    tempnode.setShaderInput("colorborders", LVecBase4(0,0,0,1))
    colorsCamera.node().setInitialState(tempnode.getState())


    # what we actually do to put edges on screen is apply them as a texture to
    # a transparent screen-fitted card

    drawnScene = normalsBuffer.getTextureCard()
    colorBorderTex = colors_buffer.getTextureCard()

    drawnScene.setTransparency(1)
    drawnScene.setColor(1, 1, 1, 1)
    drawnScene.reparentTo(render2d)
    self.drawnScene = drawnScene

    # this shader accepts, as input, the picture from the normals buffer.
    # it compares each adjacent pixel, looking for discontinuities.
    # wherever a discontinuity exists, it emits black ink.

    self.separation = 0.0005
    self.separation = 1

    self.cutoff = 0.3
    inkGen = loader.loadShader("app/view/shaders/inkGen.sha")

    stageArrow = TextureStage("Arrow")
    stageArrow.setSort(1)
    #drawnScene.setTexture(stageArrow, colorBorderTex.getTexture())
    """
    drawnScene.setShader(inkGen)

    drawnScene.setShaderInput("separation", LVecBase4(self.separation, 0, self.separation, 0))

    drawnScene.setShaderInput("screen", 1280,720)
    drawnScene.setShaderInput("cutoff", LVecBase4(self.cutoff))
    """
    print("SHADER DEBUG")

    print(drawnScene.findAllTextureStages())
