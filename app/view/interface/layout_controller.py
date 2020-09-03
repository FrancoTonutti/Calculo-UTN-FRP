from app.view.simpleui.simple_frame import SimpleFrame
from app import app
from app.view import draw

class Layout:
    def __init__(self):
        app.layout = self
        self.work_container = SimpleFrame(position=[0, 0],
                                          sizeHint=[1, 1],
                                          alpha=0,
                                          padding=[0, 0, 25, 150],
                                          layout="BoxLayout",
                                          layoutDir="X")

        self.prop_frame = SimpleFrame(position=[0, 0],
                                      size=[250, 500],
                                      sizeHint=[None, 1],
                                      frameColor="C_NEPHRITIS",
                                      layout="BoxLayout",
                                      layoutDir="Y",
                                      gridCols=2,
                                      gridRows=2,
                                      parent=self.work_container)

        self.work_area = SimpleFrame(alpha=0, parent=self.work_container)

        app.add_gui_region("prop editor", self.prop_frame)
