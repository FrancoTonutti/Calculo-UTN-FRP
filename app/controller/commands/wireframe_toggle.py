from app.controller.console import command, execute
from app.controller.commands import render
from app import app
import numpy as np
from panda3d.core import LineSegs, NodePath
from app.view import draw


@command("wire")
def wireframe_toggel():
    if app.wireframe is True:
        app.wireframe = False
    else:
        app.wireframe = True

    render.wireframe = app.wireframe

    print("Wireframe", render.wireframe)

    execute("regen")
