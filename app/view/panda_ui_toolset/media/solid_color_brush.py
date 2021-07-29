"""
Brush:

Defines objects used to paint graphical objects. Classes that derive from Brush
describe how the area is painted.
"""
from .transform import Transform
from .brush import Brush
import typing
from .colors import Colors


class SolidColorBrush(Brush):
    def __init__(self, color="White", **kwargs):
        super().__init__(**kwargs)

        self._color = Colors(color)

    def set_color(self, color):
        self._color = Colors(color)

    def get_vertex_color(self, u, v):
        return self._color.get_rgb()
