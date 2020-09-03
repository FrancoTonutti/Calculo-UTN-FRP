from direct.gui.DirectFrame import *
from direct.gui.DirectButton import *
from direct.gui import DirectGuiGlobals as DGG

"""
Esto es un archivo de testeo de ejemplo, no funciona actualmente

"""


class Frame(DirectFrame):
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
        )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        if parent is None:
            parent = pixel2d

        DirectFrame.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(Frame)


class CustomButton(DirectButton, Frame):
    def __init__(self, parent=None, **kw):
        self.textures = ()
        self.initialized = False
        optiondefs = (
            # Define type of DirectGuiWidget
            ('relief', DGG.FLAT, None),
        )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        if parent is None:
            parent = pixel2d

        DirectButton.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(CustomButton)