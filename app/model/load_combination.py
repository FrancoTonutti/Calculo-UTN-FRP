from app.model.entity import Entity, register
from app.model import Bar, Node
from app.view import draw
import numpy as np
from app import app


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
        equation = obj.get("equation")
        index = obj.get("index")

        LoadCombination(name, equation, entity_id, index)

    def __init__(self, name, equation="D", set_id=None, index=None):
        super().__init__(set_id)

        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("LoadCombination")

        if not index:
            self.index = len(entities)
        else:
            self.index = int(index)

        self.name = name
        self.equation = equation

        self.show_properties("index", "name", "equation")

        register(self)
