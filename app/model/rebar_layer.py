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

        diam1 = obj.get("diam1")
        count1 = obj.get("count1")
        diam2 = obj.get("diam2")
        count2 = obj.get("count2")

        ent = RebarLayer(entity_id)

        ent.diam1 = diam1
        ent.count1 = count1
        ent.diam2 = diam2
        ent.count2 = count2
        ent.parent = get("parent")

        return ent

    def __init__(self, set_id=None):
        super().__init__(set_id)
        self.diam1 = 0
        self.count1 = 0
        self.diam2 = 0
        self.count2 = 0

        self.parent = None

        self.set_prop_name(diam1="Diametro 1",
                           count1="Cantidad",
                           diam2="Diametro 2",
                           count2="Cantidad",
                           area="Area",
                           is_valid="Capa valida")
        self.show_properties("diam1", "count1", "diam2", "count2", "area", "is_valid")
        self.set_read_only("area", "is_valid")
        self.set_temp_properties("area", "is_valid")



    @property
    def area(self):

        combinated_area = self.count1 * self.diam1**2/400 + self.count2 * self.diam2**2/400
        combinated_area *= np.pi
        combinated_area = round(combinated_area, 2)

        return combinated_area

    def __str__(self):
        area = round(self.area, 2)

        if self.count2:
            name = "{}Ø{} + {}Ø{} ({} [cm2])".format(self.count1, self.diam1, self.count2, self.diam2, area)
        else:
            name = "{}Ø{} ({} [cm2])".format(self.count1, self.diam1, area)

        return name

    @property
    def is_valid(self):
        if self.parent:
            n1 = self.count1
            n2 = self.count2
            cc = self.parent.parent.cc
            cc = unit_manager.convert_to_mm(cc)
            dbe = 6

            reinforcement_width = n1 * self.diam1 + n2 * self.diam2 + cc * 2 + max(n1 + n2 - 1, 0) * 25 + 2*dbe

            bw, h = self.parent.parent.section.size

            if reinforcement_width/10 <= bw*100:
                return "True: {} [cm] <= {} [cm]".format( reinforcement_width/10, bw*100)
            else:

                return "False: {} [cm] > {} [cm]".format( reinforcement_width/10, bw*100)
        else:
            return "No parent setted"
