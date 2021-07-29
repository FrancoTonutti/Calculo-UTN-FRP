from direct.showbase import DirectObject

from typing import TYPE_CHECKING
from typing import List
if TYPE_CHECKING:
    # Imports only for IDE type hints
    from .framework_element import FrameworkElement


class Window():
    def __init__(self, parent=None):
        """

        Parameters
        ----------
        parent: FrameworkElement
        """
        super().__init__()
        self._render_width = 0
        self._render_height = 0
        self._childreen: List[FrameworkElement] = list()


    @property
    def actual_width(self):
        return self._render_width

    @property
    def actual_height(self):
        return self._render_height

    @property
    def childreen(self):
        return self._childreen

    def _add_child(self, child):
        if child not in self._childreen:
            if len(self._childreen) == 0:
                self._childreen.append(child)
            else:
                raise AttributeError("The main window must have an unique content")

    def _remove_child(self, child):
        if child in self._childreen:
            self._childreen.remove(child)

    def update(self, window):
        wp = window.getProperties()
        for child in self.childreen:
            width = child.width.get_value()
            height = child.height.get_value()

            if width == "Auto":
                width = wp.getXSize()

            if height == "Auto":
                height = wp.getYSize()

            child.set_render_width(width)
            child.set_render_height(height)

            child.update_tree()





class WindowManager(DirectObject.DirectObject):
    def __init__(self):
        super().__init__()
        self.window_list = list()
        self.accept('mouse1', self.print_hello)

        win = Window()
        self.window_list.append(win)

        self.default_window = win

        self.accept("window-event", self.window_resize_event)

        self.last_width = 0
        self.last_width = 0
        self.winsize = [0, 0]

    def create_window(self):
        win = Window()
        self.window_list.append(win)

    def print_hello(self):
        print('Hello!')

    def window_resize_event(self, window=None):

        if window is not None:  # Window será igual a None si la aplicación panda3d no se inició
            wp = window.getProperties()
            newsize = [wp.getXSize(), wp.getYSize()]
            if self.winsize != newsize:
                self.winsize = newsize

                for win in self.window_list:
                    win.update(window)


manager = WindowManager()