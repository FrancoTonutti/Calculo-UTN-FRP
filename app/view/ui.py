from app import app
from app.view.option_bar import OptionBar
from app.view import interface
from app.view import draw

class MainUI:
    def __init__(self):
        draw.draw_set_font()
        app.main_ui = self

        base = app.get_show_base()
        base.setBackgroundColor(1, 1, 1)

        self.layout = interface.Layout()

        self.option_bar = OptionBar()
        self.prop_editor = interface.PropertiesEditor(self.layout)
        interface.ConsoleUI(self.layout)
