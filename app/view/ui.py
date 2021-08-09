from app import app
from app.view.option_bar import OptionBar
from app.view import interface
from app.view import draw

from app.view.panda_ui_toolset.stack_panel import StackPanel



class MainUI:
    def __init__(self):
        draw.draw_set_font()
        app.main_ui = self

        base = app.get_show_base()
        base.setBackgroundColor(1, 1, 1)

        self.layout = interface.Layout()
        interface.ConsoleUI(self.layout)

        self.option_bar = OptionBar()
        self.prop_editor = interface.PropertiesEditor(self.layout)
        self.status_bar = interface.StatusBar(self.layout)
        interface.ConsoleUI(self.layout)
        self.tab_manager = interface.TabManager(self.layout)

        """main = StackPanel(orientation="Vertical", width="5 cm", height="5 cm", background="Blue")

        main.set_render_pos(400, 150)


        sec = StackPanel(height="1 cm", parent=main, background="Green")
        sec = StackPanel(height="1 cm", parent=main, background="White", max_width=50, margin=20)
        sec = StackPanel(height="1 cm", parent=main, background="Green")
        sec = StackPanel(height="1 cm", parent=main, background="Purple", orientation="Horizontal")

        StackPanel(width="1 cm", parent=sec, background="Red")
        StackPanel(width="1 cm", parent=sec, background="White")
        StackPanel(width="1 cm", parent=sec, background="Red")"""








