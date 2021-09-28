from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, AntialiasAttrib

from app import app
from app.view.ui import MainUI
from app.view import camera, shaders
from tkinter import messagebox

import traceback
import sys

from app.controller import commands
from app.controller.console import command, execute

# Carga las configuraciones para la pantalla de panda3d
loadPrcFile("data/config/config.prc")


class MyProgram(ShowBase):
    def __init__(self):
        super().__init__()

        app.set_show_base(self)

        MainUI()
        execute("new_file")

        self.shader_control = None
        self.camera_control = camera.CameraControl(self)
        # self.render.setRenderMode(5,5,1)
        self.shader_control = shaders.ShaderControlGLSL(self)

        #self.render.setAntialias(AntialiasAttrib.MAuto)
        #shaders.add_shadders(self)


        #self.separation = 1  # Pixels
        #self.filters = CommonFilters(self.win, self.cam)
        #filterok = self.filters.setCartoonInk(separation=self.separation)

# Inicia el programa
if __name__ == "__main__":
    program = MyProgram()
    try:
        program.run()
    except Exception as ex:
        messagebox.showerror(message='error: "{}" \nUbicación del error:\n{}'.format(ex, traceback.extract_tb(ex.__traceback__)))

