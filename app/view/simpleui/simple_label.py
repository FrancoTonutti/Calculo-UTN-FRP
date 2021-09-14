from direct.gui import DirectGuiGlobals
from direct.gui.DirectLabel import *
from app.view.simpleui.simple_frame import SimpleFrame
from app.view.simpleui.simple_button import SimpleButton
from app.view import draw
from panda3d.core import TextProperties

class SimpleLabel(SimpleButton):
    """
    label = None
    textCenterX = True
    textCenterY = True
    align = "center"  # "left" or "right"
    fontSize = 12
    """
    def __init__(self, parent=None, **kw):
        self.initialized2 = False
        optiondefs = (
            # Define type of DirectGuiWidget
            ('label', "None", None),
            ('textCenterX', True, None),
            ('textCenterY', True, None),
            ('align', "center", self.set_align),
            ('fontSize', 12, self.set_font_size)
        )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        if parent is None:
            parent = pixel2d

        #DirectLabel.__init__(self, parent)
        SimpleButton.__init__(self, parent, override_default=True)

        self["text_font"] = draw.draw_get_font()[0]

        # Call option initialization function
        self.initialiseoptions(SimpleLabel)
        self.set_position()

        self.initialized2 = True
        self.set_size()
        self.set_font_size()

        self["state"] = DirectGuiGlobals.DISABLED

    def update_text_pos(self):

        if self.initialized2:

            _, width, height, _ = self["frameSize"]
            height = -height

            txt_x, txt_y = self["text_pos"]
            size_x, size_y = self["text_scale"]
            padding = self["padding"]

            if self["textCenterX"]:
                txt_x = width / 2
            if self["textCenterY"]:
                txt_y = -(height / 2 + size_y / 2)
            self["text_pos"] = (txt_x+padding[0], txt_y)

            if self["align"] is "left":
                self["text_align"] = TextProperties.A_left
            elif self["align"] is "center":
                self["text_align"] = TextProperties.A_center
            elif self["align"] is "right":
                self["text_align"] = TextProperties.A_right

    def set_align(self):

        if not self.initialized:
            if self["align"] is "left":
                self["text_align"] = TextProperties.A_left
            elif self["align"] is "center":
                self["text_align"] = TextProperties.A_center
            elif self["align"] is "right":
                self["text_align"] = TextProperties.A_right

    def set_font_size(self):
        size = int(self['fontSize'])
        self['text_scale'] = (size, size)
