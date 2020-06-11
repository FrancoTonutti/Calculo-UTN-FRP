from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout

from modules.user_interface.colors import PaletteColor
from modules.user_interface.widgets import WidButton


class WidOptions(BoxLayout, PaletteColor):
    active_tab = 0
    def __init__(self, **kwargs):
        super(WidOptions, self).__init__(**kwargs)
        tab = WidTabNameBar()
        self.add_widget(tab)
        self.add_widget(WidTabContentBar())


class WidTabNameBar(BoxLayout, PaletteColor):
    color_test = (1, 1, 1)
    tab_ls = list()

    def __init__(self, **kwargs):
        super(WidTabNameBar, self).__init__(**kwargs)

        self.add_tab("Nodos")
        self.add_tab("Barras")
        self.add_tab("Materiales")

        self.set_active_tab(0)

    def add_tab(self, name):
        tab_id = len(self.tab_ls)
        btn = WidTabButton(text=name, call=lambda: self.set_active_tab(tab_id))
        self.add_widget(btn)
        self.tab_ls.append(btn)

    def set_active_tab(self, tab_id):
        if self.parent is not None:
            self.parent.active_tab = tab_id
        btn = self.tab_ls[tab_id]

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
    def __init__(self, **kwargs):
        super(WidTabContentBar, self).__init__(**kwargs)



class WidTabButton(WidButton):

    def __init__(self, text="", **kwargs):
        super(WidTabButton, self).__init__(**kwargs)
        #self.width = 100
        self.color_normal = self.get_rgba("color_title_bar")
        self.size_hint = (1, 1)
        self.text = text
        self.fit_to_text_width()