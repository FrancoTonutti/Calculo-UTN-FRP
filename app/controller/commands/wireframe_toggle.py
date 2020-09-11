from app.controller.console import command, execute
from app.controller.commands import render
from app import app
import numpy as np
from panda3d.core import LineSegs, NodePath
from app.view import draw


@command("wire")
def wireframe_toggel():
    if render.wireframe is True:
        render.wireframe = False
    else:
        render.wireframe = True

    print("Wireframe", render.wireframe)

    execute("regen")
