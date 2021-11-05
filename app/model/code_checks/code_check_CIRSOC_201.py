import math

from panda3d.core import Texture, SamplerState

from app.model.entity import Entity
from typing import TYPE_CHECKING
from typing import List
from app import app
from app.model.rebar_set import RebarType, RebarLocation

import numpy as np

from app.model import unit_manager

if TYPE_CHECKING:
    # Imports only for IDE type hints
    from app.model import *

# importing image object from PIL
import math
from PIL import Image, ImageDraw, ImageFilter


def apply_scale(val, scale, min_val=1):
    val *= scale
    val = max(round(val), min_val)
    return int(val)


class CodeCheckCIRSOC201(Entity):

    @staticmethod
    def create_from_object(obj):
        pass

    def __init__(self, set_id=None):
        super().__init__(set_id)
        self.name = None
        self.enabled_save = False

        self.reinforcement_bars = {
            6: {
                "diameter": 0.6,
                "area": np.pi * 0.3 ** 2,
                "cost": 740/12
            },
            8: {
                "diameter": 0.8,
                "area": np.pi * 0.4 ** 2,
                "cost": 1205/12
            },
            10: {
                "diameter": 1,
                "area": np.pi * 0.5 ** 2,
                "cost": 1932/12
            },
            12: {
                "diameter": 1.2,
                "area": np.pi * 0.6 ** 2,
                "cost": 2600/12
            },
            16: {
                "diameter": 1.6,
                "area": np.pi * 0.8 ** 2,
                "cost": 5000/12
            },
            20: {
                "diameter": 2,
                "area": np.pi * 1 ** 2,
                "cost": 6600/12
            }
        }

    @staticmethod
    def verify_column(element):
        return "Verificación no implementada"

    def generate_rebar_image(self, element, scale):

        draw_color = (255, 255, 255)

        bw, h = element.section.size
        bw = apply_scale(bw, scale)
        h = apply_scale(h, scale)
        cc = unit_manager.convert_to_m(element.cc)
        cc = apply_scale(cc, scale)


        shape = [(0, 0), (bw-1 , h -1)]

        # creating new Image object
        img = Image.new("RGBA", (256, 256), (255, 255, 255, 0))

        # create rectangle image
        img1 = ImageDraw.Draw(img)
        img1.rectangle(shape, fill=(255, 255, 255, 0), outline=draw_color, width=1)


        #img1.rectangle(shape, fill=(255, 0, 0, 0), outline=draw_color, width=1)

        radius = self.rebar_hook_diameter(6)/2000
        dbe = apply_scale(0.006, scale)
        radius = apply_scale(radius, scale)
        shape = [(cc, cc), (bw - cc - dbe, h - cc - dbe)]

        img1.rounded_rectangle(shape, radius, fill=(255, 255, 255, 0), outline=draw_color, width=dbe)

        shape = [(bw - 2*radius - cc - dbe, cc), (bw - cc - dbe, cc + 2*radius +dbe-1)]
        img1.arc(shape, 180+45, 45, fill=draw_color, width=dbe)


        hook_len = 5

        shape = [(bw - cc - 1.7071*radius - dbe, cc + dbe), (bw - cc - 1.7071*radius - dbe - hook_len, cc+ dbe +hook_len)]
        img1.line(shape, fill=draw_color, width=dbe)

        shape = [(bw - cc - dbe-1, cc + dbe + 1.7071 * radius),
                 (bw - cc - dbe - hook_len-1, cc + dbe + 1.7071 * radius + hook_len)]
        img1.line(shape, fill=draw_color, width=dbe)

        for rebar in element.rebar_sets:
            if rebar.rebar_type is RebarType.DEFAULT:
                if rebar.location is RebarLocation.UPPER:

                    if rebar.layer1:

                        b = bw - 2*cc - 2 * dbe - scale*rebar.layer1.diam1/1000 - radius*0.8 -1

                        count_bars = rebar.layer1.count1 + rebar.layer1.count2

                        spacing = b / (count_bars - 1)
                        db0 = int(math.ceil(
                            rebar.layer1.diam1 / 1000 * scale))

                        for i in range(count_bars):

                            if i<rebar.layer1.count1/2 or i>= rebar.layer1.count1/2 +rebar.layer1.count2:
                                db = int(math.ceil(
                                    rebar.layer1.diam1/1000 * scale))
                            else:
                                db = int(math.ceil(
                                    rebar.layer1.diam2 / 1000 * scale))



                            self.draw_bar(img1,
                                          cc + dbe + radius * 0.4 + db0 / 2 + i * spacing,
                                          cc + dbe + db / 2 + radius * 0.4, db,
                                          draw_color)

                elif rebar.location is RebarLocation.LOWER:
                    if rebar.layer1:

                        if isinstance(rebar.layer1.diam1, str):
                            print("layer1.diam1", rebar.layer1.diam1)

                        b = bw - 2 * cc - 2 * dbe - scale * rebar.layer1.diam1 / 1000 - radius * 0.8 - 1

                        count_bars = rebar.layer1.count1 + rebar.layer1.count2

                        spacing = b / (count_bars - 1)
                        db0 = int(math.ceil(
                            rebar.layer1.diam1 / 1000 * scale))

                        for i in range(count_bars):

                            if i < rebar.layer1.count1 / 2 or i >= rebar.layer1.count1 / 2 + rebar.layer1.count2:
                                db = int(math.ceil(
                                    rebar.layer1.diam1 / 1000 * scale))
                            else:
                                db = int(math.ceil(
                                    rebar.layer1.diam2 / 1000 * scale))

                            self.draw_bar(img1,
                                          cc + dbe + radius * 0.4 + db0 / 2 + i * spacing,
                                          h - cc - dbe - db / 2 - radius * 0.4, db,
                                          draw_color)






        #img1.ellipse((5, 5, 8, 8), fill=draw_color, outline=draw_color)

        #img = img.filter(ImageFilter.DETAIL)

        data = img.convert("RGBA").tobytes("raw", "RGBA")
        newtex = Texture('movie')
        newtex.setup2dTexture(256, 256, Texture.TUnsignedByte, Texture.F_rgba32)
        newtex.setRamImageAs(data, "RGBA")
        newtex.setMagfilter(SamplerState.FT_nearest_mipmap_nearest)

        return newtex

    def draw_bar(self, draw, x, y, db, color):
        shape = [(x-db/2, y-db/2),
                 (x+db/2, y+db/2)]
        draw.ellipse(shape, fill=color, outline=color)

    def rebar_hook_diameter(self, db_mm):

        if db_mm <= 25:
            d = 6 * db_mm
        elif db_mm <= 32:
            d = 8 * db_mm
        else:
            d = 10 * db_mm

        return d

    def verify_beam(self, element):
        """

        Parameters
        ----------
        element : Bar
        """
        log = ""

        rebar_sets = element.rebar_sets

        mat = element.material
        fc = unit_manager.convert_to_MPa(mat.char_resistance)
        fy = 420

        bw, h = element.section.size

        cc = unit_manager.convert_to_m(element.cc)
        dbe = 0.006
        db = 0.02

        d = h - cc - dbe - db/2

        d = math.floor(d * 100)/100



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

        min_value = round(min_value, 5)

        if not max_combination:
            log += "No se encontraron resultados del cálculo"
            return log



        log_rebar1, options_rebar1 = self.calculate_rebar(h, bw, d, fc, fy, max_value, max_combination.equation, element)
        log_rebar2, options_rebar2 = self.calculate_rebar(h, bw, d, fc, fy,
                                                        abs(min_value),
                                                        min_combination.equation,
                                                        element)
        log += log_rebar1

        enable = False

        if enable:

            for rebar in rebar_sets:
                if rebar.rebar_type is RebarType.DEFAULT:
                    if rebar.location is RebarLocation.LOWER and options_rebar1:
                        rebar.layer1.diam1 = options_rebar1[0]["diam1"]
                        rebar.layer1.count1 = options_rebar1[0]["count1"]
                        rebar.layer1.diam2 = options_rebar1[0]["diam2"]
                        rebar.layer1.count2 = options_rebar1[0]["count2"]


                    elif rebar.location is RebarLocation.UPPER and options_rebar2:
                        if min_value<0:
                            rebar.layer1.diam1 = options_rebar2[0]["diam1"]
                            rebar.layer1.count1 = options_rebar2[0]["count1"]
                            rebar.layer1.diam2 = options_rebar2[0]["diam2"]
                            rebar.layer1.count2 = options_rebar2[0]["count2"]
                        else:
                            rebar.layer1.diam1 = 10
                            rebar.layer1.count1 = 2
                            rebar.layer1.diam2 = 0
                            rebar.layer1.count2 = 0


        return log

    def calculate_rebar(self, h, bw, d, fc, fy, Mu, equation, element):

        log = ""

        log += "h = %s [m]\n" % round(h, 2)
        log += "bw = %s [m]\n" % round(bw, 2)
        log += "d = %s [m]\n\n" % round(d, 3)

        log += "f'c = %s [MPa]\n" % round(fc, 2)
        log += "fy = %s [MPa]\n\n" % round(fy, 2)

        Mn = Mu/0.9

        log += "Mu = {} [kNm] ({})\n".format(round(Mu, 2), equation)
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
        if fc <= 30:
            beta1 = 0.85
        else:
            beta1 = max(0.85 - 0.05 * (fc-30)/7, 0.65)

        Ka_min = 1.4/(0.85 * fc)
        Ka_max = 0.375 * beta1

        log += "Ka_min = %s\n" % round(Ka_min, 4)
        log += "Ka_max = %s\n\n" % round(Ka_max, 4)

        Ka = max(Ka, Ka_min)

        options = []

        if Ka < Ka_max:
            """Armadura simple"""

            As = 0.85 * fc * bw * Ka * d/fy * (100**2)  # [cm2]
            log += "As = %s [cm2]\n\n" % round(As, 2)

            options = self.generate_reinforcement(As, bw, 2.5, 2.5)

            for option in options:
                total_cost = round(option.get("cost")*element.longitude(), 2)
                log += "{} - ${}\n".format(option.get("data"), total_cost)

        else:
            """Armadura doble"""

            log += "Armadura doble"

        log += "\n##############"

        return log, options

    def generate_reinforcement(self, area, width, tmn, cc):
        options = list()

        for size, data in self.reinforcement_bars.items():

            diam1 = data.get("diameter")
            area1 = data.get("area")
            n = 2

            while n*data.get("area") < area:

                for size2, data2 in self.reinforcement_bars.items():
                    diam2 = data2.get("diameter")
                    area2 = data2.get("area")


                    if size2 is size:
                        continue

                    if diam1 < diam2:
                        continue

                    n2 = 1

                    combinated_area = n * area1 + n2 * area2

                    while combinated_area < area:
                        n2 += 1
                        combinated_area = n * area1 + n2 * area2

                    combinated_area = round(combinated_area, 2)
                    combinated_cost = n * data.get("cost") + n2 * data2.get("cost")
                    # reinforcement_width = n * data.get("diameter") + n2 * data2.get("diameter") + cc * 2 + (n + n2-1) *2.5

                    if self.is_valid_layer(width*100, cc, diam1, n, diam2, n2):
                        rebar = "{}Ø{} + {}Ø{} ({} [cm2])".format(n, size, n2, size2, combinated_area)
                        options.append({"data": rebar, "cost": combinated_cost, "diam1": size, "count1": n, "diam2": size2, "count2": n2})

                n += 1

            #reinforcement_width = n * data.get("diameter") + cc * 2 + (n - 1) * 2.5
            #if reinforcement_width <= width * 100:

            if self.is_valid_layer(width*100, cc, diam1, n):
                rebar = "{}Ø{} ({} [cm2])".format(n, size, round(n*data.get("area"), 2))
                options.append({"data": rebar, "cost": n*data.get("cost"), "diam1": size, "count1": n, "diam2": None, "count2": None})

        options = sorted(options, key=lambda x: x["cost"])

        return options

    @staticmethod
    def is_valid_layer(bw, cc, diam1, n1, diam2=0, n2=0, max_layers=2):
        reinforcement_width = n1 * diam1 + n2 * diam2 + cc * 2 + (n1 + n2 - 1) * 2.5

        if reinforcement_width > bw and n2 == 0:

            pass

        return reinforcement_width <= bw





