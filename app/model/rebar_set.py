from enum import Enum

from app.model.entity import Entity, register
from app import app

from typing import TYPE_CHECKING
from typing import List

from . import unit_manager
if TYPE_CHECKING:
    # Imports only for IDE type hints
    from app.model import *


class RebarLocation(Enum):
    LOWER = 0
    UPPER = 1
    SKIN = 2


class RebarSet(Entity):

    @staticmethod
    def create_from_object(obj):

        def get(string):
            return app.model_reg.get_entity(obj.get(string))

        entity_id = obj.get("entity_id")

        parent = get("parent")

        name = obj.get("name")
        start = obj.get("start")
        end = obj.get("end")

        location = obj.get("location")

        with RebarSet(parent, name, location, entity_id) as ent:
            # ent.fixed_ux = obj.get("fixed_ux")
            ent.start = app.ureg(obj.get("start").replace("%", "percent"))
            ent.end = app.ureg(obj.get("end").replace("%", "percent"))
            ent.shape_code = obj.get("shape_code")


            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!percent")

            print(obj.get("start"))
            print(obj.get("start").replace("%", "percent"))
            print(app.ureg(obj.get("start").replace("%", "percent")))

            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!percent")

    def __init__(self, parent, name, location, set_id=None):
        super().__init__(set_id)
        self.name = name
        self.start = 0 * app.ureg("percent")
        self.end = 100 * app.ureg("percent")

        #self.cc = 2 * unit_manager.ureg("cm")
        self._layers = 1

        self.set_prop_name(name="Nombre", parent_lenght="Longitud anfitrión", start="Inicio", end="Fin", cc="Recubrimiento", layers="Capas")
        self.show_properties("name", "parent_lenght", "start", "end", "cc", "layers")

        self.location = RebarLocation(location)

        self.set_prop_name(location="Ubicación")
        self.show_properties("location")
        #self.set_read_only("location")

        self.shape_code = 0
        self.set_prop_name(shape_code="Código de forma")
        self.show_properties("shape_code")

        self.set_read_only("parent_lenght")
        self.set_temp_properties("parent_lenght", "cc")
        self._parent = None
        self.parent = parent

        self.layer1 = ""
        self.layer2 = ""
        self.layer3 = ""

        self.set_prop_name(layer1="Capa 1", layer2="Capa 2", layer3="Capa 3")

        self.layers = 1

    @property
    def parent(self):
        return self._parent

    @property
    def parent_lenght(self):
        return round(self.parent.longitude(), 2) * unit_manager.default_ureg("longitude")

    @parent.setter
    def parent(self, value):
        self._parent = value
        self._parent.rebar_sets.append(self)

    @property
    def layers(self):
        return self._layers

    @layers.setter
    def layers(self, value):
        value = max(value, 1)
        value = min(value, 3)

        for i in range(1, 4):
            if i<= value:
                self.show_properties("layer%s" % i)
            else:
                self.hide_properties("layer%s" % i)

        self._layers = value

    @property
    def cc(self):
        return self._parent.cc

    @cc.setter
    def cc(self, value):
        self._parent.cc = value




