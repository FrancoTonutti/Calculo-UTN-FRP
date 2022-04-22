""""
Example:
https://thinkmoult.com/using-ifcopenshell-parse-ifc-files-python.html

http://academy.ifcopenshell.org/creating-a-simple-wall-with-property-set-and-quantity-information/
"""
from app import app
from app.controller.console import command
import ifc_tools

import tkinter as tk
from tkinter import filedialog
from app.model import *
from app.model.profile_sections.profile_section_I import ProfileSectionI
import pint

from app.model.profile_shapes import ProfileShapeFillRect, ProfileShapeI
from app.model.section_type import SectionType
from app.model.transaction import Transaction

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Imports only for IDE type hints
    pass

from app.controller.console import command, execute


@command(name="new_file", shortcut="s")
def new_file():
    tr = Transaction()
    tr.start("Create new file")


    model = app.model_reg

    model.clear()

    View()

    concrete = MaterialGroup("Hormigón")

    types = [15, 20, 25, 30, 35, 40, 45, 50, 60]

    for h_class in types:
        E = round(4700 * (h_class ** 0.5), 2) * app.ureg("megapascal")
        #print(E)
        #print(isinstance(E, pint.quantity.Quantity))
        hor = Material("H-{}".format(h_class), concrete)
        hor.elastic_modulus = E
        hor.char_resistance = h_class * app.ureg("megapascal")
        hor.specific_weight = 22 * app.ureg("(kN)/(m**3)")

        if h_class == 30:
            hor.set_default_material()

    #w80 = ProfileSectionI(80, 46, 5.2, 3.8, 5)
    #print("Ix: {}".format(w80.inertia_x()))

    case_D = LoadCase("D", "Carga muerta", own_weight=True)
    case_L = LoadCase("L", "Sobrecarga de uso")
    case_Lr = LoadCase("Lr", "Sobrecarga de mantenimiento")
    case_W = LoadCase("W", "Viento")

    load_comb_1 = LoadCombination("A.4.1")
    load_comb_1.set_factor(case_D, 1.4)

    load_comb_2 = LoadCombination("A.4.2")
    load_comb_2.set_factor(case_D, 1.2)
    load_comb_2.set_factor(case_L, 1.6)
    load_comb_2.set_factor(case_Lr, 0.5)

    load_comb_3a = LoadCombination("A.4.3.a")
    load_comb_3a.set_factor(case_D, 1.2)
    load_comb_3a.set_factor(case_Lr, 1.6)
    load_comb_3a.set_factor(case_L, 0.5)

    load_comb_3b = LoadCombination("A.4.3.b")
    load_comb_3b.set_factor(case_D, 1.2)
    load_comb_3b.set_factor(case_Lr, 1.6)
    load_comb_3b.set_factor(case_W, 0.8)

    load_comb_4 = LoadCombination("A.4.4")
    load_comb_4.set_factor(case_D, 1.2)
    load_comb_4.set_factor(case_W, 1.6)
    load_comb_4.set_factor(case_L, 0.5)
    load_comb_4.set_factor(case_Lr, 0.5)

    load_comb_6 = LoadCombination("A.4.6")
    load_comb_6.set_factor(case_D, 0.8)
    load_comb_6.set_factor(case_W, 1.6)

    sec_type = SectionType("Rectangular")
    shapes = sec_type.valid_values_shape()
    for shape in shapes:
        if isinstance(shape, ProfileShapeFillRect):
            sec_type.shape = shape

    Section("20/30", sec_type, {"bw": "20 cm", "h": "30 cm"})

    sec_type = SectionType("IPN")
    shapes = sec_type.valid_values_shape()
    for shape in shapes:
        if isinstance(shape, ProfileShapeI):
            sec_type.shape = shape

    Section("IPN 300", sec_type, {"d": "300 mm",
                                  "bf": "125 mm",
                                  "tf": "16.2 mm",
                                  "hw": "241 mm",
                                  "tw": "10.8 mm",
                                  "r1": "10.8 mm",
                                  "r2": "6.5 mm"})



    tr.commit()

    execute("regen")

