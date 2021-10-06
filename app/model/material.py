from app.model.entity import Entity
from typing import TYPE_CHECKING
from typing import List
from app import app

if TYPE_CHECKING:
    # Imports only for IDE type hints
    from app.model import *

class Material(Entity):

    @staticmethod
    def create_from_object(obj):

        def get(string):
            return app.model_reg.get_entity(obj.get(string))

        name = obj.get("name")

        print("create_from_object material_group1 {}".format(obj.get("material_group")))
        group = get("material_group")
        print("create_from_object material_group2 {}".format(
            group))
        entity_id = obj.get("entity_id")
        elastic_modulus = app.ureg(obj.get("elastic_modulus"))
        is_default_material = obj.get("is_default_material")

        with Material(name, group, elastic_modulus, entity_id) as ent:
            if is_default_material:
                ent.set_default_material()

            ent.char_resistance = app.ureg(obj.get("char_resistance"))

    def __init__(self, name, group, elastic_modulus=None, set_id=None):
        super().__init__(set_id)
        self.elastic_modulus = elastic_modulus
        self._material_group = None
        self.material_group = group

        self._name = None
        self.name = name

        entities = app.model_reg.find_entities("Material")
        if len(entities) == 1:
            self.set_default_material()

        self.char_resistance = 0

        self.show_properties("name", "elastic_modulus", "char_resistance")
        self.set_prop_name(elastic_modulus="Modulo Elástico E", char_resistance="Resistencia f'c")


    def __str__(self):
        if self.material_group:
            return "{}: {}".format(self.material_group.name, self.name)
        else:
            return "No group: {}".format(self.name)

    @property
    def material_group(self):
        return self._material_group

    @material_group.setter
    def material_group(self, group):
        if not group or isinstance(group, str):
            print("Material group: {}".format(group))
        else:
            reset_name = False
            if self._material_group:
                reset_name = True
                self._material_group.remove_material(self)

            group.add_material(self)
            self._material_group = group
            if reset_name:
                self.name = self._name

    def set_default_material(self):
        app.default_material = self

    def delete(self, force_delete=False):

        if self.is_default_material:
            model_reg = app.model_reg
            entities = model_reg.find_entities("Material")

            for entity in entities:
                if entity is not self:
                    entity.set_default_material()
                    break
            else:
                # Prevent for delete last material
                if not force_delete:
                    return False
                else:
                    app.default_material = None

        if self._material_group:
            self._material_group.remove_material(self)

        super(Material, self).delete()

    @property
    def is_default_material(self):
        return self is app.default_material

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):

        if not value:
            value = "Sin nombre"

        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("Material")

        filtered_entities = filter(lambda x: x.material_group is self.material_group, entities)
        filtered_entities = list(filtered_entities)

        iterate = False

        i = 2

        for entity in filtered_entities:
            if entity is not self:
                if entity.name == value:
                    iterate = True

                    if not value[:-1].endswith("_copy"):
                        value += "_copy1"
                        i = 2
                    else:
                        i = int(value[-1])+1

        while iterate:
            iterate = False

            for entity in filtered_entities:
                if entity is not self:
                    if entity.name == value:
                        iterate = True
                        value = value[:-len(str(i-1))] + str(i)
                        i += 1
                        break

        self._name = value