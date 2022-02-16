from app import app
from app.view import draw
from app.view.simpleui import SimpleButton, SimpleLabel, SimpleFrame
from ifcopenshell import guid
from .layout_controller import Layout
from app.view import simpleui
from app.view.interface.color_scheme import *
from ...model import View
from app.model.transaction import Transaction


def new_button(text, x, y, colors=None, command=None, args=None, parent=None, size=None):
    if args is None:
        args = []
    font_panda3d, font_pil = draw.draw_get_font()
    if colors is None:
        col_rollover = draw.merge_color(COLOR_MAIN_DARK, COLOR_MAIN_LIGHT, 0.2)
        colors = [COLOR_MAIN_DARK, COLOR_MAIN_LIGHT, col_rollover, "C_CONCRETE"]
    if size is None:
        width = font_pil.getsize(text)[0]
        size = [width, 19]

    btn = SimpleButton(text=text,
                       text_scale=(12, 12),
                       text_font=font_panda3d,
                       text_fg=draw.get_color(COLOR_TEXT_LIGHT, "rgba"),
                       command=command,
                       parent=parent,
                       extraArgs=args,
                       colorList=colors,
                       position=[x, y],
                       padding=[10,10,0,0],
                       size=size
                       )

    return btn

class Tab:
    def __init__(self, title, frame=None):
        self.title = title
        self.frame = frame
        self.button_frame = None
        self.id = guid.new()
        self.disable_close = False
        self.ev_focus_in = None

    def hide(self):
        if self.frame:
            self.frame.hide()

    def show(self):
        if self.frame:
            self.frame.show()

    def focus_in(self):
        if self.ev_focus_in:
            self.ev_focus_in()


class TabManager:
    def __init__(self, layout: Layout):
        self.layout_area = layout.view_tabs_area
        self.tabs = list()
        tab = Tab("Vista 3D", frame=layout.work_container)

        tr = Transaction()
        tr.start("Create View")
        View()
        tr.commit()

        tab.disable_close = True

        self.tabs.append(tab)
        self.update_tab_view_buttons()
        self.main_3d_tab = tab
        self.active_tab = tab

    def get_active_tab_index(self):
        i = 0
        for tab in self.tabs:
            if tab is self.active_tab:
                return i
            i += 1

    def close_tab(self, index):
        if not self.tabs[index].disable_close:
            tab = self.tabs.pop(index)
            tab.button_frame.removeNode()
            tab.frame.removeNode()

            if self.active_tab and self.get_active_tab_index() == index:
                #self.active_tab = 1
                self.set_active_tab(0)

            self.update_tab_view_buttons()


    def create_new_tab(self, title, fill=True):
        frame = SimpleFrame(position=[0, 0],
                    sizeHint=[1, 1],
                    alpha=1,
                    margin=[0, 0, 25, 150],
                    layout="BoxLayout",
                    layoutDir="Y")

        tab = Tab(title, frame)
        index = len(self.tabs)
        self.tabs.append(tab)

        if fill:
            app.add_gui_region("tab_{}".format(tab.id), frame)

        self.update_tab_view_buttons()

        self.set_active_tab(index)

        return tab



    def set_active_tab(self, index):
        '''btn = self.tab_btn[self.active_tab]
        col_rollover = draw.merge_color(COLOR_MAIN_DARK, COLOR_MAIN_LIGHT, 0.2)
        btn["colorList"] = [COLOR_MAIN_DARK, COLOR_MAIN_LIGHT, col_rollover,
                            "C_CONCRETE"]'''
        print("self.tabs", self.tabs)

        #frame = self.tabs[self.active_tab]
        self.active_tab.hide()

        self.active_tab = self.tabs[index]
        self.active_tab.show()
        self.active_tab.focus_in()

        '''btn = self.tab_btn[self.active_tab]
        btn["colorList"] = [COLOR_MAIN_LIGHT, COLOR_MAIN_LIGHT]'''

        '''frame = self.tabs[self.active_tab]
        frame.show()'''


    def update_tab_view_buttons(self):
        index = 0
        for tab in self.tabs:

            if tab.button_frame:
                tab.button_frame.removeNode()

            container = SimpleFrame(position=[0, 0],
                                       size=[150, 19],
                                       sizeHint=[None, None],
                                       alpha=0,
                                       margin=[10, 0, 0, 3],
                                       layout="BoxLayout",
                                       layoutDir="X",
                                    parent=self.layout_area)

            tab.button_frame = container


            col_rollover = draw.merge_color(COLOR_SEC_LIGHT, COLOR_MAIN_LIGHT,
                                            0.5)
            colors = [COLOR_SEC_LIGHT, COLOR_MAIN_LIGHT, col_rollover,
                      "C_CONCRETE"]

            button1 = new_button(tab.title, 0, 0, parent=container, colors=colors, command=self.set_active_tab, args=[index])
            button2 = new_button("x", 0, 0, parent=container, colors=colors, command=self.close_tab, args=[index])

            size_1 = button1.box_size()
            size_2 = button2.box_size()

            size = [size_1[0]+size_2[0], 19]
            container["size"] = size

            index += 1

        simpleui.update_ui()


