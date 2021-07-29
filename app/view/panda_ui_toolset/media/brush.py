"""
Brush:

Defines objects used to paint graphical objects. Classes that derive from Brush
describe how the area is painted.
"""
from .transform import Transform
import typing


class Brush:
    def __init__(self, opacity=1):
        self.opacity: float = opacity
        self.relative_transform: typing.Union[Transform, None] = None
        self.transform: typing.Union[Transform, None] = None

    def get_vertex_color(self, u, v):
        pass
