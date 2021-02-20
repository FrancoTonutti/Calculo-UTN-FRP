from panda3d.core import NodePath, PandaNode
from direct.showbase.ShowBase import ShowBase
from panda3d.core import LVecBase4
from pandac.PandaModules import Texture, TextureStage
from panda3d.core import Shader

class ShaderControlCG:
    def __init__(self, panda3d):
        # Inicialización de variables
        self.winsize = [0, 0]
        self.panda3d = panda3d
        sha_normal = "data/shaders/normalGen.sha"
        sha_depth = "data/shaders/depthGen.sha"
        sha_color = "data/shaders/colorGen.sha"
        sha_ink = "data/shaders/inkGen.sha"

        self.normal_buff, self.normal_cam = self.make_buffer("normalsBuffer", sha_normal, 0.5)
        # self.depth_buff, self.depth_cam = self.make_buffer("depthBuffer", sha_depth, 0.5)
        self.color_buff, self.color_cam = self.make_buffer("colorsBuffer", sha_color, 0.5)

        tex_normal = self.normal_buff.getTextureCard()
        # tex_depth = self.depth_buff.getTextureCard()
        tex_color = self.color_buff.getTextureCard()

        tex_normal.setTransparency(1)
        tex_normal.setColor(1, 1, 1, 1)
        tex_normal.reparentTo(self.panda3d.render2d)


        stage_border = TextureStage("border")
        stage_border.setSort(1)
        # tex_normal.setTexture(stage_border, tex_color.getTexture())

        # stage_depth = TextureStage("depth")
        # stage_depth.setSort(2)
        # tex_normal.setTexture(stage_depth, tex_depth.getTexture())

        shader_ink = self.panda3d.loader.loadShader(sha_ink)
        #tex_normal.setShader(shader_ink)

        width = self.panda3d.win.getXSize()
        height = self.panda3d.win.getYSize()

        tex_normal.setShaderInput("screen", width, height)
        self.tex_normal = tex_normal

    def make_buffer(self, name: str, shader_path:str, clear_color=0.0):
        buffer = self.panda3d.win.makeTextureBuffer(name, 0, 0)
        color = LVecBase4(clear_color)
        buffer.setClearColor(color)
        camera_lens = self.panda3d.cam.node().getLens()
        camera = self.panda3d.makeCamera(buffer, lens=camera_lens)
        camera.node().setScene(self.panda3d.render)
        temp_node = NodePath(PandaNode("node "+name))
        shader = self.panda3d.loader.loadShader(shader_path)
        temp_node.setShader(shader)
        temp_node.setShaderInput("showborders", LVecBase4(1))
        temp_node.setShaderInput("colorborders", LVecBase4(0, 0, 0, 1))
        camera.node().setInitialState(temp_node.getState())

        return buffer, camera

    def update_cameras(self, lens):
        self.normal_cam.node().setLens(lens)
        # self.depth_cam.setLens(lens)
        self.color_cam.node().setLens(lens)

        width = self.panda3d.win.getXSize()
        height = self.panda3d.win.getYSize()
        self.tex_normal.setShaderInput("screen", width, height)


