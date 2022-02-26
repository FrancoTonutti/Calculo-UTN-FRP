from app.model.bar import Bar
import numpy as np
from app.view import draw
from app import app
from .material import Material

from typing import TYPE_CHECKING
from typing import List

if TYPE_CHECKING:
    # Imports only for IDE type hints
    from app.model import *


class Beam(Bar):

    @staticmethod
    def create_from_object(obj):
        print("intentando crear desde objeto")

        def get(string):
            return app.model_reg.get_entity(obj.get(string))

        start = get("start")
        end = get("end")
        sec = get("section")
        mat = get("material")
        entity_id = obj.get("entity_id")
        name = obj.get("name")

        bar = Bar(start, end, sec, mat, entity_id)
        bar.name = name

        return bar

    def __init__(self, start, end, section, material=None, set_id=None):
        super().__init__(start, end, section, material, set_id)