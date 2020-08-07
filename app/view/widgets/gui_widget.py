from app import app
from app.view import draw
from panda3d.core import TextProperties

class GuiWidget:
    def __init__(self):
        self.initialized = False

    def mergeoptions(self, optiondefs):
        optiondefs_base = (
            # Define type of DirectGuiWidget
            ('frameColor', (0, 0, 0, 1), self.setFrameColor),
            ('colorString', "C_CONCRETE", self.setColorString),
            ('position', [0, 0], self.setPosition),
            ('orginV', "top", self.setPosition),
            ('orginH', "left", self.setPosition),
            ('alpha', 255, self.setColorString),
            ('size', None, self.set_size),
            ('textCenterX', True, None),
            ('textCenterY', True, None),
            ('align', "left", self.set_align)

        )

        name_list = list()
        for name, default, function in optiondefs:
            name_list.append(name)

        for name, default, function in optiondefs_base:

            if name not in name_list:
                print("mergeoptions", name)
                optiondefs += ((name, default, function),)

        return optiondefs

    def setColorString(self):
        col = draw.get_color(self["colorString"], color_format="rgba", alpha=self["alpha"])
        print(col)
        self["frameColor"] = col

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

    def set_size(self):

        if self["size"] is not None:
            width, height = self["size"]
            self["frameSize"] = (0, width, -height, 0)

            if self.initialized and hasattr(self, "onscreenText"):
                txt_x, txt_y = self["text_pos"]
                size_x, size_y = self["text_scale"]
                if self["textCenterX"]:
                    txt_x = width/2
                if self["textCenterY"]:
                    txt_y = 0#+(height/2 + size_y/2)
                self["text_pos"] = (txt_x, txt_y)

    def set_align(self):
        if hasattr(self, "onscreenText"):
            if self["align"] is "left":
                self["text_align"] = TextProperties.A_left
            elif self["align"] is "center":
                self["text_align"] = TextProperties.A_center
            elif self["align"] is "right":
                self["text_align"] = TextProperties.A_right