class ShaderControlGLSL:
    def __init__(self, panda3d):
        # Inicialización de variables
        self.winsize = [0, 0]
        self.panda3d = panda3d
        sha_depthnormal_path = "data/shaders/GLSL/normal_depth"
        sha_outline_path = "data/shaders/GLSL/outline"

        self.normal_buff, self.normal_cam = self.make_buffer("normal_depthBuffer", sha_depthnormal_path, 0.5)
        # self.depth_buff, self.depth_cam = self.make_buffer("depthBuffer", sha_depth, 0.5)
        # self.color_buff, self.color_cam = self.make_buffer("colorsBuffer", sha_color, 0.5)

        tex_normal = self.normal_buff.getTextureCard()
        # tex_depth = self.depth_buff.getTextureCard()
        # tex_color = self.color_buff.getTextureCard()

        tex_normal.setTransparency(1)
        tex_normal.setColor(1, 1, 1, 1)
        tex_normal.reparentTo(self.panda3d.render2d)


        # stage_border = TextureStage("border")
        # stage_border.setSort(1)
        # tex_normal.setTexture(stage_border, tex_color.getTexture())

        # stage_depth = TextureStage("depth")
        # stage_depth.setSort(2)
        # tex_normal.setTexture(stage_depth, tex_depth.getTexture())
        shader_outline = Shader.load(Shader.SL_GLSL,
                                     vertex=sha_outline_path + ".vert",
                                     fragment=sha_outline_path + ".frag")

        tex_normal.setShader(shader_outline)

        width = self.panda3d.win.getXSize()
        height = self.panda3d.win.getYSize()

        tex_normal.setShaderInput("resolution", width, height)
        self.tex_normal = tex_normal

    def make_buffer(self, name: str, shader_path:str, clear_color=0.0):
        buffer = self.panda3d.win.makeTextureBuffer(name, 0, 0)
        color = LVecBase4(clear_color)
        buffer.setClearColor(color)
        camera_lens = self.panda3d.cam.node().getLens()
        camera = self.panda3d.makeCamera(buffer, lens=camera_lens)
        camera.node().setScene(self.panda3d.render)
        temp_node = NodePath(PandaNode("node "+name))
        #shader = self.panda3d.loader.loadShader(shader_path)
        shader = Shader.load(Shader.SL_GLSL,
                             vertex=shader_path + ".vert",
                             fragment=shader_path + ".frag")
        temp_node.setShader(shader)
        temp_node.setShaderInput("showborders", LVecBase4(1))
        temp_node.setShaderInput("colorborders", LVecBase4(0, 0, 0, 1))
        camera.node().setInitialState(temp_node.getState())

        return buffer, camera

    def update_camera_lens(self, lens):
        self.normal_cam.node().setLens(lens)
        # self.depth_cam.setLens(lens)
        # self.color_cam.node().setLens(lens)

        width = self.panda3d.win.getXSize()
        height = self.panda3d.win.getYSize()
        self.tex_normal.setShaderInput("screen", width, height)


def add_shadders(self: ShowBase):

    normalsBuffer = self.win.makeTextureBuffer("normalsBuffer", 0, 0)
    normalsBuffer.setClearColor(LVecBase4(0.5, 0.5, 0.5, 0.5))
    self.normalsBuffer = normalsBuffer
    normalsCamera = self.makeCamera(
        normalsBuffer, lens=self.cam.node().getLens())
    normalsCamera.node().setScene(self.render)
    tempnode = NodePath(PandaNode("temp node"))
    normalGen = self.loader.loadShader("app/view/shaders/normalGen.sha")
    tempnode.setShader(normalGen)
    tempnode.setShaderInput("showborders", LVecBase4(1))
    normalsCamera.node().setInitialState(tempnode.getState())

    depth_buffer = self.win.makeTextureBuffer("depthBuffer", 0, 0)
    depth_buffer.setClearColor(LVecBase4(0, 0, 0, 0))
    self.depth_buffer = depth_buffer
    depth_camera = self.makeCamera(
        depth_buffer, lens=self.cam.node().getLens())

    depth_camera.node().setScene(self.render)
    tempnode = NodePath(PandaNode("temp node depth"))
    depth_gen = self.loader.loadShader("app/view/shaders/depthGen.sha")
    tempnode.setShader(depth_gen)
    depth_camera.node().setInitialState(tempnode.getState())




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
    depthTex = depth_buffer.getTextureCard()

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

    stage_border = TextureStage("border")
    stage_border.setSort(1)
    drawnScene.setTexture(stage_border, colorBorderTex.getTexture())

    stage_depth = TextureStage("depth")
    stage_depth.setSort(2)
    drawnScene.setTexture(stage_depth, depthTex.getTexture())


    drawnScene.setShader(inkGen)

    drawnScene.setShaderInput("separation", LVecBase4(self.separation, 0, self.separation, 0))

    drawnScene.setShaderInput("screen", 1280,720)
    drawnScene.setShaderInput("cutoff", LVecBase4(self.cutoff))

    print("SHADER DEBUG")

    print(drawnScene.findAllTextureStages())
