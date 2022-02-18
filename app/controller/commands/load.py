from app.model import Load, Bar
from direct.task.Task import TaskManager
from app import app

from panda3d.core import LineSegs, NodePath
import numpy as np

from app.controller.console import command, execute
import pint

from app.model import unit_manager
from app.model.transaction import TM, Transaction
from app.view.interface.properties import PropEditorModes


@command(name="load")
def add_load():
    print("ADD LOAD")
    tr = TM.get_active_transaction()
    print(tr)
    # Agrega una tarea al TaskManager para agregar una carga

    tr = Transaction()
    tr.start("Create load")

    entity = None
    value = 10 * app.ureg("kN")
    angle = 90

    status_bar = app.main_ui.status_bar
    status_bar.set_status_hint("Seleccione una barra")

    new_load = Load(entity, value, angle)

    prop_editor = app.main_ui.prop_editor
    prop_editor.set_mode(PropEditorModes.CREATE)
    prop_editor.entity_read(new_load)

    app.console.start_command(add_load_task)


def add_load_task(task):
    tr = TM.get_root_transaction()
    if tr.name == "Create load":
        prop_editor = app.main_ui.prop_editor

        for entity in prop_editor.selection:
            if isinstance(entity, Bar):
                status_bar = app.main_ui.status_bar
                status_bar.set_status_hint("")
                prop_editor.entity.set_parent(entity)
                prop_editor.set_mode(PropEditorModes.EDIT)
                prop_editor.add_to_selection(prop_editor.entity)
                tr.commit()

                return task.done

        panda3d = app.get_show_base()
        watcher = panda3d.mouseWatcherNode
        if watcher.has_mouse() and (watcher.isButtonDown("escape") or watcher.isButtonDown("mouse3")):
            print("ROLLBACK")
            tr.rollback()
            status_bar = app.main_ui.status_bar
            status_bar.set_status_hint("")
            prop_editor.set_mode(PropEditorModes.EDIT)
            prop_editor.add_to_selection(prop_editor.entity)
            return task.done

        return task.cont
    else:
        status_bar = app.main_ui.status_bar
        status_bar.set_status_hint(tr.name)
        prop_editor = app.main_ui.prop_editor
        prop_editor.set_mode(PropEditorModes.EDIT)
        return task.done





def add_load_OLD():
    print("ADD LOAD")
    # Agrega una tarea al TaskManager para agregar una carga

    app.console.set_arg_typefuc("entity", None)
    app.console.set_arg_typefuc("value", float)
    app.console.set_arg_typefuc("angle", float)

    app.console.set_arg_suffix("value", " kN")
    app.console.set_arg_suffix("angle", " º")

    app.console.start_command(add_load_task)


def add_load_task_OLD(task):

    if app.console.get_active_arg() == "entity":
        selection = app.main_ui.status_bar.entity_info
        app.console.set_arg("entity", selection)

    if app.console.get_active_arg() is None:
        entity = app.console.get_arg("entity")
        value = app.console.get_arg("value")
        angle = app.console.get_arg("angle")

        if entity == "entity":
            entity = None

        if value == "value":
            value = None

        if angle == "angle":
            angle = None

        if entity and value and angle:
            print("Load created")

            value = value * app.ureg(unit_manager.unit_settings.get("load"))
            print(entity, value, angle)

            tr = Transaction()
            tr.start("Create load")
            load = Load(entity, value, angle)
            tr.commit()
            #entity.add_child_model(load)




            app.console.set_arg("entity", None)
            #app.console.close_command()



    return task.cont
