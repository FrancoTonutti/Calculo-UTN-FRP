from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile

from app.user_interface import camera
from app.user_interface.main_ui import MainApp
from app import panda_tasks

from app.controller.console import command_list

from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')

# Carga las configuraciones para la pantalla de panda3d
loadPrcFile("data/config/config.prc")



class MyProgram(ShowBase):
    def __init__(self):
        super().__init__()
        print("panda3d start")
        # Inicia la interfaz de usuario en Kivy
        self.kyvi_main_widet = None
        self.kyvi_workspace = None
        self.kivy_app = kivy_app = MainApp(self)
        kivy_app.run()

        # Cambia el color de fondo del modelo 3d
        self.setBackgroundColor(1, 1, 1)

        # Activa el movimiento de la camara personalizado, agrega la indicaión de los ejes en la esquina inferior
        # y cambia a una lente de vista ortogonal en lugar de la vista en persepctiva por defecto

        cam_control = camera.CameraControl(self)

        # Define el plano de trabajo y la ubicación del mouse en el modelo
        self.work_plane_vect = (0, 1, 0)
        self.work_plane_point = (0, 0, 0)
        self.work_plane_mouse = (0, 0, 0)

        # Creamos una variable que almacenará el registro de todos los elementos del modelo
        self.model_reg = dict()
        self.commands = command_list

        # Crea un objecto cursor que se ubica según la posición de la camara

        self.cursor = self.render.attach_new_node("cursor_pos")
        scale = 0.1
        self.cursor.setScale(scale, scale, scale)
        self.cursor.setPos(0, 10, 0)
        self.cursor.reparentTo(self.camera)

        # Agrega una función al administrador de tarea que se ejecuta en cada momento
        # para determinar la posición del mouse en el plano de coordenadas

        self.task_mgr.add(lambda task: panda_tasks.get_mouse_3d_coords_task(task, self), "get_mouse_3d_coords_task")

        # Agrega un indicador de ejes en el centro del modelo
        box = self.loader.loadModel("data/geom/custom-axis")
        box.setPos(0, 0, 0)
        box.setScale(0.1, 0.1, 0.1)
        box.reparentTo(self.render)

        # self.accept("escape", self.userExit)


# Inicia el programa
if __name__ == "__main__":
    program = MyProgram()

    program.run()
