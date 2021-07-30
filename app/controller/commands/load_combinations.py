
from app.model import Load
from direct.task.Task import TaskManager
from app import app

from panda3d.core import LineSegs, NodePath
import numpy as np

from app.controller.console import command, execute
from app.view.interface.color_scheme import *
from app.view.simpleui import SimpleScrolledFrame, SimpleLabel, SimpleButton

from app.model.load_type import LoadType


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
            gridRows=10,
            frameColor=scheme_rgba(COLOR_MAIN_LIGHT),
            alpha=1
        )
        canvas = frame_scrolled.getCanvas()
        for title in titles:
            label = create_label(title, canvas)
            #btn = new_button(title, parent=canvas)

        self.frame = frame_scrolled
        self.model = model
        self.params = params
        self.update_table()

    def update_table(self):
        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities(self.model)
        for entity in entities:
            pass


def create_load_type():
    LoadType("Carga1", "D")


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

    create_label("Tipos de carga", frame)

    btn1 = new_button("Agregar Tipo", parent=frame, command=create_load_type)

    frame_scrolled = Table(["Nº", "Nombre", "Id"], frame, "LoadType", None)

    create_label("Combinaciones de cargas", frame)

    btn1 = new_button("Agregar Combinación", parent=frame)

    frame_scrolled2 = Table(["Nº", "Tipo", "Ecuación"], frame, "data", None)

    execute("regen_ui")


