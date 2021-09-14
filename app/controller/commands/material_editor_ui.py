from direct.gui import DirectGuiGlobals as DGG

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
from app.model import MaterialGroup, Material


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

        create_label("Materiales", frame, padding=[10, 0, 0, 0], margin=[0, 0, 0, 10])
        content  = SimpleFrame(
            parent=frame,
            sizeHint=[1, 1],
            layout="BoxLayout",
            layoutDir="Y",
            margin=[10, 10, 0, 0],
            alpha=0
        )

        btn_container = SimpleFrame(
            parent=content,
            sizeHint=[1, None],
            size=[None, 25],
            layout="BoxLayout",
            layoutDir="X",
            alpha=0,
            margin=[0,0,10,10]
        )

        btn1 = new_button("Agregar Material", parent=btn_container,
                          command=self.create_material_group)
        btn2 = new_button("Agregar Clase", parent=btn_container,
                          command=self.create_material_group, margin=[10, 0, 0, 0])

        btn2['state'] = DGG.DISABLED

        self.col1 = SimpleScrolledFrame(position=[0, 0],
                                        canvasSize=(0, 100, -200, 0),
                                        size=[250, None],
                                        sizeHint=[0.25, 0.9],
                                        parent=content,
                                        frameColor=scheme_rgba(
                                            COLOR_SEC_DARK),
                                        alpha=1,
                                        padding=[0, 1, 0, 0],
                                        layout="GridLayout",
                                        layoutDir="X",
                                        gridCols=1,
                                        gridRows=10)

        self.material_list_btns = []

        self.selected_group = None

        self.update_list()

    def update_list(self):

        for btn in self.material_list_btns:
            btn.destroy()

        self.material_list_btns.clear()

        model_reg = app.model_reg
        entities = model_reg.find_entities("MaterialGroup")

        self.selected_group = None

        for group in entities:
            if self.selected_group is None:
                self.selected_group = group

            btn = new_button(group.name, parent=self.col1.canvas,
                             command=self.open_group, args=[group])
            self.material_list_btns.append(btn)

        execute("regen_ui")

    def open_group(self, group):
        pass

    def create_material_group(self):
        mg = MaterialGroup("Material")

        self.update_list()
