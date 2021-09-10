from app import app
from app.view.interface.color_scheme import *
from app.view.simpleui.simple_frame import SimpleFrame

"""COLOR_TEXT_LIGHT = (238, 238, 238)
COLOR_MAIN_DARK = (35 / 255, 35 / 255, 35 / 255, 255 / 255)
COLOR_MAIN_LIGHT = (66 / 255, 66 / 255, 66 / 255, 1)
COLOR_SEC_DARK = (43, 43, 43)
COLOR_SEC_LIGHT = (52, 52, 52)"""


class Layout:
    def __init__(self):
        app.layout = self

        self.options_bar = SimpleFrame(position=[0, 0],
                                       size=[1366, 150],
                                       sizeHint=[1, None],
                                       frameColor=scheme_rgba(COLOR_MAIN_DARK),
                                       padding=[0, 0, 0, 0],
                                       layout="BoxLayout",
                                       layoutDir="Y")

        self.options_bar_titles = SimpleFrame(size=[None, 25],
                                              parent=self.options_bar,
                                              alpha=0,
                                              sizeHint=[1, None],
                                              layout="BoxLayout",
                                              layoutDir="X"
                                              )

        self.options_tab_content = SimpleFrame(size=[None, 100],
                                               parent=self.options_bar,
                                               alpha=0,
                                               sizeHint=[1, None],
                                               layout="BoxLayout",
                                               layoutDir="X")

        app.add_gui_region("options_frame", self.options_bar)

        self.view_tabs_area = SimpleFrame(position=[0, 125],
                                          frameColor=scheme_rgba(COLOR_MAIN_DARK),
                                          #frameColor="C_NEPHRITIS",
                                          size=[1366, 25],
                                          sizeHint=[1, None],
                                          margin=[0, 0, 0, 0],
                                          layout="BoxLayout",
                                          layoutDir="X",
                                          parent=self.options_bar)

        self.work_container = SimpleFrame(position=[0, 0],
                                          sizeHint=[1, 1],
                                          alpha=0,
                                          margin=[0, 0, 25, 150],
                                          layout="BoxLayout",
                                          layoutDir="X")

        self.prop_frame = SimpleFrame(position=[0, 0],
                                      size=[250, 500],
                                      sizeHint=[None, 1],
                                      # frameColor="C_NEPHRITIS",
                                      frameColor=scheme_rgba(COLOR_MAIN_LIGHT),
                                      layout="BoxLayout",
                                      layoutDir="Y",
                                      gridCols=2,
                                      gridRows=2,
                                      parent=self.work_container)

        app.add_gui_region("prop editor", self.prop_frame)
        self.work_area = SimpleFrame(alpha=0, parent=self.work_container)

        self.status_bar_frame = SimpleFrame(position=[0, -25],
                                            size=[50, 25],
                                            sizeHint=[1, None],
                                            orginV="bottom",
                                            layout="BoxLayout",
                                            layoutDir="X",
                                            frameColor=scheme_rgba(COLOR_MAIN_DARK))

        app.add_gui_region("status_bar", self.status_bar_frame)
