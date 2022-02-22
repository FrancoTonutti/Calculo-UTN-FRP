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

from app.model.transaction import Transaction

if TYPE_CHECKING:
    # Imports only for IDE type hints
    pass

from app.controller.console import command, execute

import time
import tempfile
import ifcopenshell

O = 0., 0., 0.
X = 1., 0., 0.
Y = 0., 1., 0.
Z = 0., 0., 1.


@command(name="open_file", shortcut="s")
def save():
    print("----------------------------------------------------")
    print("save()")
    root = tk.Tk()
    root.withdraw()

    filename = "myfile.json"

    filename = filedialog.askopenfile(mode="r", defaultextension=".json", filetypes=[('json', '.json'),])
    if filename is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        print("cancel save as")
        return
    print(filename)

    '''temp_handle, temp_filename = tempfile.mkstemp(suffix=".ifc")
    data = "".encode()
    print(temp_filename)
    with open(temp_filename, "wb") as f:
        f.write(data)'''


    model = app.model_reg

    model.clear()
    execute("regen")

    with filename as f:
        content = f.read()

    tr = Transaction()
    tr.start("Open file")
    model.from_JSON(content)
    tr.commit()


