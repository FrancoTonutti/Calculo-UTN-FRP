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

from app.view.interface.tools import *


class UI:
    def __init__(self, frame):

        create_label("Resultados", frame)

        columns_container = SimpleFrame(
            parent=frame,
            sizeHint=[1, 1],
            frameColor=scheme_rgba(COLOR_MAIN_DARK),
            alpha=1,
            layout="BoxLayout",
            layoutDir="X"
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

        self.col2 = SimpleScrolledFrame(position=[0, 0],
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

        for bar in entities:
            new_button(str(bar), parent=self.col1.canvas)

        execute("regen_ui")


@command(name="view_results", shortcut="b")
def view_results():
    tab_manager = app.main_ui.tab_manager

    index = 0
    for tab in tab_manager.tabs:

        if tab.title == "Resultados":
            tab_manager.set_active_tab(index)
            return None
        index += 1

    new_tab = tab_manager.create_new_tab("Resultados")
    frame = new_tab.frame
    frame["frameColor"] = scheme_rgba(COLOR_SEC_LIGHT)
    frame["layoutDir"] = "Y"

    UI(frame)
