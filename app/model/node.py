from app.model.entity import Entity, register
from app import app

from typing import TYPE_CHECKING
from typing import List

from .entity_reference import EntityReference

if TYPE_CHECKING:
    # Imports only for IDE type hints
    from app.model import *
from . import unit_manager

class Node(Entity):

    @staticmethod
    def create_from_object(obj):

        entity_id = obj.get("entity_id")
        x = obj.get("x")
        y = obj.get("y")
        z = obj.get("z")

        name = obj.get("name")

        new_node = Node(x, y, z, name, entity_id)

        new_node.fixed_ux = obj.get("fixed_ux")
        new_node.fixed_uy = obj.get("fixed_uy")
        new_node.fixed_uz = obj.get("fixed_uz")
        new_node.fixed_rx = obj.get("fixed_rx")
        new_node.fixed_ry = obj.get("fixed_ry")
        new_node.fixed_rz = obj.get("fixed_rz")
        new_node.plane_z = obj.get("plane_z")

        return new_node

    def __init__(self, x, y, z=0, name="", set_id=None):
        super().__init__(set_id)
        self._plane_z = None

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

        self.show_properties("plane_z")
        self.bind_to_model("plane_z")
        self.set_prop_name(plane_z="Plano Z")

        self.set_combo_box_properties("plane_z")

        register(self)
        self.create_model()

    def __str__(self):
        name = str(self.name)
        x = round(self.position[0], 2)
        y = round(self.position[1], 2)
        z = round(self.position[2], 2)
        return "Nodo {} ({}, {}, {})".format(name, x, y, z)

    @property
    def plane_z(self):
        return str(self._plane_z)

    @plane_z.setter
    def plane_z(self, value):

        if (not value) and self._plane_z:
            self._plane_z.remove_child_model(self)
            self._plane_z = None
            self.unset_read_only("z")

        if isinstance(value, EntityReference):
            value = value.__reference__

        # Obtenemos el registro del modelo
        if isinstance(value, str):
            entities = app.model_reg.find_entities("Level")

            for ent in entities:
                if ent.name == value:
                    self._plane_z = ent
                    self._plane_z.add_child_model(self)
                    self.set_read_only("z")
        elif isinstance(value, Entity):
            if value.category_name == "Level":
                self._plane_z = value
                self._plane_z.add_child_model(self)
                self.set_read_only("z")

    @staticmethod
    def valid_values_plane_z():
        # Obtenemos el registro del modelo
        entities = app.model_reg.find_entities("Level")

        values = [None]

        for ent in entities:
            values.append(ent.name)

        return values

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

        self.geom[0].setScale(0.50, 0.50, 0.50)

        if len(self.geom) is 2:
            self.geom[1].reparentTo(self.geom[0])
            self.geom[1].setPos(0, 0, -0.2)
            self.geom[0].setScale(0.8, 0.80, 0.80)
            self.geom[1].setScale(0.20, 0.20, 0.20)

    def delete(self):
        if self.transaction_check():
            for child in self.get_child_models():
                child.delete()

            super(Node, self).delete()



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

    '''@property
    def z(self):
        return self.__z

    @z.setter
    def z(self, val):
        self.__z = round(float(val), 2)'''

    @property
    def z(self):
        if self._plane_z:
            self.__z = unit_manager.convert_to_m(self._plane_z.z)

        return self.__z

    @z.setter
    def z(self, value):
        if self._plane_z is None:
            self.__z = round(float(value), 2)
        else:
            self.__z = unit_manager.convert_to_m(self._plane_z.z)

    @property
    def position(self):
        return [self.x, self.y, self.z]

    @position.setter
    def position(self, value: list):
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
