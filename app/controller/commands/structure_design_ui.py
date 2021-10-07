from app.model import Load
from direct.task.Task import TaskManager
from app import app

from panda3d.core import LineSegs, NodePath
import numpy as np

from app.controller.console import command, execute
from app.model.load_combination import LoadCombination
from app.view.interface.color_scheme import *
from app.view.simpleui import SimpleScrolledFrame, SimpleLabel, SimpleButton, \
    SimpleCheckBox, SimpleEntry, SimpleFrame

from app.model.load_type import LoadType
from app.view import simpleui

from app.model.code_checks.code_check_CIRSOC_201 import CodeCheckCIRSOC201

from app.view.interface.tools import *

class UI:
    def __init__(self, frame):
        model_reg = app.model_reg
        entities = model_reg.find_entities("CodeCheckCIRSOC201")
        if entities:
            self.code_check = entities[0]
        else:
            self.code_check = CodeCheckCIRSOC201()


        create_label("Dimensionado", frame, padding=[10, 0, 0, 0],
                     margin=[0, 0, 0, 10])

        content = SimpleFrame(
            parent=frame,
            sizeHint=[1, 1],
            layout="BoxLayout",
            layoutDir="Y",
            margin=[10, 10, 35, 0],
            alpha=0
        )
        create_label("Seleccione una barra", content)

        columns_container = SimpleFrame(
            parent=content,
            sizeHint=[None, None],
            size=[None, None],
            layout="BoxLayout",
            layoutDir="X",
            alpha=0,
            margin=[0, 0, 10, 10]
        )

        execute("regen_ui")

        self.col1 = SimpleScrolledFrame(position=[0, 0],
                    canvasSize=(0, 100, -200, 0),
                    size=[250, None],
                    sizeHint=[0.25, 1],
                    parent=columns_container,
                    frameColor=scheme_rgba(COLOR_SEC_LIGHT),
                    alpha=1,
                    padding=[0, 1, 0, 0],
                    layout="GridLayout",
                    layoutDir="X",
                    gridCols=1,
                    gridRows=10)

        self.col2 = SimpleFrame(position=[0, 0],
                    sizeHint=[0.75, 1],
                    parent=columns_container,
                    frameColor=scheme_rgba(COLOR_SEC_LIGHT),
                    padding=[1, 0, 0, 0],
                    alpha=1,
                    layout="BoxLayout",
                    layoutDir="Y")

        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("Bar")

        self.title = create_label("Seleccione una barra", self.col2, padding=[0,0,0,0])

        self.selected_bar = None
        self.bar_list_buttons = list()



        for bar in entities:
            if self.selected_bar is None:
                self.selected_bar = bar

            btn = new_button(str(bar), parent=self.col1.canvas, command=self.explore_bar, args=[bar])
            self.bar_list_buttons.append(btn)



        model = []

        execute("regen_ui")
        self.log_label = create_label("LOG", self.col2, margin=[0,0,20,20])

        self.explore_bar(self.selected_bar)

        execute("regen_ui")

    def update(self):

        for btn in self.bar_list_buttons:
            btn.destroy()
        self.bar_list_buttons.clear()

        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("Bar")

        self.selected_bar = None

        for bar in entities:
            if self.selected_bar is None:
                self.selected_bar = bar

            btn = new_button(str(bar), parent=self.col1.canvas,
                             command=self.explore_bar, args=[bar])
            self.bar_list_buttons.append(btn)

        self.explore_bar(self.selected_bar)

        execute("regen_ui")

    def explore_bar(self, bar_entity):
        if bar_entity:
            self.selected_bar = bar_entity

            self.title["text"] = str(bar_entity)

            if self.selected_bar.behavior == "Viga":
                self.log_label["text"] = self.code_check.verify_beam(self.selected_bar)
            else:
                self.log_label["text"] = self.code_check.verify_column(self.selected_bar)




@command(name="view_design")
def view_results():
    tab_manager = app.main_ui.tab_manager

    index = 0
    for tab in tab_manager.tabs:

        if tab.title == "Dimensionado":
            tab_manager.set_active_tab(index)
            return None
        index += 1

    new_tab = tab_manager.create_new_tab("Dimensionado")
    frame = new_tab.frame
    #frame["frameColor"] = scheme_rgba(COLOR_SEC_LIGHT)
    frame["layoutDir"] = "Y"

    ui = UI(frame)
    new_tab.ev_focus_in = ui.update
