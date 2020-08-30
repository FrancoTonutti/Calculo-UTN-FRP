from direct.gui.DirectScrolledFrame import *
from app.view.simpleui.simple_frame import SimpleFrame
from app.view import draw
from panda3d.core import TextProperties


class SimpleScrolledFrame(DirectScrolledFrame, SimpleFrame):
    def __init__(self, parent=None, **kw):
        self.initialized = False
        optiondefs = (
            # Define type of DirectGuiWidget
            ('autoHideScrollBars', 1, self.setAutoHideScrollBars),
            ('scrollBarWidth', 16, self.setScrollBarWidth),
            ('borderWidth', (1, 1), self.setBorderWidth),
        )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        if parent is None:
            parent = pixel2d

        DirectScrolledFrame.__init__(self, parent)
        SimpleFrame.__init__(self, parent, override_default=True)

        self["text_font"] = draw.draw_get_font()[0]

        # Call option initialization function
        self.initialiseoptions(SimpleScrolledFrame)
        self.set_position()

        self.initialized = True
        self.set_size()

        canvas = self.getCanvas()
        canvas.setPythonTag('simple_gui', self)
