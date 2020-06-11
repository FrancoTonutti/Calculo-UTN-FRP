from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from modules.user_interface.colors import PaletteColor

from kivy.properties import StringProperty
import time




class WidWorkspace(BoxLayout):
    pass


class WidButton(Button, PaletteColor):
    image_path = StringProperty('')
    overmouse = False

    def __init__(self, img_dir="img/blank.png", call=None, **kwargs):
        super(WidButton, self).__init__(**kwargs)
        self.color_normal = (0, 0, 0, 0)
        self.color_pressed = self.get_rgba("color_title_bar_light")

        self.background_color = self.color_normal
        self.image_path = img_dir
        self.background_normal = img_dir
        self.background_down = img_dir
        self.call_on_press = call


        if img_dir is not "" and img_dir is not "img/blank.png":
            pass

        self.wid_main = None
        self.active_btn = False



    def on_press(self):
        # Busca al widget principal WidMain
        wid_main = self.parent
        while "WidMain" not in str(type(wid_main)):
            wid_main = wid_main.parent

        self.wid_main = wid_main
        # Obtiene el administrador de tareas de panda3d
        task_mgr = self.wid_main.panda3D.task_mgr

        # Agrega una tarea de botón activo
        if not task_mgr.hasTaskNamed("active_btn"):
            self.active_btn = True
            task_mgr.add(self.active_btn_task, "active_btn")

    def on_release(self):
        if self.call_on_press is not None and self.active_btn:
            self.active_btn = False
            self.call_on_press()

    def active_btn_task(self, task):
        mouse_node = self.wid_main.panda3D.mouseWatcherNode
        if not mouse_node.isButtonDown('mouse1'):
            # Estable el boton como inactivo y remueve la tarea "active_btn"
            if not self.overmouse:
                self.active_btn = False
            self.wid_main.panda3D.task_mgr.remove("active_btn")

        return task.cont

    def fit_to_text_width(self):
        print("fit_to_text_width")
        hint = self.size_hint
        self.size_hint = (None, hint[1])
        print(self.text)
        print(self.texture_size)
        #self.width = self.text_size[0]


