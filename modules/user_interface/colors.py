"""
Colors from http://materialuicolors.co/?utm_source=launchers
"""


def rgb(r, g, b):

    col = [r/255, g/255, b/255]
    return col


class PaletteColor:

    def __init__(self):

        self.color_title_bar = rgb(30, 136, 229)  # Blue 600
        self.color_title_bar_light = rgb(33, 150, 243)  # Blue 500
        self.color_options_bar = rgb(250, 250, 250)  # Grey 50

        #self.color_title_bar = rgb(255, 255, 255)  # Blue 600
        #self.color_title_bar_light = rgb(240, 240, 240)  # Blue 500

    def get_rgba(self, name):
        col = getattr(self, name).copy()

        if col is None:
            col = [1, 0, 0, 1]

        if len(col) is 3:
            col.append(1)
        return col
