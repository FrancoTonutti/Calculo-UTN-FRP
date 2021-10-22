from app.model.entity import Entity, register
from app import app

from typing import TYPE_CHECKING
from typing import List
if TYPE_CHECKING:
    # Imports only for IDE type hints
    from app.model import *

class Node(Entity):

    @staticmethod
    def create_from_object(obj):

        entity_id = obj.get("entity_id")
        x = obj.get("x")
        y = obj.get("y")
        z = obj.get("z")

        name = obj.get("name")

        with Node(x, y, z, name, entity_id) as ent:

            ent.fixed_ux = obj.get("fixed_ux")
            ent.fixed_uy = obj.get("fixed_uy")
            ent.fixed_uz = obj.get("fixed_uz")
            ent.fixed_rx = obj.get("fixed_rx")
            ent.fixed_ry = obj.get("fixed_ry")
            ent.fixed_rz = obj.get("fixed_rz")



    def __init__(self, x, y, z=0, name="", set_id=None):
        super().__init__(set_id)
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.name = name
        self.hide_properties("position")
        self.set_prop_name()
        self.show_properties("name", "x", "y", "z")
        self.index = 0

        self.fixed_ux = False
        self.fixed_uy = False
        self.fixed_uz = False

        self.fixed_rx = False
        self.fixed_ry = False
        self.fixed_rz = False

        self.loads: List[Load] = []

        self.show_properties("fixed_ux", "fixed_uz", "fixed_ry")

        self.bind_to_model("x", "y", "z", "fixed_ry", "fixed_ux", "fixed_uz")

        self.set_temp_properties("position_str", "position")

        register(self)
        self.create_model()

    def __str__(self):
        name = str(self.name)
        x = round(self.position[0], 2)
        y = round(self.position[1], 2)
        z = round(self.position[2], 2)
        return "Nodo {} ({}, {}, {})".format(name, x, y, z)

    def add_load(self, new_load):
        self.loads.append(new_load)

    def get_loads(self):
        for load_entity in self.loads:
            yield load_entity

    def create_model(self):
        print("CREATE NODE")
        self.geom = [None]
        self.geom[0] = self.load_model("data/geom/node")

        #self.geom[0].setTag('entity_type', type(Node).__name__)
        #self.geom[0].setTag('entity_id', self.entity_id)

        self.update_model()

    def update_model(self):

        ux, uz, ry = self.get_restrictions2d()

        if ry is False:
            if "node_box" in str(self.geom[0]):
                self.geom[0].removeNode()
                self.geom[0] = self.load_model("data/geom/node")
        else:
            if "node_box" not in str(self.geom[0]):
                self.geom[0].removeNode()
                self.geom[0] = self.load_model("data/geom/node_box")

        x, y, z = self.position
        self.geom[0].setPos(x, y, z)

        if ux + uz == 0 and len(self.geom) is 2:
            print("REMOVE GEOM!!!")
            geom2 = self.geom.pop()
            geom2.removeNode()

        angle = 0
        model = None
        if ux + uz == 1:
            model = "support_roller_x"
            if uz is not True:
                angle = 90
        elif ux + uz == 2:
            model = "support_pinned_x"

        self.geom[0].setR(angle)

        if model:
            if len(self.geom) is 1:
                self.geom.append(None)

            if model not in str(self.geom[1]):
                if self.geom[1]:
                    self.geom[1].removeNode()
                self.geom[1] = self.load_model("data/geom/{}".format(model), parent=self.geom[0])

        if len(self.geom) is 2:
            self.geom[1].reparentTo(self.geom[0])
            self.geom[1].setPos(0, 0, -0.2)
            self.geom[1].setScale(0.20, 0.20, 0.20)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, val):
        self.__x = round(float(val), 2)

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, val):
        self.__y = round(float(val), 2)

    @property
    def z(self):
        return self.__z

    @z.setter
    def z(self, val):
        self.__z = round(float(val), 2)

    @property
    def position(self):
        return [self.x, self.y, self.z]

    @position.setter
    def position(self, value: list):
        if isinstance(value, list) and len(value) == 3:
            x, y, z = value
            self.x = x
            self.y = y
            self.z = z

    @property
    def position_str(self):
        x, y, z = self.position
        x = round(x, 2)
        y = round(y, 2)
        z = round(z, 2)

        return "{}, {}, {}".format(x, y, z)

    @position_str.setter
    def position_str(self, value: str):
        value = value.split(",", 3)
        if len(value) is 3:
            x, y, z = value
            x = float(x)
            y = float(y)
            z = float(z)
            self.position = [x, y, z]

    def get_restrictions(self):
        restrictions = [self.fixed_ux,
                        self.fixed_uy,
                        self.fixed_uz,
                        self.fixed_rx,
                        self.fixed_ry,
                        self.fixed_rz]

        return restrictions

    def get_restrictions2d(self):
        restrictions = [self.fixed_ux,
                        self.fixed_uz,
                        self.fixed_ry]

        return restrictions
