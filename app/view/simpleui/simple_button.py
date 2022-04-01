from direct.gui.DirectButton import *
from direct.gui.DirectLabel import *
from app.view.simpleui.simple_frame import SimpleFrame
from app.view import draw
from panda3d.core import TextProperties
from direct.gui.DirectButton import *
from app.view.simpleui import window

from panda3d.core import *
from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectButton import *
#from direct.gui import DirectFrame, DirectButton
from direct.showbase import ShowBaseGlobal
from app.view import draw
from app.view.simpleui import window


class SimpleButton(DirectButton, SimpleFrame):
    def __init__(self, parent=None, override_default=True, **kw):
        self.textures = ()
        self.initialized = False
        self.is_rollover = False
        optiondefs = (
            # Define type of DirectGuiWidget
            ('relief', DGG.FLAT, None),
            ('frameColor', (1, 1, 1, 1), self.setFrameColor),
            ('colorList', None, self.setColorNames),
            # Sounds to be used for button events
            ('rolloverSound', None, self.setRolloverSound),
            ('clickSound', None, self.setClickSound),
            # Can only be specified at time of widget contruction
            # Do the text/graphics appear to move when the button is clicked
            ('pressEffect', None, DGG.INITOPT),
            ('position', [0, 0], self.setPosition),
            ('size', [None, None], self.set_size),
            ('textCenterX', True, None),
            ('textCenterY', True, None)

        )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        if parent is None:
            parent = pixel2d

        DirectButton.__init__(self, parent)
        SimpleFrame.__init__(self, parent, override_default=override_default)
        # Call option initialization functions
        self.initialiseoptions(SimpleButton)
        self.initialized = True
        size = self['frameSize']
        #self.setPos(-size[0], 0, -size[3])
        self.setPos(0, 0, 0)
        self.flattenLight()
        self.setPosition()
        self.set_size()

        self.bind(DGG.ENTER, self.on_enter)
        self.bind(DGG.EXIT, self.on_leave)

    def on_enter(self, event):
        #draw.change_cursor("/c/Windows/Cursors/no_rm.cur")
        #draw.change_cursor("/d/Bibliotecas/Documentos/Python 3/UTN/Calculo-UTN-FRP/data/cursors/cursor-link.cur")
        #draw.change_cursor("data/cursors/link.cur")
        window.set_cursor(window.cr_link)
        self.is_rollover = True

    def on_leave(self, event):
        #draw.change_cursor("/c/Windows/Cursors/aero_arrow.cur")
        #draw.change_cursor("/d/Bibliotecas/Documentos/Python 3/UTN/Calculo-UTN-FRP/data/cursors/arrow.cur")
        window.set_cursor(window.cr_arrow)
        self.is_rollover = False

    def get_extra_args(self):
        return self["extraArgs"]

    def setColorNames(self):
        if self["colorList"] is not None:
            self.textures = ()
            if len(self["colorList"]) == 2:
                self["colorList"].append(draw.merge_color(self["colorList"][0], self["colorList"][1],0.7))
                self["colorList"].append("C_CONCRETE")

            for color_name in self["colorList"]:
                color = draw.get_color(color_name)
                img = PNMImage(1, 1)
                img.fillVal(color[0], color[1], color[2])
                tex = Texture("test")
                tex.load(img)
                self.textures += tex,
            if self.textures is not ():
                self["frameTexture"] = self.textures
        else:
            self["frameTexture"] = None

    def setPosition(self):
        x, y = self["position"]
        self.setPos(x, 0, -y)



        """def set_size(self):
            # width, height = self["size"]
            pad = self["padding"]
            pad_x = pad[0] + pad[1]
            pad_y = pad[2] + pad[3]
    
            #width, height = self.box_size()
    
            width, height = self["size"]
            #width = max(width - pad_x, 0)
            #height = max(height - pad_y, 0)
            self["frameSize"] = (0, width, -height, 0)
    
    
            if self.initialized:
                txt_x, txt_y = self["text_pos"]
                size_x, size_y = self["text_scale"]
                if self["textCenterX"]:
                    txt_x = width/2
                if self["textCenterY"]:
                    txt_y = -(height/2 + size_y/2)
                self["text_pos"] = (txt_x, txt_y)"""

    def update_text_pos(self):
        if self.initialized:
            _, width, height, _ = self["frameSize"]
            height = -height

            txt_x, txt_y = self["text_pos"]
            size_x, size_y = self["text_scale"]
            if self["textCenterX"]:
                txt_x = width / 2
            if self["textCenterY"]:
                txt_y = -(height / 2 + size_y / 2)
            self["text_pos"] = (txt_x, txt_y)