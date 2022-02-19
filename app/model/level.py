import numpy as np

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

        with Node(z, name, entity_id) as ent:
            pass

    def __init__(self, z, name="Nivel", set_id=None):
        super().__init__(set_id)
        self.z: float = z
        self.name = name

        self.show_properties("z", "name")
        self.set_prop_name(z="Altura", name="Nombre")
        self.set_units(z="m")

        self.bind_to_model("z")

        self.create_model()

    def create_model(self):
        print("CREATE model level")
        self.geom = [None]*9

        '''self.geom[0] = self.load_model("data/geom/square")
        self.geom[0].set_two_sided(True)
        self.geom[0].setHpr(0, 90, 0)
        self.geom[0].setLightOff()'''

        #self.geom[0].setTag('entity_type', type(Node).__name__)
        #self.geom[0].setTag('entity_id', self.entity_id)

        self.geom[5] = self.load_model("data/geom/beam")
        self.geom[6] = self.load_model("data/geom/beam")
        self.geom[7] = self.load_model("data/geom/beam")
        self.geom[8] = self.load_model("data/geom/beam")




        self.update_model()

    def update_model(self):
        #self.geom[0].reparentTo(self.geom[0])
        z = unit_manager.convert_to_m(self.z)
        #self.geom[0].setPos(0, 0, z)
        #self.geom[0].setScale(1, 1, 1)

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

            line = self.geom[i]
            if line is not None:
                line.removeNode()
            line = self.draw_line_3d(x0, y0, z, x1, y1, z, 1, "C_BLACK")

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





