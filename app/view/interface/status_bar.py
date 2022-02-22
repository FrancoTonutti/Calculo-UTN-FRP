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
from app.view.interface.color_scheme import *
from .. import draw, simpleui


def execute_console(cmd):
    print(cmd)


class StatusBar(DirectObject):
    def __init__(self, layout: Layout):
        super().__init__()
        self.frame = layout.status_bar_frame
        self.entity_info = None
        self._status_hint = ""

        self.command_info = SimpleLabel(
            text_fg=draw.get_color(COLOR_TEXT_LIGHT, "rgba"),
            parent=self.frame,
            text="",
            alpha=1,
            frameColor=scheme_rgba(COLOR_HIGHLIGHT),
            align="left",
            textCenterX=False,
            padding=[10,0,0,0],
            size=[None, None],
            sizeHint=[None, True])

        self.command_info.hide()

        self.info_label = SimpleLabel(text_fg=draw.get_color(COLOR_TEXT_LIGHT, "rgba"),
                                      parent=self.frame,
                                      text="",
                                      alpha=0,
                                      frameColor="C_WHITE",
                                      align="left",
                                      textCenterX=False,
                                      padding=[10,0,0,0],)

    def command_start(self, name):

        font_panda3d, font_pil = draw.draw_get_font(font_size=12)
        width, height = font_pil.getsize(name)
        self.command_info["text"] = name
        self.command_info["size"] = [10+width+10, None]
        self.command_info.show()
        simpleui.update_ui()

    def command_ended(self):
        self.command_info["size"] = [None, None]
        self.command_info.hide()
        simpleui.update_ui()


    def set_status_hint(self, hint):
        self._status_hint = hint

        if self.entity_info is None:
            self.info_label.setText(self._status_hint)

    def entity_read(self, entity=None):
        # Revisa que la entidad leída haya cambiado
        if self.entity_info != entity:
            c_black = (0, 0, 0, 1)
            # Si cambió la entidad señalada por el cursor se resetea la visualización de la la entidad anterior
            if self.entity_info and not self.entity_info.is_selected and self.entity_info.geom:
                for geom in self.entity_info.geom:
                    if geom:
                        if "render/lines" in str(geom):
                            #geom.setRenderModeThickness(3)
                            geom.setRenderModeFilled(1)
                            color = geom.getPythonTag('defcolor')

                            geom.setColorScale(color)
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
                            #geom.setRenderModeThickness(20)

                            color = draw.get_color(draw.C_NEPHRITIS,
                                                   color_format="rgba",
                                                   alpha=1)
                            geom.setColorScale(color)

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
                self.info_label.setText(self._status_hint)
