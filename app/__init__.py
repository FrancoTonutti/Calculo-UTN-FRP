from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.view.interface.console_ui import ConsoleUI

from direct.showbase.ShowBase import ShowBase
from typing import Type, Union
from direct.gui.DirectEntry import *


PandaApp = Union[Type[ShowBase], None]


class App:
    def __init__(self):
        self.base: PandaApp = None
        self.gui_objects = dict()
        self.workspace_active = True
        self.mouse_on_workspace = False

        # Define el plano de trabajo y la ubicación del mouse en el modelo
        self.work_plane_vect = (0, 1, 0)
        self.work_plane_point = (0, 0, 0)
        self.work_plane_mouse = (0, 0, 0)

        # Creamos una variable que almacenará el registro de todos los elementos del modelo
        self.model_reg = dict()
        self.console_input: Union[DirectEntry, None] = None
        self.console: ConsoleUI = None

        self.commands = dict()
        self.cursor = None

        self.main_ui = None

    def set_show_base(self, base):
        self.base = base
        # Crea un objeto cursor que se ubica en un punto del espacio relativo a la cámara, según la posición del cursor
        # en la ventana, será usado para determinar la ubicación del mouse dentro del espacio de trabajo
        self.cursor = self.base.render.attach_new_node("cursor_pos")
        scale = 0.1
        self.cursor.setScale(scale, scale, scale)
        self.cursor.setPos(0, 10, 0)
        self.cursor.reparentTo(self.base.camera)

    def get_show_base(self) -> PandaApp:
        return self.base

    def add_gui_region(self, name: str, direct_gui_object) -> None:
        self.gui_objects.update({name: direct_gui_object})


app = App()


def get_running_app():
    return app
