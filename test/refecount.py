import ctypes
import sys

from app.model import Entity, View

import ctypes
from panda3d.core import GeomNode, CollisionSegment, CollisionNode
from app import app
import uuid

from typing import TYPE_CHECKING
from typing import List

from app.model.entity import Test2
from app.model.transaction import Transaction

if TYPE_CHECKING:
    # Imports only for IDE type hints
    pass
from ifcopenshell import guid
from ifcopenshell.file import file

LANG = {
    "start": "Inicio",
    "end": "Fin",
    "section": "Sección",
    "material": "Material",
    "width": "Ancho",
    "height": "Alto",
    "name": "Nombre"
}

class Test:
    def __init__(self):
        print("!!! ", sys.getrefcount(self))
        print("!!! References to {}:".format(self),
              ctypes.c_long.from_address(id(self)).value)
        print("!!! References to {}:".format(self),
              ctypes.c_long.from_address(id(self)).value)
        print("!!! References to {}:".format(self),
              ctypes.c_long.from_address(id(self)).value)
        print("!!! References to {}:".format(self),
              ctypes.c_long.from_address(id(self)).value)


tr = Transaction()
tr.start("sadasd")
a = Entity()
tr.commit()


print(sys.getrefcount(a))
print(sys.getrefcount(a))
print("!!! References to {}:".format(a),ctypes.c_long.from_address(id(a)).value)
print(a.__references__)