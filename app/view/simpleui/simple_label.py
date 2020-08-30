from direct.gui.DirectLabel import *
from app.view.simpleui.simple_frame import SimpleFrame
from app.view import draw
from panda3d.core import TextProperties

class SimpleLabel(DirectLabel, SimpleFrame):
    def __init__(self, parent=None, **kw):
        self.initialized = False
        optiondefs = (
            # Define type of DirectGuiWidget
            ('label', "None", None),
            ('textCenterX', True, self.update_text_pos),
            ('textCenterY', True, self.update_text_pos),
            ('align', "center", self.set_align)
        )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        if parent is None:
            parent = pixel2d

        DirectLabel.__init__(self, parent)
        SimpleFrame.__init__(self, parent, override_default=True)

        self["text_font"] = draw.draw_get_font()[0]

        # Call option initialization function
        self.initialiseoptions(SimpleLabel)
        self.set_position()

        self.initialized = True
        self.set_size()

    def update_text_pos(self):

        if self.initialized:
            width, height = self.box_size()

            txt_x, txt_y = self["text_pos"]
            size_x, size_y = self["text_scale"]
            if self["textCenterX"]:
                txt_x = width / 2
            if self["textCenterY"]:
                txt_y = -(height / 2 + size_y / 2)
            self["text_pos"] = (txt_x, txt_y)

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
