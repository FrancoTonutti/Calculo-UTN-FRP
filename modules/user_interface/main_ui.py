from panda3d_kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from modules.user_interface.widgets import WidButton

from modules.user_interface import widgets, option_bar


# El widget princpal abarca todos los elementos de la interzas
class WidMain(BoxLayout):
    def __init__(self, panda_app):
        super(WidMain, self).__init__()

        # Almacena en la clase una referencia al modelo en panda3d
        self.panda3D = panda_app

        # Agrega la cinta de opciones a la interfaz
        cinta = option_bar.WidOptions()
        self.add_widget(cinta)
        self.add_widget(widgets.WidWorkspace())

        # Agrega una lista con todos los botones de la interfaz
        self.button_data = list()
        self.get_all_buttons()

        # Incia una tarea que comprueba cuando el cursor se encuentra arriba de un botón
        self.panda3D.task_mgr.add(self.button_overmouse_task, "button_overmouse_task")

    def get_all_buttons(self):
        self.button_data.clear()
        self.iterate_buttons(self)

    def iterate_buttons(self, parent):
        # Busca todos las botones(de la clase "WidButton") de la interfaz
        # revisando en los elementos hijos de cada widget
        for child in parent.children:
            if isinstance(child, WidButton):
                self.button_data.append(child)
            else:
                self.iterate_buttons(child)

    def button_overmouse_task(self, task):
        # Evalua si el cursor se encuentra dentro de la ventana
        if self.panda3D.mouseWatcherNode.has_mouse():
            # Obtenemos la posición del cursor, la cordenada "y" se invierte
            height = self.panda3D.win.getYSize()

            mouse_data = self.panda3D.win.getPointer(0)
            mouse_pos = mouse_data.getX(), height - mouse_data.getY()
        else:
            mouse_pos = None

        # Recorremos la lista de botones
        for btn in self.button_data:
            if mouse_pos is not None:
                # Analiza la posición del cursor respecto a la de cada boton y su tamaño
                overmouse_x = (btn.pos[0] <= mouse_pos[0] <= btn.pos[0] + btn.size[0])
                overmouse_y = (btn.pos[1] <= mouse_pos[1] <= btn.pos[1] + btn.size[1])

                if overmouse_x and overmouse_y:
                    btn.background_color = btn.color_pressed
                    btn.overmouse = True
                else:
                    btn.background_color = btn.color_normal
                    btn.overmouse = False
            else:
                btn.background_color = btn.color_normal

        return task.cont


class MainApp(App):
    def __init__(self, panda_app, **kwargs):
        super().__init__(panda_app, **kwargs)
        self.panda3D = self.panda_app

    def build(self):
        return WidMain(self.panda3D)
