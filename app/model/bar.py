from app.model.entity import Entity, register
import numpy as np
from app.view import draw
from app import app
from .material import Material

from typing import TYPE_CHECKING
from typing import List
if TYPE_CHECKING:
    # Imports only for IDE type hints
    from app.model import *


class Bar(Entity):

    def __init__(self, start, end, section, material=None):
        super().__init__()
        self.name = ""
        self.start: Node = start
        self.end: Node = end
        self.section: Section = section
        if material is None:
            material = Material(20 * (10 ** 9))
        self.material: Material = material
        self._width = 0.2
        self._height = 0.3
        self.borders = True

        self.loads: List[Load] = []

        self.start.add_child_model(self)
        self.end.add_child_model(self)

        self.show_properties("name", "width", "height", "borders")

        self.show_properties("start_x", "start_y", "start_z")
        self.set_prop_name(start_x="Incio x", start_y="Incio y", start_z="Incio z")
        self.show_properties("end_x", "end_y", "end_z")
        self.set_prop_name(end_x="Fin x", end_y="Fin y", end_z="Fin z")
        register(self)

        self.create_model()

    def __str__(self):
        if self.name is "":
            name_start = self.start.name
            name_end = self.end.name

            if name_start is not "" and name_end is not "":
                name = "Barra {}-{}".format(name_start, name_end)
            else:
                name = None
        else:
            name = "Barra {}".format(self.name)

        if name is None:
            return super().__str__()
        else:
            return name

    def add_load(self, new_load):
        self.loads.append(new_load)

    def get_loads(self):
        for load_entity in self.loads:
            yield load_entity

    def longitude(self):
        start = self.start.position[0], self.start.position[1]
        end = self.end.position[0], self.end.position[1]

        delta_x = end[0] - start[0]
        delta_y = end[1] - start[1]

        long = np.linalg.norm([delta_x, delta_y])

        return long


    @property
    def width(self):
        return self.section.size[0]

    @width.setter
    def width(self, value):
        print("setter width")
        self.section.size[0] = value

    @property
    def height(self):
        return self.section.size[1]

    @height.setter
    def height(self, value):
        print("setter height")
        self.section.size[1] = value

    @property
    def start_x(self):
        return self.start.x

    @start_x.setter
    def start_x(self, value: str):
        self.start.x = value

    @property
    def start_y(self):
        return self.start.y

    @start_y.setter
    def start_y(self, value: str):
        self.start.y = value

    @property
    def start_z(self):
        return self.start.z

    @start_z.setter
    def start_z(self, value: str):
        self.start.z = value

    @property
    def end_x(self):
        return self.end.x

    @end_x.setter
    def end_x(self, value: str):
        self.end.x = value

    @property
    def end_y(self):
        return self.end.y

    @end_y.setter
    def end_y(self, value: str):
        self.end.y = value

    @property
    def end_z(self):
        return self.end.z

    @end_z.setter
    def end_z(self, value: str):
        self.end.z = value

    def create_model(self):
        print("CREATE MODEL")
        self.geom = [None, None]
        self.geom[0] = self.load_model("data/geom/beam")

        self.update_model()

    def update_model(self):
        geom = self.geom[0]
        x0, y0, z0 = self.start.position
        x1, y1, z1 = self.end.position
        geom.setPos(x0, y0, z0)

        b, h = self.section.size
        x = x1 - x0
        y = y1 - y0
        z = z1 - z0
        vector = [x, y, z]
        norm = np.linalg.norm(vector)
        geom.setScale(b, norm, h)
        geom.setShaderInput("showborders", self.borders, self.borders, self.borders, self.borders)

        geom.lookAt(self.end.geom[0])

        if app.wireframe is True:
            geom.hide()
            geom.setScale(0.1, norm, 0.1)

            line = self.geom[1]
            if line is not None:
                line.removeNode()
            line = draw.draw_line_3d(x0, y0, z0, x1, y1, z1, 3, "C_BLUE")

            line.setDepthOffset(1)
            self.geom[1] = line
            print("!!!!!!!!!!!!!!!!!!!!!!line")
            print(line)
            #line.setLight(panda3d.plight_node)

        else:
            line = self.geom[1]
            if line is not None:
                line.removeNode()
                self.geom[1] = None
