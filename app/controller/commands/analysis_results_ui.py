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


class ResultsInstance:
    def __init__(self, index):
        self.index = index
        self.name = index
        self.equation = ""
        self.max = 0
        self.min = 0
        self.percent0 = 0
        self.percent25 = 0
        self.percent50 = 0
        self.percent75 = 0
        self.percent100 = 0

    def is_read_only(self, any):
        return True


class UI:
    def __init__(self, frame):

        create_label("Barras", frame)

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

        self.title = create_label("Seleccione una barra", self.col2, padding=[15,15,15,0])

        self.selected_bar = None
        self.bar_list_buttons = list()



        for bar in entities:
            if self.selected_bar is None:
                self.selected_bar = bar

            btn = new_button(str(bar), parent=self.col1.canvas, command=self.explore_bar, args=[bar])
            self.bar_list_buttons.append(btn)



        model = []

        execute("regen_ui")
        create_label("Esfuerzos de momento", self.col2)

        self.table1 = Table(
            ["Combinación", "Ecuación","Max", "Min", "0%", "25%", "50%", "75%", "100%"],
            self.col2, model,
            ["name", "equation", "max", "min", "percent0", "percent25", "percent50",
             "percent75", "percent100"], enable_detete=False)

        create_label("Esfuerzos de corte", self.col2)
        self.table2 = Table(
            ["Combinación", "Ecuación", "Max", "Min", "0%", "25%", "50%",
             "75%", "100%"],
            self.col2, model,
            ["name", "equation", "max", "min", "percent0", "percent25",
             "percent50",
             "percent75", "percent100"], enable_detete=False)

        create_label("Esfuerzos normal", self.col2)
        self.table3 = Table(
            ["Combinación", "Ecuación", "Max", "Min", "0%", "25%", "50%",
             "75%", "100%"],
            self.col2, model,
            ["name", "equation", "max", "min", "percent0", "percent25",
             "percent50",
             "percent75", "percent100"], enable_detete=False)

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
        self.table1.update_table()

        execute("regen_ui")

    def explore_bar(self, bar_entity):
        self.selected_bar = bar_entity

        self.title["text"] = str(bar_entity)

        model_1 = []
        model_2 = []
        model_3 = []

        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("LoadCombination")

        combinations = sorted(entities, key=lambda x: x.index)

        i = 1
        for combination in combinations:
            result_1 = ResultsInstance(i)
            result_2 = ResultsInstance(i)
            result_3 = ResultsInstance(i)

            #bar_element.set_analysis_results(combination, "v_shear", v_shear)
            #bar_element.set_analysis_results(combination, "v_normal", v_normal)

            result_1.name = combination.name
            result_1.equation = combination.equation

            result_2.name = combination.name
            result_2.equation = combination.equation

            result_3.name = combination.name
            result_3.equation = combination.equation

            v_moment = bar_entity.get_analysis_results(combination, "v_moment")

            if v_moment is not None:
                print("v_moment", v_moment)

                result_1.max = v_moment[0][1]
                result_1.min = v_moment[0][1]
                for pos, value in v_moment:
                    result_1.max = max(value, result_1.max)
                    result_1.min = min(value, result_1.min)

                result_1.max = round(result_1.max, 2)
                result_1.min = round(result_1.min, 2)

                result_1.percent0 = round(v_moment[0][1], 2)
                result_1.percent25 = round(v_moment[4][1], 2)
                result_1.percent50 = round(v_moment[7][1], 2)
                result_1.percent75 = round(v_moment[10][1], 2)
                result_1.percent100 = round(v_moment[14][1], 2)

            model_1.append(result_1)

            v_shear = bar_entity.get_analysis_results(combination, "v_shear")

            if v_shear is not None:

                result_2.max = v_shear[0][1]
                result_2.min = v_shear[0][1]
                for pos, value in v_shear:
                    result_2.max = max(value, result_2.max)
                    result_2.min = min(value, result_2.min)

                result_2.max = round(result_2.max, 2)
                result_2.min = round(result_2.min, 2)

                result_2.percent0 = round(v_shear[0][1], 2)
                result_2.percent25 = round(v_shear[4][1], 2)
                result_2.percent50 = round(v_shear[7][1], 2)
                result_2.percent75 = round(v_shear[10][1], 2)
                result_2.percent100 = round(v_shear[14][1], 2)

            model_2.append(result_2)

            v_normal = bar_entity.get_analysis_results(combination, "v_normal")

            if v_normal is not None:

                result_3.max = v_normal[0][1]
                result_3.min = v_normal[0][1]
                for pos, value in v_normal:
                    result_3.max = max(value, result_3.max)
                    result_3.min = min(value, result_3.min)

                result_3.max = round(result_3.max, 2)
                result_3.min = round(result_3.min, 2)

                result_3.percent0 = round(v_normal[0][1], 2)
                result_3.percent25 = round(v_normal[4][1], 2)
                result_3.percent50 = round(v_normal[7][1], 2)
                result_3.percent75 = round(v_normal[10][1], 2)
                result_3.percent100 = round(v_normal[14][1], 2)

            model_3.append(result_3)

            i += 1

        self.table1.model = model_1
        self.table1.update_table()

        self.table2.model = model_2
        self.table2.update_table()

        self.table3.model = model_3
        self.table3.update_table()

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

    ui = UI(frame)
    new_tab.ev_focus_in = ui.update
