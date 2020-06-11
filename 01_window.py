from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, LineSegs, NodePath, WindowProperties

from modules.user_interface import custom_camera
from modules.user_interface.main_ui import MainApp
from modules import panda_tasks

# Carga las configuraciones para la pantalla de panda3d
loadPrcFile("config/config.prc")


class MyProgram(ShowBase):
    def __init__(self):
        super().__init__()

        # Inicia la interfaz de usuario en Kivy
        self.kivy_app = kivy_app = MainApp(self)
        kivy_app.run()

        # Cambia el color de fondo del modelo 3d
        self.setBackgroundColor(1, 1, 1)

        # Activa el movimiento de la camara personalizado, agrega la indicaión de los ejes en la esquina inferior
        # y cambia a una lente de vista ortogonal en lugar de la vista en persepctiva por defecto
        custom_camera.enable(self)
        custom_camera.show_view_cube(self)
        custom_camera.set_lens(self, "OrthographicLens")

        # Define el plano de trabajo y la ubicación del mouse en el modelo
        self.work_plane_vect = (0, 1, 0)
        self.work_plane_point = (0, 0, 0)
        self.work_plane_mouse = (0, 0, 0)

        # Crea un objecto cursor que se ubica según la posición de la camara
        self.cursor = self.loader.loadModel("models/box")
        scale = 0.1
        self.cursor.setScale(scale, scale, scale)
        self.cursor.setPos(0, 10, 0)
        self.cursor.reparentTo(self.camera)

        # Agrega una función al administrador de tarea que se ejecuta en cada momento
        # para determinar la posición del mouse en el plano de coordenadas
        self.task_mgr.add(lambda task: panda_tasks.get_mouse_3d_coords_task(task, self), "get_mouse_3d_coords_task")

        # Agrega un indicador de ejes en el centro del modelo
        box = self.loader.loadModel("models/custom-axis2")
        box.setPos(0, 0, 0)
        box.setScale(0.1, 0.1, 0.1)
        box.reparentTo(self.render)


# Inicia el programa
if __name__ == "__main__":
    program = MyProgram()
    program.run()
