import numpy as np
from panda3d.core import BitMask32

from app.model.entity import Entity, register
from app import app

from typing import TYPE_CHECKING
from typing import List
from . import unit_manager
from ..view import draw

if TYPE_CHECKING:
    # Imports only for IDE type hints
    from app.model import *


class Level(Entity):

    @staticmethod
    def create_from_object(obj):

        entity_id = obj.get("entity_id")
        z = obj.get("z")

        name = obj.get("name")

        return Level(z, name, entity_id)

    def __init__(self, z, name="Nivel", set_id=None):
        super().__init__(set_id)
        self.z: float = z
        self._name = ""
        self.name = name

        self.show_properties("z", "name")
        self.set_prop_name(z="Altura", name="Nombre")
        self.set_units(z="m")

        self.bind_to_model("z")

        self.create_model()

    def __str__(self):
        if self.name:
            return self.name
        else:
            return super(Level, self).__str__()

    def create_model(self):
        print("CREATE model level")
        self.geom = [None]*9

        self.geom[0] = self.load_model("data/geom/square2", set_id=False)
        self.geom[0].set_two_sided(True)
        self.geom[0].setHpr(0, 90, 0)
        self.geom[0].setLightOff()
        self.geom[0].hide(BitMask32.bit(1))
        self.geom[0].setTextureOff(1)
        self.geom[0].setShaderInput("showborders", False, False, False, False)

        self.geom[5] = self.load_model("data/geom/beam")
        self.geom[6] = self.load_model("data/geom/beam")
        self.geom[7] = self.load_model("data/geom/beam")
        self.geom[8] = self.load_model("data/geom/beam")

        self.update_model()

    def update_model(self):
        #self.geom[0].reparentTo(self.geom[0])
        z = unit_manager.convert_to_m(self.z)
        self.geom[0].setPos(0, 0, z)
        scale_x = 10
        scale_y = 3
        self.geom[0].setScale(scale_x, 1, scale_y)

        if self.is_selected:
            self.geom[0].show()
        else:
            self.geom[0].hide()

        points = [
            [-0.5, 0.5],
            [0.5, 0.5],
            [0.5, -0.5],
            [-0.5, -0.5],
            [-0.5, 0.5],
            ]


        for i in range(1, 5):
            x0, y0 = points[i-1]
            x1, y1 = points[i]

            x0 *= scale_x
            x1 *= scale_x

            y0 *= scale_y
            y1 *= scale_y

            line = self.geom[i]
            color = None
            if line is not None:
                color = line.getColorScale()
                line.removeNode()
            line = self.draw_line_3d(x0, y0, z, x1, y1, z, 1, "C_BLACK")
            if color:
                line.setColorScale(color)
            line.setShaderInput("showborders", False, False,
                                False, False)
            self.geom[i] = line

            geom3d = self.geom[i+4]

            geom3d.setPos(x0, y0, z)
            b, h = [0.05, 0.05]

            x = x1 - x0
            y = y1 - y0
            #z = z - z
            vector = [x, y, 0]

            norm = np.linalg.norm(vector)
            geom3d.setScale(b, norm, h)
            geom3d.lookAt(x1, y1, z)
            geom3d.setPythonTag('select_hidden', True)
            geom3d.hide()

    def on_deselect(self):

        if self.geom:
            self.geom[0].hide()

    def on_select(self):
        if self.geom:
            self.geom[0].show()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):

        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("Level")

        iterate = False

        for entity in entities:
            if entity is not self:
                if entity.name == value:
                    iterate = True

                    if not value[:-1].endswith("_copy"):
                        value += "_copy1"
                        i = 2
                    else:
                        i = int(value[-1]) + 1

        while iterate:
            iterate = False

            for entity in entities:
                if entity is not self:
                    if entity.name == value:
                        iterate = True
                        value = value[:-1] + str(i)
                        i += 1
                        break

        self._name = value

    def delete(self):
        entities = app.model_reg.find_entities("Node")

        for ent in entities:
            if ent._plane_z is self:
                ent.plane_z = None

        super(Level, self).delete()
