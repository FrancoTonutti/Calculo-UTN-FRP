from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, LineSegs, NodePath, WindowProperties

from modules.user_interface import custom_camera
from modules.user_interface.main_ui import MainApp
from modules import panda_tasks

loadPrcFile("config/config.prc")

'''
from kivy.uix.boxlayout import BoxLayout
class Contenedor01(BoxLayout):
    pass


class MainApp(App):
    title = 'Hola Mundo'

    def build(self):
        return Contenedor01()
'''


class MyProgram(ShowBase):
    def __init__(self):
        super().__init__()

        # Interfaz de usuario en Kivy

        self.kivy_app = kivy_app = MainApp(self)
        kivy_app.run()

        # desabilita el control de la camara por defecto
        # self.disable_mouse()

        self.setBackgroundColor(1, 1, 1)

        custom_camera.enable(self)
        custom_camera.show_view_cube(self)
        custom_camera.set_lens(self, "OrthographicLens")
        #############

        self.work_plane_vect = (0, 1, 0)
        self.work_plane_point = (0, 0, 0)
        self.work_plane_mouse = (0, 0, 0)

        self.cursor = self.loader.loadModel("models/box")
        scale = 0.1
        self.cursor.setScale(scale, scale, scale)
        self.cursor.setPos(0, 10, 0)
        self.cursor.reparentTo(self.camera)

        self.task_mgr.add(lambda task: panda_tasks.get_mouse_3d_coords_task(task, self), "get_mouse_3d_coords_task")


        box = self.loader.loadModel("models/custom-axis2")
        box.setPos(0, 0, 0)
        box.setScale(0.1, 0.1, 0.1)
        box.reparentTo(self.render)

        """
        lines = LineSegs()
        lines.moveTo(0, 0, 0)
        lines.drawTo(2, 2, 2)
        lines.setThickness(4)
        node = lines.create()
        np = NodePath(node)
        np.reparentTo(self.render)

        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        """



program = MyProgram()
program.run()
