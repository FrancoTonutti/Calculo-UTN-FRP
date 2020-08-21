from direct.gui.DirectEntry import *
from app.view import draw
from app import app
from direct.showbase.DirectObject import DirectObject
from app.view.widgets.gui_widget import GuiWidget
from direct.task.Task import TaskManager
from app.view.simpleui.simple_frame import SimpleFrame

from panda3d.core import MouseWatcher
task_manager = TaskManager()
mouse_watcher = MouseWatcher()

class Entry(DirectEntry, DirectObject, GuiWidget):
    def __init__(self, parent=None, **kw):
        self.textures = ()
        self.initialized = False

        if isinstance(parent, SimpleFrame):
            self.parent_gui = parent
        else:
            self.parent_gui = None

        optiondefs = (
            # Define type of DirectGuiWidget
            ('frameColor', (0, 0, 0, 1), self.setFrameColor),
            ('colorString', "C_CONCRETE", self.setColorString),
            ('position', [25, 25], self.setPosition),
            ('orginV', "top", self.setPosition),
            ('orginH', "left", self.setPosition),
            ('alpha', 255, self.setColorString),
            ('label', None, None),
            ('focusInCommand', self.on_focus, None),
            ('focusInExtraArgs', [], None),
            ('focusOutCommand', self.on_defocus, None),
            ('focusOutExtraArgs', [], None),


        )
        optiondefs = self.mergeoptions(optiondefs)
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        if parent is None:
            parent = pixel2d

        DirectEntry.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(Entry)
        size = self['frameSize']
        if size is None:
            size = self["text_scale"][1]
            self.setPos(0, 0, -size)
        else:
            self.setPos(-size[0], 0, -size[3])

        self.flattenLight()
        self.setPosition()
        self.initialized = True
        if self["size"] is None:
            font_size = self["text_scale"][1]
            self["size"] = [font_size*self["width"], font_size*self["numLines"]+4]
        self.set_size()

        self.accept('aspectRatioChanged', self.setPosition)
        print("initial text", self["initialText"])
        if self["label"] is not None and self["initialText"] is "":
            self.enterText(self["label"])

    def on_focus(self, *args):
        self["focus"] = True
        print("on_focus", self["focus"])
        if self.get() == self["label"]:
            self.enterText("")
        task_manager.add(self.focus_task, "entry_focus_task")

    def on_defocus(self):
        self["focus"] = False
        if self["label"] is not None and self.get() is "":
            self.enterText(self["label"])
        else:
            print("defocus", self.get() == "", self["text"])



    def focus_task(self, task):
        panda3d = app.get_show_base()
        btn = panda3d.mouseWatcherNode

        if btn.isButtonDown("mouse1"):
            mouse_data = panda3d.win.getPointer(0)
            mouse_x, mouse_y = mouse_data.getX(), mouse_data.getY()

            frame_size = self["frameSize"]
            if frame_size is None:
                frame_size = self.getBounds()
            else:
                frame_size = list(frame_size)

            pos = self.getPos(pixel2d)

            x0 = pos[0] + frame_size[0]
            x1 = pos[0] + frame_size[1]
            y0 = -pos[2] - frame_size[2]
            y1 = -pos[2] - frame_size[3]

            x_left = min(x0, x1)
            x_right = max(x0, x1)
            y_top = min(y0, y1)
            y_bottom = max(y0, y1)

            overmouse_x = (x_left <= mouse_x <= x_right)
            overmouse_y = (y_top <= mouse_y <= y_bottom)

            if not overmouse_x or not overmouse_y:
                print("over task")
                task_manager.remove(task)
                self["focus"] = False




        return task.cont

    def defocus(self):
        self["focus"] = False
