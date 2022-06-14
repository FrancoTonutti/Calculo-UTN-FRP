from app.model import Load, Bar, MouseEventHandler, Section, Node
from direct.task.Task import TaskManager
from app import app

from panda3d.core import LineSegs, NodePath
import numpy as np

from app.controller.console import command, execute
import pint

from app.model import unit_manager
from app.model.entity_reference import EntityReference
from app.model.events import EventListener
from app.model.level import Level
from app.model.transaction import TM, Transaction
from app.view.interface.properties import PropEditorModes



@command(name="create_bar")
def create_bar():

    tr = Transaction()
    tr.start("Create bar")

    z = 0

    status_bar = app.main_ui.status_bar
    status_bar.set_status_hint("Haga click en el punto inicial")

    section = Section.last_section

    print("SECCION----{}".format(section.__str__()))
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

    events = EventListener()
    cache = {"handler": handler, "new_bar": new_bar, "start": node_start, "end": node_end, "step": 0, "events": events, "on_select": None}

    events.add_listener("onselect", on_select, args=[cache])

    app.console.start_command(add_bar_task, "Crear barra", cache)


def on_select(cache, selection):
    print("on_select()", selection)
    step = cache.get("step")
    if step == 0:
        step_1(cache, selection)
    elif step == 1:
        step_2(cache, selection)


def step_1(cache, selection):

    print("step_1", selection)

    new_bar: Bar = cache.get("new_bar")
    start: Node = cache.get("start")
    end: Node = cache.get("end")
    prop_editor = app.main_ui.prop_editor

    x, y, z = app.work_plane_mouse
    start.position = x, y, z
    end.position = x, y, z

    print("mouse1_btn_released start", selection)
    for entity in selection:
        if isinstance(entity, EntityReference):
            entity = entity.__reference__

        if isinstance(entity, Node):
            old_start = new_bar.start#start.delete()

            new_bar.start = entity
            old_start.delete()

            start = entity
            cache.update({"start": start})
            prop_editor.deselect_all()
            break
        elif isinstance(entity, Level):
            start.plane_z = entity

            break

    start.show()
    end.show()

    new_bar.show()

    cache.update({"step": 1})


def step_2(cache, selection):

    print("step_2", selection)

    new_bar: Bar = cache.get("new_bar")
    start: Node = cache.get("start")
    end: Node = cache.get("end")
    prop_editor = app.main_ui.prop_editor

    x, y, z = app.work_plane_mouse

    end.position = x, y, z
    print("mouse1_btn_released end", prop_editor.selection)
    for entity in prop_editor.selection:
        if isinstance(entity, EntityReference):
            entity = entity.__reference__

        if isinstance(entity, Node):
            old_end = new_bar.end
            new_bar.end = entity
            old_end.delete()
            end = entity
            cache.update({"end": end})
            break
        elif isinstance(entity, Level):
            end.plane_z = entity

            break

    cache.update({"step": 2})


def add_bar_task(task, cache: dict):
    tr = TM.get_root_transaction()
    active_tr = TM.get_active_transaction()
    if tr.name == "Create bar":
        step = cache.get("step")
        handler = cache.get("handler")
        new_bar: Bar = cache.get("new_bar")
        start: Node = cache.get("start")
        end: Node = cache.get("end")
        events: EventListener = cache.get("events")

        panda3d = app.get_show_base()
        watcher = panda3d.mouseWatcherNode
        prop_editor = app.main_ui.prop_editor
        status_bar = app.main_ui.status_bar

        if step == 1:
            x, y, z = app.work_plane_mouse

            active_tr.disable_register()
            end.position = x, y, z
            active_tr.enable_register()

        elif step == 2:
            start.is_selectable = True
            end.is_selectable = True
            new_bar.is_selectable = True

            prop_editor.set_mode(PropEditorModes.EDIT)
            prop_editor.add_to_selection(new_bar)
            prop_editor.update_selection()

            tr.commit()
            events.close_listener()
            return task.done

        if watcher.has_mouse() and (watcher.isButtonDown("escape") or watcher.isButtonDown("mouse3")):
            print("-------ROLLBACK----------------")
            tr.rollback()
            events.close_listener()
            return add_bar_end(task)

        return task.cont
    else:
        print("ROOT TRANSACTION ERROR")
        return add_bar_end(task)


def add_bar_end(task):
    status_bar = app.main_ui.status_bar
    status_bar.set_status_hint("")
    prop_editor = app.main_ui.prop_editor
    prop_editor.set_mode(PropEditorModes.EDIT)
    return task.done