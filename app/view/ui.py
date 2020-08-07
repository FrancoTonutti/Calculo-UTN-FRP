from app import app
from app.view.option_bar import OptionBar
from app.view.simpleui.simple_frame import SimpleFrame


class MainUI:
    def __init__(self):
        app.main_ui = self

        base = app.get_show_base()
        base.setBackgroundColor(1, 1, 1)

        self.option_bar = OptionBar()
