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

        LoadType(name, load_code, entity_id)

    def __init__(self, name, load_code="D", set_id=None):
        super().__init__(set_id)
        self.name = name
        self.load_code = load_code

        register(self)
