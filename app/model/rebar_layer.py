from enum import Enum

from app.model.entity import Entity, register
from app import app

from typing import TYPE_CHECKING
from typing import List

import numpy as np

from . import unit_manager
if TYPE_CHECKING:
    # Imports only for IDE type hints
    from app.model import *


class RebarLayer(Entity):

    @staticmethod
    def create_from_object(obj):

        def get(string):
            return app.model_reg.get_entity(obj.get(string))

        entity_id = obj.get("entity_id")

        with RebarSet(entity_id) as ent:
            # ent.fixed_ux = obj.get("fixed_ux")
            pass

    def __init__(self, set_id=None):
        super().__init__(set_id)
        self.diam1 = 0
        self.count1 = 0
        self.diam2 = 0
        self.count2 = 0

        self.set_prop_name(diam1="Diametro 1",
                           count1="Cantidad",
                           diam2="Diametro 2",
                           count2="Cantidad",
                           area="Area")
        self.show_properties("diam1", "count1", "diam2", "count2", "area")
        self.set_read_only("area")
        self.set_temp_properties("area")

    @property
    def area(self):

        combinated_area = self.count1 * self.diam1**2/400 + self.count2 * self.diam2**2/400
        combinated_area *= np.pi

        return combinated_area

    def __str__(self):
        area = round(self.area, 2)

        if self.count2:
            name = "{}Ø{} + {}Ø{} ({} [cm2])".format(self.count1, self.diam1, self.count2, self.diam2, area)
        else:
            name = "{}Ø{} ({} [cm2])".format(self.count1, self.diam1, area)

        return name

