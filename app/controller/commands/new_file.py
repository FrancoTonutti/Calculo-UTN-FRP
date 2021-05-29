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


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Imports only for IDE type hints
    pass

from app.controller.console import command, execute


@command(name="new_file", shortcut="s")
def new_file():
    model = app.model_reg

    model.clear()
    execute("regen")



