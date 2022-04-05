from app.model.entity import Entity, register
from app.model import Bar, Node
from app.view import draw
import numpy as np
from app import app


class LoadCase(Entity):
    """
    bar: parent bar
    load_type: string  = "D", "L", "W", "S" etc.
    value: float
    """

    @staticmethod
    def create_from_object(obj):

        entity_id = obj.get("entity_id")
        description = obj.get("description")
        load_code = obj.get("load_code")
        index = obj.get("index")
        own_weight = obj.get("own_weight")

        return LoadCase(load_code, description, entity_id, index, own_weight)

    def __init__(self,  load_code="D", description="", set_id=None, index=None, own_weight=False):
        super().__init__(set_id)

        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("LoadCase")

        if index:
            self._index = index
        else:
            self._index = 1
            self.index = 100

        #self._load_code = load_code
        self.load_code = load_code

        self.description = description
        self.load_code = load_code
        self.own_weight = own_weight


        self.show_properties("index", "name", "load_code", "own_weight")

        register(self)

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("LoadCase")

        sorted_entities = []
        for entity in entities:
            if entity is not self:
                sorted_entities.append(entity)

        sorted_entities = sorted(sorted_entities, key=lambda x: x.index)

        value = max(value, 1)

        if value <= len(sorted_entities):
            sorted_entities.insert(value-1, self)
        else:
            sorted_entities.append(self)

        i = 1
        for entity in sorted_entities:
            entity._index = i
            i += 1

    def delete(self):
        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("LoadCombination")

        for entity in entities:

            if self.entity_id in entity.factors.keys():
                entity.factors.pop(self.entity_id)

        return super(LoadCase, self).delete()

    @property
    def load_code(self):
        return self._load_code

    @load_code.setter
    def load_code(self, value):

        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("LoadCase")

        iterate = False

        for entity in entities:
            if entity is not self:
                if entity.load_code == value:
                    iterate = True

                    if not value[:-1].endswith("_copy"):
                        value += "_copy1"
                        i = 2
                    else:
                        i = int(value[-1])+1

        while iterate:
            iterate = False

            for entity in entities:
                if entity is not self:
                    if entity.load_code == value:
                        iterate = True
                        value = value[:-1] + str(i)
                        i += 1
                        break


        self._load_code = value
