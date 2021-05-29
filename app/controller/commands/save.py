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

import time
import tempfile
import ifcopenshell

O = 0., 0., 0.
X = 1., 0., 0.
Y = 0., 1., 0.
Z = 0., 0., 1.


@command(name="save", shortcut="s")
def save():
    print("----------------------------------------------------")
    print("save()")
    root = tk.Tk()
    root.withdraw()

    filename = "myfile.json"

    filename = filedialog.asksaveasfile(defaultextension=".json", filetypes=[('json', '.json'),])
    if filename is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        print("cancel save as")
        return
    print(filename)




    model = app.model_reg

    ifc_bars = []
    ifc_ent = None
    for entity_bar in model.get_bars():
        pass
        #ifc_ent = entity_bar.generate_ifc(ifcfile)
        #ifc_bars += [ifc_ent]



    #temp_handle, temp_filename = tempfile.mkstemp(suffix=".ifc")
    data = model.toJSON()
    data = data
    print(filename)
    '''with open(filename, "wb") as f:
        f.write(data)'''

    with filename as f:
        f.write(data)
