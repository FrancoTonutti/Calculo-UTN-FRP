from panda3d.core import *
from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectButton import *
#from direct.gui import DirectFrame, DirectButton
from direct.showbase import ShowBaseGlobal
from app.view import draw
from app.view.simpleui import window

class CustomButton(DirectButton):
    def __init__(self, parent=None, **kw):
        self.textures = ()
        self.initialized = False
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

        # Call option initialization functions
        self.initialiseoptions(CustomButton)
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

    def on_leave(self, event):
        #draw.change_cursor("/c/Windows/Cursors/aero_arrow.cur")
        #draw.change_cursor("/d/Bibliotecas/Documentos/Python 3/UTN/Calculo-UTN-FRP/data/cursors/arrow.cur")
        window.set_cursor(window.cr_arrow)

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

    def set_size(self):
        width, height = self["size"]
        self["frameSize"] = (0, width, -height, 0)

        if self.initialized:
            txt_x, txt_y = self["text_pos"]
            size_x, size_y = self["text_scale"]
            if self["textCenterX"]:
                txt_x = width/2
            if self["textCenterY"]:
                txt_y = -(height/2 + size_y/2)
            self["text_pos"] = (txt_x, txt_y)


def new_button(text, x, y, colors=None, command=None, args=None, parent=None, size=None):
    if args is None:
        args = []
    font_panda3d, font_pil = draw.draw_get_font()
    if colors is None:
        col_rollover = draw.merge_color("C_NEPHRITIS", "C_WHITE", 0.2)
        colors = ["C_NEPHRITIS", "C_WHITE", col_rollover, "C_CONCRETE"]
    if size is None:
        width = font_pil.getsize(text)[0] + 20
        size = [width, 20]

    btn = CustomButton(text=text,
                       text_scale=(12, 12),
                       text_font=font_panda3d,
                       command=command,
                       parent=parent,
                       extraArgs=args,
                       colorList=colors,
                       position=[x, y],
                       size=size
                       )

    return btn

