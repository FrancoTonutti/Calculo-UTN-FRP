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
import pint

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Imports only for IDE type hints
    pass

from app.controller.console import command, execute


@command(name="new_file", shortcut="s")
def new_file():


    model = app.model_reg

    model.clear()

    concrete = MaterialGroup("Hormigón")

    types = [15, 20, 25, 30, 35, 40, 45, 50, 60]

    for h_class in types:
        E = round(4700 * (h_class ** 0.5), 2) * app.ureg("megapascal")
        print(E)
        print(isinstance(E, pint.quantity.Quantity))
        hor = Material("H-{}".format(h_class), concrete, E)
        hor.char_resistance = h_class * app.ureg("megapascal")

        if h_class == 30:
            hor.set_default_material()

    execute("regen")
