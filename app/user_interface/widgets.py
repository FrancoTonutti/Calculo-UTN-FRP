from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from app.user_interface.colors import PaletteColor
from kivy.properties import StringProperty





# Barra de estado inferior
class WidStateBarTop(BoxLayout, PaletteColor):
    pass


# Barra de estado inferior
class WidStateBarBot(BoxLayout, PaletteColor):
    pass


# Widget de botón base para el proyecto
class WidButton(Button, PaletteColor):
    image_path = StringProperty('')
    overmouse = False
    active_btn = False
    wid_main = None

    def __init__(self, img_dir="data/img/blank.png", call=None, **kwargs):
        super(WidButton, self).__init__(**kwargs)

        # Se definen los colores que tendrá el botón en los diferentes estados
        self.color_normal = (0, 0, 0, 0)
        self.color_pressed = self.get_rgba("color_title_bar_light")

        self.background_color = self.color_normal

        # Se establece la textura para los botones, por defecto una imagen transparente
        self.image_path = img_dir
        self.background_normal = img_dir
        self.background_down = img_dir
        self.call_on_press = call

    def on_press(self):
        # Busca al widget principal WidMain
        if self.wid_main is None:
            self.wid_main = self.parent
            while "WidMain" not in str(type(self.wid_main)):
                self.wid_main = self.wid_main.parent

        # Obtiene el administrador de tareas de panda3d
        task_mgr = self.wid_main.panda3D.task_mgr

        # Agrega una tarea que analiza el botón activo
        if not task_mgr.hasTaskNamed("active_btn"):
            self.active_btn = True
            task_mgr.add(self.active_btn_task, "active_btn")

    def on_release(self):
        # Llama a la función especificada en el parametro call cuando se presiona el botón
        if self.call_on_press is not None and self.active_btn:
            self.active_btn = False
            self.call_on_press()

    def active_btn_task(self, task):
        # Esta tarea se encarga de revisar si el botón del mouse se levanta dentro del mismo botón que se presionó

        # Obtenemos el nodo del mouse desde panda3d
        mouse_node = self.wid_main.panda3D.mouseWatcherNode

        if not mouse_node.isButtonDown('mouse1'):
            # Estable el boton como inactivo y remueve la tarea "active_btn"
            if not self.overmouse:
                self.active_btn = False
            self.wid_main.panda3D.task_mgr.remove("active_btn")

        return task.cont

    def fit_to_text_width(self):
        # Establece las propiedades para que el botón se ajuste al texto
        hint = self.size_hint
        self.size_hint = (None, hint[1])


