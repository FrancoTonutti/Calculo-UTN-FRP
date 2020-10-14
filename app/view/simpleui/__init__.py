from direct.showbase.DirectObject import DirectObject
from .simple_frame import SimpleFrame
from .simple_entry import SimpleEntry
from .simple_label import SimpleLabel
from .simple_scrolled_frame import SimpleScrolledFrame
from .simple_checkbox import SimpleCheckBox
from .simple_button import SimpleButton


def update_ui():
    print("simple_ui_manager")
    resize_gui_childrens(pixel2d)


def resize_gui_childrens(nodepath):

    for obj in nodepath.children:
        #print("getPythonTag", obj.getPythonTag("simple_gui"))
        if obj.hasPythonTag('simple_gui'):
            gui_obj = obj.getPythonTag("simple_gui")
            print("set_size", gui_obj, gui_obj["frameColor"])
            gui_obj.set_size()
            resize_gui_childrens(obj)


def init():
    obj = DirectObject()
    obj.accept('aspectRatioChanged', update_ui)


init()

"""
from direct.task import Task

def simple_ui_manager_task(task):
    #print("simple_ui_manager_task")
    return task.cont
    
tm = Task.TaskManager()
if not tm.hasTaskNamed("simple_ui_manager_task"):
    tm.add(simple_ui_manager_task, "simple_ui_manager_task")
"""