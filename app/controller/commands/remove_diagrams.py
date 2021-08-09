from app.controller.console import command
from app import app
import numpy as np
from panda3d.core import LineSegs, NodePath
from app.view import draw

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # Imports only for IDE type hints
    from app.view.interface.console_ui import ConsoleUI
    from app.model import *


@command("remove_diagrams")
def remove_diagrams():
    print("remove_diagrams")
    # Accede a la interfaz de kivy para obtener la información de panda3d
    panda3d = app.get_show_base()
    # Obtenemos el registro del modelo
    model_register = app.model_reg

    node_list = list(model_register.find_entities("Diagram"))

    for node_entity in node_list:  # type: Node
        print("remove", node_entity)
        node_entity.delete()