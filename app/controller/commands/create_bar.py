from app.model import Load, Bar, MouseEventHandler, Section, Node
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


@command(name="create_bar")
def create_bar():
    print("create_level")
    #tr = TM.get_active_transaction()
    #print(tr)
    # Agrega una tarea al TaskManager para agregar una carga

    tr = Transaction()
    tr.start("Create bar")

    z = 0

    status_bar = app.main_ui.status_bar
    status_bar.set_status_hint("Haga click en el punto inicial")

    section = Section(0.2, 0.3)
    node_start = Node(0, 0)
    node_start.hide()
    node_end = Node(1, 0)
    node_end.hide()
    new_bar = Bar(node_start, node_end, section)
    new_bar.hide()

    node_start.is_selectable = False
    node_end.is_selectable = False
    new_bar.is_selectable = False

    prop_editor = app.main_ui.prop_editor
    prop_editor.deselect_all()
    prop_editor.set_mode(PropEditorModes.CREATE)
    prop_editor.entity_read(new_bar)

    handler = MouseEventHandler()

    cache = {"handler": handler, "new_bar": new_bar, "start": node_start, "end": node_end, "step": 0}

    app.console.start_command(add_level_task, "Crear barra", cache)


def add_level_task(task, cache: dict):

    tr = TM.get_root_transaction()
    active_tr = TM.get_active_transaction()
    if tr.name == "Create bar":
        step = cache.get("step")
        handler = cache.get("handler")
        new_bar: Bar = cache.get("new_bar")
        start: Node = cache.get("start")
        end: Node = cache.get("end")

        panda3d = app.get_show_base()
        watcher = panda3d.mouseWatcherNode
        prop_editor = app.main_ui.prop_editor
        #new_level = prop_editor.entity



        if handler.mouse1_btn_released():
            if step == 0:
                x, y, z = app.work_plane_mouse
                start.position = x, y, z
                end.position = x, y, z

                for entity in prop_editor.selection:

                    if isinstance(entity, Node):
                        start.delete()

                        new_bar.start = entity
                        start = entity
                        cache.update({"start": start})
                        prop_editor.deselect_all()
                        break


                cache.update({"step": 1})

                start.show()
                end.show()

                new_bar.show()


            elif step == 1:
                x, y, z = app.work_plane_mouse

                end.position = x, y, z
                print("selection", prop_editor.selection)

                for entity in prop_editor.selection:
                    print(entity)
                    if isinstance(entity, Node):
                        end.delete()

                        new_bar.end = entity
                        end = entity
                        cache.update({"end": end})
                        break

                cache.update({"step": 2})

                start.is_selectable = True
                end.is_selectable = True
                new_bar.is_selectable = True

                prop_editor.set_mode(PropEditorModes.EDIT)
                prop_editor.add_to_selection(new_bar)
                prop_editor.update_selection()

                tr.commit()
                return task.done

            #new_level.z = round(float(z), 2)

        if step == 1:
            x, y, z = app.work_plane_mouse

            active_tr.disable_register()
            end.position = x, y, z
            active_tr.enable_register()

        if watcher.has_mouse() and (watcher.isButtonDown("escape") or watcher.isButtonDown("mouse3")):
            print("-------ROLLBACK----------------")
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