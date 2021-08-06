from app.model.entity import Entity, register
from app.model import Bar, Node
from app.view import draw
import numpy as np
from app import app
from app.model.load_type import LoadType

class LoadCombination(Entity):
    """
    bar: parent bar
    load_type: string  = "D", "L", "W", "S" etc.
    value: float
    """

    @staticmethod
    def create_from_object(obj):

        entity_id = obj.get("entity_id")
        name = obj.get("name")
        index = obj.get("index")

        LoadCombination(name, entity_id, index)

    def __init__(self, name, set_id=None, index=None):
        super().__init__(set_id)

        if index:
            self._index = index
        else:
            self._index = 100
            self.index = 100

        self.name = name

        self.factors = dict()

        self.show_properties("index", "name", "equation")
        self.set_read_only("equation")

        register(self)

    def set_factor(self, load: LoadType, factor: float):
        self.factors.update({load.entity_id: factor})

    def get_factor(self, load: LoadType):
        return self.factors.get(load.entity_id, 0.0)

    @property
    def equation(self):
        eq = ""

        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("LoadType")

        sorted_entities = []
        for entity in entities:
            sorted_entities.append(entity)

        sorted_entities = sorted(sorted_entities, key=lambda x: x.index)

        for entity in sorted_entities:
            factor = self.get_factor(entity)
            if factor > 0:
                if eq != "":
                    eq += " + "
                eq += "{} {}".format(factor, entity.load_code)

        return eq

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("LoadCombination")

        sorted_entities = []
        for entity in entities:
            if entity is not self:
                sorted_entities.append(entity)

        sorted_entities = sorted(sorted_entities, key=lambda x: x.index)

        value = max(value, 1)

        if value <= len(sorted_entities):
            sorted_entities.insert(value - 1, self)
        else:
            sorted_entities.append(self)

        i = 1
        for entity in sorted_entities:
            entity._index = i
            i += 1

    def __setattr__(self, key, value):
        '''try:
            super().__setattr__(key, value)
        except AttributeError as ex:
            panda3d = app.get_show_base()
            # Obtenemos el registro del modelo
            model_reg = app.model_reg
            entities = model_reg.find_entities("LoadType")
            for entity in entities:
                if entity.load_code == key:
                    print("set_factor")
                    self.set_factor(entity, value)
                    break
            else:
                raise AttributeError(ex)'''

        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("LoadType")
        for entity in entities:
            if entity.load_code == key:
                print("set_factor")
                self.set_factor(entity, value)
                break
        else:
            super().__setattr__(key, value)


    def __getattr__(self, key):
        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("LoadType")
        for entity in entities:
            if entity.load_code == key:
                return self.get_factor(entity)

        else:
            ex = "Attributo no encontrado {}".format(key)
            raise AttributeError(ex)


