from app.model import Load, Bar, MouseEventHandler, Section, Node, View
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



@command(name="delete")
def create_bar():

    tr = Transaction()
    tr.start("Delete Entity")

    z = 0

    status_bar = app.main_ui.status_bar
    status_bar.set_status_hint("Haga click en un elemento para eliminarlo")

    prop_editor = app.main_ui.prop_editor
    #prop_editor.deselect_all()

    handler = MouseEventHandler()

    events = EventListener()
    cache = {"name": "delete", "handler": handler, "step": 0, "events": events, "on_select": None}

    events.add_listener("onselect", on_select, args=[cache])

    app.console.start_command(delete_task, "Eliminar", cache)


def on_select(cache, selection):
    print("on_select()", selection)
    step = cache.get("step")
    if step == 0:
        for entity in selection:
            if isinstance(entity, View):
                continue
            print("Eliminar: {}".format(entity))
            entity.delete()

def delete_task(task, cache: dict):
    tr = TM.get_root_transaction()
    active_tr = TM.get_active_transaction()
    if tr.name == "Delete Entity":
        #step = cache.get("step")
        #handler = cache.get("handler")
        events: EventListener = cache.get("events")

        panda3d = app.get_show_base()
        watcher = panda3d.mouseWatcherNode
        #prop_editor = app.main_ui.prop_editor
        #status_bar = app.main_ui.status_bar


        if watcher.has_mouse() and (watcher.isButtonDown("escape") or watcher.isButtonDown("mouse3")):
            print("-------ROLLBACK----------------")
            #tr.rollback()
            cache.update({"step": 1})
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