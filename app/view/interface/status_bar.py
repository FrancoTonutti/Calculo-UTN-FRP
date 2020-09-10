from app import app
from .layout_controller import Layout
from direct.showbase.DirectObject import DirectObject
from app.controller.console import execute
from app.view.simpleui.simple_entry import SimpleEntry
from app.view.simpleui.simple_label import SimpleLabel
from app.view.simpleui.simple_scrolled_frame import SimpleScrolledFrame
from panda3d.core import TextNode
from panda3d.core import WindowProperties
from direct.gui.DirectScrolledFrame import *


def execute_console(cmd):
    print(cmd)


class StatusBar(DirectObject):
    def __init__(self, layout: Layout):
        super().__init__()
        self.frame = layout.status_bar_frame
        self.entity_info = None

        self.info_label = SimpleLabel(parent=self.frame,
                                      text="Prueba",
                                      alpha=0,
                                      frameColor="C_WHITE",
                                      align="left",
                                      textCenterX=False)

    def entity_read(self, entity=None):

        if self.entity_info != entity:

            if self.entity_info and self.entity_info.geom:
                self.entity_info.geom.setRenderModeFilled(1)

            self.entity_info = entity
            if entity is not None:
                if self.entity_info.geom:
                    c_black = (0, 0, 0, 1)
                    self.entity_info.geom.setRenderModeFilledWireframe(c_black, 1)
                    self.entity_info.geom.setRenderModeThickness(3)

            if entity is not None:
                self.info_label.setText(str(entity))
            else:
                self.info_label.setText("")
