from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile

from app import app
from app.view.ui import MainUI
from app.view import camera, shaders

from app.controller import commands

# Carga las configuraciones para la pantalla de panda3d
loadPrcFile("data/config/config.prc")


class MyProgram(ShowBase):
    def __init__(self):
        super().__init__()
        app.set_show_base(self)

        MainUI()

        camera.CameraControl(self)

        shaders.add_shadders(self)

        #self.separation = 1  # Pixels
        #self.filters = CommonFilters(self.win, self.cam)
        #filterok = self.filters.setCartoonInk(separation=self.separation)

# Inicia el programa
if __name__ == "__main__":
    program = MyProgram()
    program.run()
