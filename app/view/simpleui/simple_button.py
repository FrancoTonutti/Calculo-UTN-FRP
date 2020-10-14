from direct.gui.DirectButton import *
from direct.gui.DirectLabel import *
from app.view.simpleui.simple_frame import SimpleFrame
from app.view import draw
from panda3d.core import TextProperties
from direct.gui.DirectButton import *

class SimpleButton(DirectButton, SimpleFrame):
    def __init__(self, parent=None, **kw):
        self.initialized = False
        optiondefs = (
            # Define type of DirectGuiWidget
            ('command',        None,       None),
        )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        if parent is None:
            parent = pixel2d

        DirectButton.__init__(self, parent)
        SimpleFrame.__init__(self, parent, override_default=True)

        # Call option initialization function
        self.initialiseoptions(SimpleButton)
        self.set_position()

        self.initialized = True
        self.set_size()
        #self.setPythonTag('simple_gui', self)