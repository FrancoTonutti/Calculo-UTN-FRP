from .ui_element import UIElement
from .window import manager
import typing
from typing import List
from .qualifed_double import QualifedDouble
from .thickness import Thickness
from .controls import get_args


class FrameworkElement(UIElement):
    def __init__(self, parent=None, width="Auto", height="Auto", margin=0,
                 min_width=10, max_width="Auto", min_height=10,
                 max_height="Auto"):
        """

        Parameters
        ----------
        parent: FrameworkElement
        width
        height
        margin
        min_width
        max_width
        min_height
        max_height
        """

        '''default_args = {
            "parent": None,
            "width": "Auto",
            "height": "Auto",
            "margin": 0,
            "min_width": 0,
            "max_width": "Auto",
            "min_height": 0,
            "max_height": "Auto"

        }

        kwargs = get_args(default_args, **kwargs)'''

        super().__init__()
        self._render_width = QualifedDouble(0)
        self._render_height = QualifedDouble(0)
        self.cursor = None
        self._childreen: List[FrameworkElement] = list()
        self._parent: typing.Union[FrameworkElement, None] = None

        self._width = QualifedDouble(width)
        self._height = QualifedDouble(height)
        self._min_width = QualifedDouble(min_width)
        self._max_width = QualifedDouble(max_width)
        self._min_height = QualifedDouble(min_height)
        self._max_height = QualifedDouble(max_height)


        self.use_layout_rounding = False

        self.set_parent(parent)

        self._margin = Thickness(margin)

        self._x = 0
        self._y = 0

        self.geom = None

    @property
    def margin(self):
        return self._margin

    @margin.setter
    def margin(self, left, top=None, right=None, bottom=None):
        self._margin.set_thickness(left, top, right, bottom)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width.set_value(value)

    @property
    def min_width(self):
        return self._min_width

    @min_width.setter
    def min_width(self, value):
        self._min_width.set_value(value)

    @property
    def max_width(self):
        return self._max_width

    @max_width.setter
    def max_width(self, value):
        self._max_width.set_value(value)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height.set_value(value)

    @property
    def min_height(self):
        return self._min_height

    @min_height.setter
    def min_height(self, value):
        self._min_height.set_value(value)

    @property
    def max_height(self):
        return self._max_height

    @max_height.setter
    def max_height(self, value):
        self._max_height.set_value(value)

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
            self._childreen.append(child)

    def _remove_child(self, child):
        if child in self._childreen:
            self._childreen.remove(child)

    def set_parent(self, parent):
        if parent and not isinstance(parent, FrameworkElement):
            exeption_msj = "Parent object must be instance of " \
                           "FrameworkElement, not '{}'".format(type(parent))
            raise TypeError(exeption_msj)

        if self._parent is not None:
            self._parent._remove_child(self)

        if parent is None:
            parent = manager.default_window

        parent._add_child(self)

        self._parent = parent

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self.set_parent(value)

    def set_render_width(self, width):
        self._render_width.set_value(width)

    def get_render_width(self):
        return self._render_width.get_value()

    def get_render_height(self):
        return self._render_height.get_value()

    def set_render_height(self, height):
        self._render_height.set_value(height)

    def set_render_pos(self, x=None, y=None):

        if x:
            self._x = x

        if y:
            self._y = y


    def update_render(self):
        pass

    def update_layout(self):
        pass

    def update_tree(self):
        self.update_render()
        self.update_layout()

        for child in self.childreen:
            child.update_tree()

