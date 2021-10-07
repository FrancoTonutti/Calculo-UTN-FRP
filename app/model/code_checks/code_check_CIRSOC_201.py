import math

from app.model.entity import Entity
from typing import TYPE_CHECKING
from typing import List
from app import app

from app.model import unit_manager

if TYPE_CHECKING:
    # Imports only for IDE type hints
    from app.model import *


class CodeCheckCIRSOC201(Entity):

    @staticmethod
    def create_from_object(obj):
        pass

    def __init__(self, set_id=None):
        super().__init__(set_id)
        self.name = None

    @staticmethod
    def verify_column(element):
        return "Verificación no implementada"

    @staticmethod
    def verify_beam(element):
        """

        Parameters
        ----------
        element : Bar
        """
        log = "####### %s #######\n\n" % str(element)

        mat = element.material
        fc = unit_manager.convert_to_MPa(mat.char_resistance)
        fy = 420

        bw, h = element.section.size

        cc = 0.02
        dbe = 0.006
        db = 0.01

        d = h - cc - dbe - db/2

        if fc <= 30:
            beta1 = 0.85
        else:
            beta1 = max(0.85 - 0.05 * (fc-30)/7, 0.65)

        Mu = 0

        combinations = app.model_reg.find_entities("LoadCombination")

        max_value = 0
        min_value = 0
        max_combination = None
        min_combination = None

        for combination in combinations:
            v_moment = element.get_analysis_results(combination, "v_moment")
            if v_moment is not None:
                for pos, value in v_moment:
                    if value >= max_value:
                        max_value = value
                        max_combination = combination

                    if value <= min_value:
                        min_value = value
                        min_combination = combination

        if not max_combination:
            return log

        log += "h = %s [m]\n" % round(h, 2)
        log += "bw = %s [m]\n" % round(bw, 2)
        log += "d = %s [m]\n\n" % round(d, 3)

        log += "f'c = %s [MPa]\n" % round(fc, 2)
        log += "fy = %s [MPa]\n\n" % round(fy, 2)



        Mu = max_value

        Mn = Mu/0.9

        log += "Mu = {} [kNm] ({})\n".format(round(Mu, 2), max_combination.equation)
        log += "Mn = %s [kNm]\n\n" % round(Mn, 2)

        mn = Mn/(0.85 * (fc * 1000) * bw * d**2)

        log += "mn = %s [MPa]\n\n" % round(mn, 5)

        if 1 - 2 * mn >= 0:
            Ka = 1 - math.sqrt(1 - 2 * mn)
        else:
            Ka = 1
        log += "Ka = %s\n" % round(Ka, 4)

        """
        ec = 0.003
        es = 0.005
        kc_max = ec / (ec + es)
        kc_max = 0.375
        
        Ka_max = kc_max * beta1
        """
        Ka_min = 1.4/(0.85 * fc)
        Ka_max = 0.375 * beta1

        log += "Ka_min = %s\n" % round(Ka_min, 4)
        log += "Ka_max = %s\n\n" % round(Ka_max, 4)

        Ka = max(Ka, Ka_min)

        if Ka < Ka_max:
            """Armadura simple"""

            As = fc * bw * Ka * d/fy * (100**2)  # [cm2]
            log += "As = %s [cm2]\n" % round(Ka_max, 2)

        else:
            """Armadura doble"""

            log += "Armadura doble"

        log += "\n##############"

        return log


