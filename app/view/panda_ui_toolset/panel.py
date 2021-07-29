import math
from typing import List

from direct.gui.OnscreenGeom import OnscreenGeom
from panda3d.core import GeomVertexData, GeomVertexFormat, Geom, \
    GeomVertexWriter, GeomTristrips, GeomNode, Point3D, deg2Rad, NodePath, \
    VBase4
from panda3d.egg import EggData, EggVertexPool, EggPolygon, EggVertex, \
    loadEggData

from .ui_element import UIElement
from .framework_element import FrameworkElement
from .media.brush import Brush
import typing
from .controls import Orientation
from panda3d.core import MeshDrawer2D

from .media.solid_color_brush import SolidColorBrush


class Panel(FrameworkElement):
    def __init__(self, orientation: typing.Union[int, str, None] = None,
                 background="White",
                 **kwargs):
        """
        Parameters
        ----------
        orientation
        parent: FrameworkElement
        width
        height
        margin
        min_width
        max_width
        min_height
        max_height
        background
        logical_orientation
        """
        super().__init__(**kwargs)

        self.background: typing.Union[Brush, None] = background
        self.logical_orientation: typing.Union[Orientation, int, None] = None
        self.set_orientation(orientation)

    @property
    def background(self):
        return self._background_brush

    @background.setter
    def background(self, value):
        if isinstance(value, str):
            brush = SolidColorBrush(color=value)

            self._background_brush = brush



    def set_orientation(self, orientation: typing.Union[int, str, None]):

        if isinstance(orientation, str):
            if orientation == "Horizontal":
                orientation = Orientation.HORIZONTAL
            elif orientation == "Vertical":
                orientation = Orientation.VERTICAL
            else:
                exeption_msj = "The string '{}' is not valid orientation. " \
                               "Options allowed: 'Horizontal', " \
                               "'Vertical".format(orientation)
                raise ValueError(exeption_msj)
        elif isinstance(orientation, int):
            if orientation is not 0 and orientation is not 1:
                exeption_msj = "The int '{}' is not valid orientation. " \
                               "Options allowed: 0, 1".format(orientation)
                raise ValueError(exeption_msj)
        elif orientation is not None and not isinstance(orientation, Orientation):
            exeption_msj = "Orientation must be int or str, not '{}'".format(type(orientation))
            raise TypeError(exeption_msj)

        self.logical_orientation = orientation

    @property
    def has_logical_orientation(self) -> bool:
        return self.logical_orientation is not None

    @property
    def childreen_count(self) -> int:
        return len(self._childreen)

    def generate_geom(self):
        data = EggData()

        vp = EggVertexPool('fan')
        data.addChild(vp)

        # real polygons:
        radius = 30  # arc radius
        width = self.get_render_width()  # line width
        height = - self.get_render_height()
        screen = (1024, 768)

        x0 = self._x
        y0 = -self._y

        strips = {
            'rect': [
                {'x': x0, 'z': y0},  # tl
                {'x': x0 + width, 'z': y0},  # tr
                {'x': x0 + width, 'z': y0 + height},  # br
                {'x': x0, 'z': y0 + height}  # bl
            ]
        }

        for strip in strips.keys():
            poly = EggPolygon()
            data.addChild(poly)
            for vert in strips[strip]:
                v = EggVertex()
                v.setPos(Point3D(vert['x'], 0, vert['z']))

                r, g, b = self.background.get_vertex_color(0, 0)

                v.setColor(VBase4(r, g, b, 1))
                #v.setColor((256, 138.0 / 256, 72.0 / 256, 1))
                poly.addVertex(vp.addVertex(v))

        node = loadEggData(data)

        return NodePath(node)

    def update_render(self):
        geom_node = self.generate_geom()

        if self.geom is None:
            self.geom = OnscreenGeom(
                geom=geom_node,
                pos=(0, 0, 0),
                hpr=(0, 0, 0),
                scale=(1, 1, 1),
                parent=pixel2d
            )
        else:
            self.geom.setGeom(geom_node)






