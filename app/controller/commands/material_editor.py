from direct.task.Task import Task
from panda3d.core import WindowProperties
from panda3d.core import WindowHandle
from app import app
from app.controller.console import command
from panda3d.core import GraphicsWindow


@command(name="medit", shortcut="s")
def medit():
    print("medit")
    # win = app.base.openWindow()
    wp = WindowProperties()
    wp.clearDefault()
    wp.setSize(500, 500)
    wp.setOrigin(512, 128)
    wp.setTitle("Editor de Materiales")

    win: GraphicsWindow = app.base.win
    h = win.getWindowHandle()

    # wp.setParentWindow(h)
    wp.setZOrder(WindowProperties.Z_top)
    print(wp.getUndecorated())

    medit_win = app.base.openWindow(props=wp, aspectRatio=1)

    task = Task(medit_focus_task)

    app.base.task_mgr.add(task, "medit_focus_task", extraArgs=[task, medit_win])


def medit_focus_task(task, medit_win: GraphicsWindow):
    # print(medit_win.getProperties().getForeground())

    base_props = app.base.win.getProperties()
    medit_props = medit_win.getProperties()

    base_foreground = not base_props.getForeground()
    medit_foreground = not medit_props.getForeground()

    print("base_foreground : {}".format(base_foreground))
    print("base minimized : {}".format(base_props.minimized))
    print("medit_foreground : {}".format(medit_foreground))

    if base_foreground and medit_foreground:
        properties = WindowProperties()
        properties.setZOrder(WindowProperties.Z_normal)
        properties.setMinimized(True)
        medit_win.request_properties(properties)
        print("minimize")
    elif not base_foreground and medit_props.minimized:
        properties = WindowProperties()
        properties.setZOrder(WindowProperties.Z_top)
        properties.setMinimized(False)
        medit_win.request_properties(properties)
        print("maximize")

    if not medit_win.getProperties().getOpen():
        return task.done

    return task.cont
