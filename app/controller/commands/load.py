from app.model import Load
from direct.task.Task import TaskManager
from app import app

from panda3d.core import LineSegs, NodePath
import numpy as np

from app.controller.console import command, execute




@command(name="load", shortcut="b", args=["entity", "value", "angle"])
def add_load():
    print("ADD LOAD")
    # Agrega una tarea al TaskManager para agregar una carga

    app.console.set_arg_typefuc("entity", None)
    app.console.set_arg_typefuc("value", float)
    app.console.set_arg_typefuc("angle", float)

    app.console.set_arg_suffix("value", " kN")
    app.console.set_arg_suffix("angle", " º")

    app.console.start_command(add_load_task)


def add_load_task(task):

    if app.console.get_active_arg() == "entity":
        selection = app.main_ui.status_bar.entity_info
        app.console.set_arg("entity", selection)

    if app.console.get_active_arg() is None:
        entity = app.console.get_arg("entity")
        value = app.console.get_arg("value")
        angle = app.console.get_arg("angle")

        if entity and value and angle:
            load = Load(entity, value, angle)
            #entity.add_child_model(load)


            app.console.set_arg("entity", None)
            app.console.close_command()



    return task.cont
