from panda3d.core import *
from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectFrame import *
from direct.showbase.DirectObject import DirectObject
#from direct.gui import DirectFrame, DirectButton
from direct.showbase import ShowBaseGlobal
from app.view import draw
from app import app

class Frame(DirectFrame, DirectObject):
    """
    Crea un Frame que abarca el ancho de la pantalla

    Argumentos

    colorString -- Nombre del color para el marco (default: "C_CONCRETE")
    position -- Lista con las alturas inicial y final del marco, desde arriba hacia abajo (default: [0, 10])
    Ademas todos los parametros heredados de DirectFrame
    """

    def __init__(self, parent=None, **kw):
        self.textures = ()
        optiondefs = (
            # Define type of DirectGuiWidget
            ('frameColor', (1, 0, 0, 1), self.setFrameColor),
            ('colorString', "C_CONCRETE", self.setColorString),
            ('position', [0, 10], self.setPosition),
            ('orginV', "top", self.setPosition),
            ('orginH', "left", self.setPosition),
            ('alpha', 255, self.setColorString)
        )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        if parent is None:
            parent = pixel2d

        DirectFrame.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(Frame)
        self.setPosition()
        size = self['frameSize']
        self.setPos(-size[0], 0, -size[3])
        self.flattenLight()
        self.setPosition()

        self.accept('aspectRatioChanged', self.setPosition)

    def setPosition(self):
        if self.parent == pixel2d:
            frame_width = app.get_show_base().win.getXSize()
            frame_height = app.get_show_base().win.getYSize()

        else:
            size = self.parent["frameSize"]
            if size is not None:
                frame_width = size[1] - size[0]
                frame_height = size[3] - size[2]
            else:
                frame_width = 0
                frame_height = 0

        x0, y0 = 0, 0
        x, y = self["position"]

        if self["orginH"] is "left":
            x0 = 0
        elif self["orginH"] is "center":
            x0 = frame_width / 2
        elif self["orginH"] is "right":
            x0 = frame_width

        if self["orginV"] is "top":
            y0 = 0
        elif self["orginV"] is "middle":
            y0 = -frame_height / 2
        elif self["orginV"] is "bottom":
            y0 = -frame_height

        self.setPos(x0 + x, 0, y0 - y)
        # height = h2-h1
        # self["frameSize"] = (0, win_width, 0, -height)

    def setColorString(self):
        col = draw.get_color(self["colorString"], color_format="rgba", alpha=self["alpha"])
        print(col)
        self["frameColor"] = col


