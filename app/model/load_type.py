from app.model.entity import Entity, register
from app.model import Bar, Node
from app.view import draw
import numpy as np
from app import app


class LoadType(Entity):
    """
    bar: parent bar
    load_type: string  = "D", "L", "W", "S" etc.
    value: float
    """

    @staticmethod
    def create_from_object(obj):

        entity_id = obj.get("entity_id")
        name = obj.get("name")
        load_code = obj.get("load_code")
        index = obj.get("index")

        LoadType(name, load_code, entity_id, index)

    def __init__(self, name, load_code="D", set_id=None, index=None):
        super().__init__(set_id)

        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("LoadType")

        self._index = 100
        self.index = 100

        self._load_code = load_code

        self.name = name
        self.load_code = load_code

        self.show_properties("index", "name", "load_code")

        register(self)

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("LoadType")

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



    @property
    def load_code(self):
        return self._load_code

    @load_code.setter
    def load_code(self, value):

        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("LoadType")

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
