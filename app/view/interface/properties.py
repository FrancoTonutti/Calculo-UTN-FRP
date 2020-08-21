from app import app
from .layout_controller import Layout
from direct.showbase.DirectObject import DirectObject
from app.controller.console import execute

class PropertiesEditor(DirectObject):
    def __init__(self, layout: Layout):
        self.frame = layout.prop_frame
        self.container = layout.work_container
        self.accept("control-1", self.toogle_show)

    def toogle_show(self):
        if self.frame.is_hidden():
            self.frame["size"] = [250, 500]
            self.frame.show()
        else:
            self.frame.hide()
            self.frame["size"] = [0, 500]

        execute("regen_ui")
