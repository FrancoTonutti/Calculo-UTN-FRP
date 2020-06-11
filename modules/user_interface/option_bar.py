from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout

from modules.user_interface.colors import PaletteColor
from modules.user_interface.widgets import WidButton


class WidOptions(BoxLayout, PaletteColor):
    active_tab = 0

    def __init__(self, **kwargs):
        super(WidOptions, self).__init__(**kwargs)

        # Agrega la barra de pestañas y el contenedor de secciones
        tab = WidTabNameBar()
        self.add_widget(tab)
        content = WidTabContentBar()
        self.add_widget(content)


class WidTabNameBar(BoxLayout, PaletteColor):
    color_test = (1, 1, 1)
    tab_ls = list()

    def __init__(self, **kwargs):
        super(WidTabNameBar, self).__init__(**kwargs)

        # Agrega el botón de cada pestaña
        self.add_tab("Nodos")
        self.add_tab("Barras")
        self.add_tab("Materiales")

        self.set_active_tab(0)

    def add_tab(self, name):
        # Crea un botón y le asigna la función set_active_tab como acción cuando es presionado
        tab_id = len(self.tab_ls)
        btn = WidTabButton(text=name, call=lambda: self.set_active_tab(tab_id))
        self.add_widget(btn)
        self.tab_ls.append(btn)

    def set_active_tab(self, tab_id):
        # Establece la pestaña activa en el widget padre "WidOptions"
        if self.parent is not None:
            self.parent.active_tab = tab_id

        # Recorre todos los botones y asigna colores según si corresponde a la nueva pestaña activa
        i = 0
        for btn in self.tab_ls:
            if i is tab_id:
                btn.color_normal = self.get_rgba("color_options_bar")
                btn.color_pressed = self.get_rgba("color_options_bar")
                btn.color = (0, 0, 0, 1)
            else:
                btn.color_normal = self.get_rgba("color_title_bar")
                btn.color_pressed = self.get_rgba("color_title_bar_light")
                btn.color = (1, 1, 1, 1)
            i += 1


class WidTabContentBar(BoxLayout, PaletteColor):
    # Almacenará los botones de cada pestaña en distintas secciones

    def __init__(self, **kwargs):
        super(WidTabContentBar, self).__init__(**kwargs)


class WidTabButton(WidButton):
    # Definimos un botón que hereda propiedades de "WidButton" y lo adaptamos en tamaño

    def __init__(self, text="", **kwargs):
        super(WidTabButton, self).__init__(**kwargs)
        self.color_normal = self.get_rgba("color_title_bar")
        self.text = text
        self.fit_to_text_width()
