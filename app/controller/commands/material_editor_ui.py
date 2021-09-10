from app.controller.console import command, execute
from app.controller.commands import render
from app import app
import numpy as np
from panda3d.core import LineSegs, NodePath
from app.view import draw
from app.view.interface.color_scheme import *

from app.view.interface.tools import *

__tab_title__ = "Editor de materiales"

from app.view.simpleui import SimpleFrame


@command("material_editor")
def section_editor():
    tab_manager = app.main_ui.tab_manager

    index = 0
    for tab in tab_manager.tabs:

        if tab.title == __tab_title__:
            tab_manager.set_active_tab(index)
            return None
        index += 1

    new_tab = tab_manager.create_new_tab(__tab_title__)
    frame = new_tab.frame
    frame["frameColor"] = scheme_rgba(COLOR_SEC_LIGHT)
    frame["layoutDir"] = "Y"

    UI(frame)

class UI:
    def __init__(self, frame):

        create_label("Materiales", frame, padding=[30, 0, 20, 0])
        btn_bar  = SimpleFrame(
            parent=frame,
            sizeHint=[1, 1],
            alpha=0,
            layout="BoxLayout",
            layoutDir="X",
            padding=[10, 10, 10, 10]
        )

        btn_bar.setFrameColor()

        btn1 = new_button("Agregar Material", parent=btn_bar,
                          command=self.create_profile)
        btn1 = new_button("Agregar Clase", parent=btn_bar,
                          command=self.create_profile)


        execute("regen_ui")

    def create_profile(self):
        pass