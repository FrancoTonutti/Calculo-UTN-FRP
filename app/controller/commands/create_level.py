from app.model import Load, Bar, MouseEventHandler
from direct.task.Task import TaskManager
from app import app

from panda3d.core import LineSegs, NodePath
import numpy as np

from app.controller.console import command, execute
import pint

from app.model import unit_manager
from app.model.level import Level
from app.model.transaction import TM, Transaction
from app.view.interface.properties import PropEditorModes


@command(name="create_level")
def create_level():
    print("create_level")
    #tr = TM.get_active_transaction()
    #print(tr)
    # Agrega una tarea al TaskManager para agregar una carga

    tr = Transaction()
    tr.start("Create level")

    z = 0

    status_bar = app.main_ui.status_bar
    status_bar.set_status_hint("Haga click en la altura deseada")

    new_level = Level(z)

    prop_editor = app.main_ui.prop_editor
    prop_editor.deselect_all()
    prop_editor.set_mode(PropEditorModes.CREATE)
    prop_editor.entity_read(new_level)

    handler = MouseEventHandler()

    app.console.start_command(add_level_task, "Crear nivel", handler)


def add_level_task(task, handler: MouseEventHandler=None):
    #print("add_level_task")
    tr = TM.get_root_transaction()
    if tr.name == "Create level":
        panda3d = app.get_show_base()
        watcher = panda3d.mouseWatcherNode
        prop_editor = app.main_ui.prop_editor
        new_level = prop_editor.entity

        if handler.mouse1_btn_released():
            x, y, z = app.work_plane_mouse
            new_level.z = round(float(z), 2)
            prop_editor.set_mode(PropEditorModes.EDIT)
            prop_editor.add_to_selection(new_level)
            prop_editor.update_selection()

            tr.commit()
            return task.done
        else:
            pass
            #print("None")


        if watcher.has_mouse() and (watcher.isButtonDown("escape") or watcher.isButtonDown("mouse3")):
            print("ROLLBACK")
            tr.rollback()
            status_bar = app.main_ui.status_bar
            status_bar.set_status_hint("")
            prop_editor.set_mode(PropEditorModes.EDIT)
            prop_editor.deselect_all()
            return task.done

        return task.cont
    else:
        print("ROOT TRANSACTION ERROR")
        status_bar = app.main_ui.status_bar
        status_bar.set_status_hint("")
        prop_editor = app.main_ui.prop_editor
        prop_editor.set_mode(PropEditorModes.EDIT)
        return task.done

