from direct.gui.DirectEntry import *
from direct.task.Task import TaskManager
from app.view.simpleui.simple_frame import SimpleFrame
from app.view.widgets.gui_widget import GuiWidget
from panda3d.core import MouseWatcher, PGEntry
task_manager = TaskManager()
mouse_watcher = MouseWatcher()
from app import app
import random
from panda3d.core import TextProperties
from app.view import draw
from direct.gui import DirectGuiGlobals as DGG
from app.view.simpleui import window


class SimpleEntry(DirectEntry, SimpleFrame):
    def __init__(self, parent=None, **kw):
        # ('focusInCommand', self.on_focus, None),
        # ('focusOutCommand', self.on_defocus, None),
        optiondefs = (
            # Define type of DirectGuiWidget
            ('label', "None", None),

            ('focusInExtraArgs', [], None),

            ('focusOutExtraArgs', [], None),
            ('textCenterX', True, self.update_text_pos),
            ('textCenterY', True, self.update_text_pos),
            ('align', "center", self.set_align),
            ('value', None, None),
            ('typeFunc', str, None),
            ('prefix', "", None),
            ('suffix', "", None),

        )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        if parent is None:
            parent = pixel2d

        DirectEntry.__init__(self, parent)
        SimpleFrame.__init__(self, parent, override_default=True)

        self["text_font"] = draw.draw_get_font()[0]

        # Call option initialization functionsprint("initialiseoptions START !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.initialiseoptions(SimpleEntry)

        self.set_position()

        self.initialized = True

        if self["size"] == [None, None]:
            font_size = self["text_scale"][1]
            self["size"] = [font_size*self["width"], font_size*self["numLines"]+4]

        self.set_size()

        if self["label"] is not None and self["initialText"] is "":
            self.enterText(self["label"])

        #task_manager.add(self.focus_task, "entry_focus_task")
        self.bind(DGG.ENTER, self.on_enter)
        self.bind(DGG.EXIT, self.on_leave)

        self.accept(self.guiItem.getFocusInEvent(), self.on_focus)
        self.accept(self.guiItem.getFocusOutEvent(), self.on_defocus)

        if not self.isEmpty():
            self["focus"] = False
            if self["label"] is not None and self.get() is "":
                self.enterText(self["label"])
            elif self.get() is not "":
                func = self["typeFunc"]
                if func is not None:

                    self.enter_value(func(self.get()))
                    prefix = self["prefix"]
                    txt = self.get()
                    suffix = self["suffix"]

                    self.enterText("{}{}{}".format(prefix, txt, suffix))

        #self.on_defocus()



    def on_enter(self, event):
        # draw.change_cursor("/c/Windows/Cursors/no_rm.cur")
        # draw.change_cursor("/d/Bibliotecas/Documentos/Python 3/UTN/Calculo-UTN-FRP/data/cursors/cursor-link.cur")
        # draw.change_cursor("data/cursors/link.cur")
        window.set_cursor(window.cr_beam)


    def on_leave(self, event):
        # draw.change_cursor("/c/Windows/Cursors/aero_arrow.cur")
        # draw.change_cursor("/d/Bibliotecas/Documentos/Python 3/UTN/Calculo-UTN-FRP/data/cursors/arrow.cur")
        window.set_cursor(window.cr_arrow)

    def on_focus(self, event=None):
        self.focusInCommandFunc()
        self["focus"] = True
        if self.get() == self["label"]:
            self.enterText("")
        else:
            value = self['value']
            if value is not None:
                self.enterText(str(value))

        task_manager.add(self.focus_task, "entry_focus_task")

    def on_defocus(self, event=None):
        self.focusOutCommandFunc()
        if not self.isEmpty():
            self["focus"] = False
            if self["label"] is not None and self.get() is "":
                self.enterText(self["label"])
            elif self.get() is not "":
                func = self["typeFunc"]
                if func is not None:

                    self.enter_value(func(self.get()))
                    prefix = self["prefix"]
                    txt = self.get()
                    suffix = self["suffix"]

                    self.enterText("{}{}{}".format(prefix, txt, suffix))

    def focus_task(self, task):
        panda3d = app.get_show_base()
        btn = panda3d.mouseWatcherNode

        if btn.isButtonDown("mouse1"):
            mouse_data = panda3d.win.getPointer(0)
            mouse_x, mouse_y = mouse_data.getX(), mouse_data.getY()

            if str(self) == "**removed**":
                task_manager.remove(task)
                return task.cont

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
                task_manager.remove(task)
                self["focus"] = False
        return task.cont

    def defocus(self):
        self["focus"] = False
        self.on_defocus()
        PGEntry.setFocus(self.guiItem, self['focus'])

    def update_text_pos(self):

        if hasattr(self, "enterText"):
            width, height = self.box_size()

            txt_x, txt_y = self["text_pos"]
            size_x, size_y = self["text_scale"]
            if self["textCenterX"]:
                txt_x = width / 2
            if self["textCenterY"]:
                txt_y = -(height / 2 + size_y / 2)
            self["text_pos"] = (txt_x, txt_y)

    def set_align(self):
        if hasattr(self, "onscreenText"):
            if self["align"] is "left":
                self["text_align"] = TextProperties.A_left
            elif self["align"] is "center":
                self["text_align"] = TextProperties.A_center
            elif self["align"] is "right":
                self["text_align"] = TextProperties.A_right

    def focusInCommandFunc(self):
        if self['focusInCommand']:
            self['focusInCommand'](*[self.get()] + self['focusInExtraArgs'])
        if self['autoCapitalize']:
            self.accept(self.guiItem.getTypeEvent(), self._handleTyping)
            self.accept(self.guiItem.getEraseEvent(), self._handleErasing)

    def focusOutCommandFunc(self):
        if self['focusOutCommand']:
            self['focusOutCommand'](*[self.get()] + self['focusOutExtraArgs'])
        if not self.isEmpty():
            if self['autoCapitalize']:
                self.ignore(self.guiItem.getTypeEvent())
                self.ignore(self.guiItem.getEraseEvent())

    def enter_value(self, value):
        self["value"] = value
        self.enterText(str(self["value"]))

    def get_value(self):
        value = self["value"]

        if self["focus"]:
            if str(self["value"]) != self.get():
                value = self.get()
                type_func = self["typeFunc"]
                if type_func is not None:
                    try:
                        value = type_func(value)
                    except ValueError as ex:
                        pass

        return value
