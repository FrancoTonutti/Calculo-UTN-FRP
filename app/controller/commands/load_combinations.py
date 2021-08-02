
from app.model import Load
from direct.task.Task import TaskManager
from app import app

from panda3d.core import LineSegs, NodePath
import numpy as np

from app.controller.console import command, execute
from app.model.load_combination import LoadCombination
from app.view.interface.color_scheme import *
from app.view.simpleui import SimpleScrolledFrame, SimpleLabel, SimpleButton, \
    SimpleCheckBox, SimpleEntry

from app.model.load_type import LoadType
from app.view import simpleui

def create_label(text, parent):
    font_panda3d, font_pil = draw.draw_get_font()
    width = font_pil.getsize(text)[0]
    size = [20 + width, 19]

    label = SimpleLabel(
        text_fg=scheme_rgba(COLOR_TEXT_LIGHT),
        orginV="bottom",
        position=[0, 0],
        text_scale=(12, 12),
        text=text,
        parent=parent,
        size=size,
        frameColor="C_WHITE",
        alpha=0,
        align="left",
        textCenterX=False,
        padding=[15, 0, 0, 0]

    )

    return label

def new_button(text, colors=None, command=None, args=None, parent=None, size=None, padding=None):
    if args is None:
        args = []
    font_panda3d, font_pil = draw.draw_get_font()
    if colors is None:
        col_rollover = draw.merge_color(COLOR_SEC_DARK, COLOR_MAIN_LIGHT, 0.8)
        colors = [COLOR_SEC_DARK, COLOR_MAIN_LIGHT, col_rollover, "C_CONCRETE"]
    if size is None:
        width = font_pil.getsize(text)[0]
        size = [20+width, 25]
    if padding is None:
        padding = [20, 20, 0, 0]

    btn = SimpleButton(text=text,
                       text_scale=(12, 12),
                       text_font=font_panda3d,
                       text_fg=draw.get_color(COLOR_TEXT_LIGHT, "rgba"),
                       command=command,
                       parent=parent,
                       extraArgs=args,
                       colorList=colors,
                       position=[0, 0],
                       padding=padding,
                       size=size
                       )

    return btn


class Table:
    def __init__(self, titles, parent, model, params):
        frame_scrolled = SimpleScrolledFrame(

            position=[0, 0],
            canvasSize=(0, 100, -200, 0),
            parent=parent,
            layout="GridLayout",
            layoutDir="X",
            gridCols=max(len(titles), 1),
            gridRows=2,
            frameColor=scheme_rgba(COLOR_MAIN_LIGHT),
            alpha=1
        )
        self.canvas = frame_scrolled.getCanvas()
        for title in titles:
            label = create_label(title, self.canvas)
            #btn = new_button(title, parent=canvas)

        self.frame = frame_scrolled
        self.model = model
        self.params = params
        self.data_fields = list()
        self.update_table()

    def update_table(self):
        for fields in self.data_fields:
            for field in fields:
                field.destroy()
        self.data_fields.clear()

        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities(self.model)
        entities = sorted(entities, key=lambda x: x.index)

        for entity in entities:

            print("entity", entity)
            field_list = list()
            for param in self.params:
                field = self.add_field(entity, param, entity.prop_name(param), getattr(entity, param))
                field_list.append(field)
            self.data_fields.append(field_list)
        self.frame["gridRows"] = len(self.data_fields)+1
        simpleui.update_ui()

    def entity_set_prop(self, new_value: any, entity, name: str):
        old_value = getattr(entity, name, None)

        if new_value != "" and isinstance(old_value, float):
            new_value = float(new_value)

        if new_value != "" and isinstance(old_value, int):
            new_value = int(new_value)

        if isinstance(old_value, bool):
            if new_value == "True":
                new_value = True
            elif new_value == "False":
                new_value = False

        if old_value == new_value:
            return None

        if type(old_value) is type(new_value):
            if entity is not None:
                print("atributo establecido {}: {}".format(name, new_value))
                setattr(entity, name, new_value)
                print("verif {}: {}".format(name, getattr(entity, name,
                                                          "undefined")))
        else:
            if entity is not None:
                print("El tipo de asignación no corresponde: {},{}->{}".format(
                    name, type(old_value), type(new_value)))

    def add_field(self, entity, prop: str, fieldname: str, value=0):
        if isinstance(value, bool):
            entry = SimpleCheckBox(
                position=[0, 0],
                size=[None, 20],
                sizeHint=[0.50, None],
                parent=self.canvas,
                command=self.entity_set_prop,
                extraArgs=[entity, prop],
                value=value,
                frameColor="C_WHITE",
                maxSize=16
            )
        else:
            entry = SimpleEntry(
                text_fg=scheme_rgba(COLOR_TEXT_LIGHT),
                orginH="center",
                position=[0, 0],
                text_scale=(12, 12),
                width=20,
                align="left",
                textCenterX=False,
                command=self.entity_set_prop,
                extraArgs=[entity, prop],
                focusOutCommand=self.entity_set_prop,
                focusOutExtraArgs=[entity, prop],
                parent=self.canvas,
                size=[None, 20],
                padding=[15, 0, 0, 0],
                sizeHint=[1, None],
                frameColor="C_WHITE",
                alpha=0,
                initialText=str(value)

            )
        return entry






class UI:
    def __init__(self, frame):

        create_label("Tipos de carga", frame)

        btn1 = new_button("Agregar Tipo", parent=frame,
                          command=self.create_load_type)

        self.load_table = Table(["Nº", "Descripción", "Nombre"], frame, "LoadType",
                                ["index", "name", "load_code"])

        create_label("Combinaciones de cargas", frame)

        btn1 = new_button("Agregar Combinación", parent=frame,
                          command=self.create_load_combination)

        self.combination_table = Table(["Nº", "Designación", "Ecuación"], frame, "LoadCombination",
                                ["index", "name", "equation"])

        execute("regen_ui")

    def create_load_type(self):
        LoadType("Carga1", "D")
        self.load_table.update_table()

    def create_load_combination(self):
        LoadCombination("12-1", "1.4*D")
        self.combination_table.update_table()




@command(name="load_combinations", shortcut="b")
def load_combinations():
    tab_manager = app.main_ui.tab_manager

    index = 0
    for tab in tab_manager.tabs:

        if tab.title == "Combinaciones de cargas":
            tab_manager.set_active_tab(index)
            return None
        index += 1

    new_tab = tab_manager.create_new_tab("Combinaciones de cargas")
    frame = new_tab.frame
    frame["frameColor"] = scheme_rgba(COLOR_SEC_LIGHT)
    frame["layoutDir"] = "Y"

    UI(frame)



