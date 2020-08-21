from app import app
from app.view.option_bar import OptionBar
from app.view.simpleui.simple_frame import SimpleFrame
from app.view import interface


class MainUI:
    def __init__(self):
        app.main_ui = self

        base = app.get_show_base()
        base.setBackgroundColor(1, 1, 1)

        self.layout = interface.Layout()

        self.option_bar = OptionBar()
        self.prop_nav = interface.PropertiesEditor(self.layout)
        interface.ConsoleUI(self.layout)

        if False:
            frame = SimpleFrame(position=[0, 0], sizeHint=[1, 1], alpha=0, padding=[0, 0, 25, 150], layout="BoxLayout.X")
            frame2 = SimpleFrame(position=[0, 0], size=[250, 500], sizeHint=[None, 1], frameColor="C_RED", parent=frame)
            frame6 = SimpleFrame(alpha=100, parent=frame)


        if False:
            frame3 = SimpleFrame(size=[500, 200], frameColor="C_BLACK", layout="BoxLayout.X", sizeHint=[0.5, 1])

            frame4 = SimpleFrame(frameColor="C_CARROT", size=[100, 20], sizeHint=[0.25, 0.25], parent=frame3)
            frame6 = SimpleFrame(frameColor="C_GREEN", parent=frame3)
            frame5 = SimpleFrame(frameColor="C_BLUE", size=[100, 20], sizeHint=[0.25, 0.25], parent=frame3, padding=[25, 25, 25, 25])
            frame6 = SimpleFrame(frameColor="C_GREEN", parent=frame3)
            frame5 = SimpleFrame(frameColor="C_RED", size=[100, 20], sizeHint=[0.25, 0.25], parent=frame3)

            #frame6 = SimpleFrame()
        
