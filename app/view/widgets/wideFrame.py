from panda3d.core import *
from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectFrame import *
from direct.showbase.DirectObject import DirectObject
#from direct.gui import DirectFrame, DirectButton
from direct.showbase import ShowBaseGlobal
from app.view import draw
from app import app

class WideFrame(DirectFrame, DirectObject):
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
        )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        if parent is None:
            parent = pixel2d

        DirectFrame.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(WideFrame)
        self.setPosition()
        size = self['frameSize']
        self.setPos(-size[0], 0, -size[3])
        self.flattenLight()
        self.setPosition()

        self.accept('aspectRatioChanged', self.setPosition)

    def setPosition(self):
        win_width = app.get_show_base().win.getXSize()
        win_height = app.get_show_base().win.getYSize()

        h1, h2 = self["position"]
        if self["orginV"] is "top":
            self.setPos(0, 0, -h1)
        elif self["orginV"] is "middle":
            self.setPos(0, 0, -win_height/2 - h1)
        elif self["orginV"] is "bottom":
            self.setPos(0, 0, -win_height - h1)

        height = h2-h1
        self["frameSize"] = (0, win_width, 0, -height)

    def setColorString(self):
        col = draw.get_color(self["colorString"], color_format="rgba")
        print(col)
        self["frameColor"] = col


