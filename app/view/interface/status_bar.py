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

from .. import draw


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
        # Revisa que la entidad leída haya cambiado
        if self.entity_info != entity:
            c_black = (0, 0, 0, 1)
            # Si cambió la entidad señalada por el cursor se resetea la visualización de la la entidad anterior
            if self.entity_info and not self.entity_info.is_selected and self.entity_info.geom:
                for geom in self.entity_info.geom:
                    if geom:
                        if "render/lines" in str(geom):
                            geom.setRenderModeThickness(3)
                            geom.setRenderModeFilled(1)
                        else:
                            pass
                            # geom.setRenderModeFilled(1)
                            geom.setTextureOff(0)
                            geom.setColorScale(1, 1, 1, 1)

            # Se cambia la visualización de la nueva entidad
            self.entity_info = entity
            if self.entity_info and not self.entity_info.is_selected and self.entity_info.geom:

                for geom in self.entity_info.geom:
                    if geom:
                        if "render/lines" in str(geom):
                            geom.setRenderModeThickness(20)
                            geom.setRenderModeFilled(1)
                        else:
                            pass
                            geom.setTextureOff(1)
                            color = draw.get_color(draw.C_NEPHRITIS, color_format="rgba", alpha=0.2)
                            geom.setColorScale(color)
                            # geom.setRenderModeThickness(3)
                            #geom.setRenderModeFilledWireframe(c_black, 1)


            if entity is not None:
                self.info_label.setText(str(entity))
            else:
                self.info_label.setText("")
