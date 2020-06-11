from panda3d_kivy.app import App

from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from modules.user_interface.widgets import WidButton

from modules.user_interface import widgets, title_bar, option_bar

from modules.user_interface.option_bar import WidOptions
from modules import panda_tasks

class WidMain(BoxLayout):
    def __init__(self, panda_app):
        super(WidMain, self).__init__()
        self.title_bar = title_bar.WidTitleBar()

        #self.add_widget(self.title_bar)
        self.add_widget(option_bar.WidOptions())
        self.add_widget(widgets.WidWorkspace())

        self.button_data = list()

        self.get_all_buttons()

        self.panda3D = panda_app

        self.panda3D.task_mgr.add(self.button_overmouse_task, "button_overmouse_task")

    def get_all_buttons(self):
        self.button_data.clear()
        self.iterate_buttons(self)

    def iterate_buttons(self, parent):
        for child in parent.children:
            #print(child)
            #if "WidButton" in str(type(child)):
            if isinstance(child, WidButton):
                self.button_data.append(child)
                #print("funciona")
            else:
                #print("dont match----------")
                #print(isinstance(child, WidButton))
                #print(type(child))
                self.iterate_buttons(child)

    def button_overmouse_task(self, task):
        if self.panda3D.mouseWatcherNode.has_mouse():
            width = self.panda3D.win.getXSize()
            height = self.panda3D.win.getYSize()

            mouse_data = self.panda3D.win.getPointer(0)
            mouse_pos = mouse_data.getX(), height - mouse_data.getY()
        else:
            mouse_pos = None

        for btn in self.button_data:
            if mouse_pos is not None:
                overmouse_x = (btn.pos[0] <= mouse_pos[0] <= btn.pos[0] + btn.size[0])
                overmouse_y = (btn.pos[1] <= mouse_pos[1] <= btn.pos[1] + btn.size[1])

                if overmouse_x and overmouse_y:
                    btn.background_color = btn.color_pressed
                    btn.overmouse = True
                else:
                    btn.background_color = btn.color_normal
                    btn.overmouse = False

                # print("{}:{}:{}".format(btn.pos, btn.size, mouse_pos))
            else:
                btn.background_color = btn.color_normal
        return task.cont


class MainApp(App):
    def __init__(self, panda_app, **kwargs):
        super().__init__(panda_app, **kwargs)
        self.panda3D = self.panda_app

    def build(self):
        return WidMain(self.panda3D)


if __name__ == '__main__':
    Config.set('graphics', 'width', 1920)
    Config.set('graphics', 'height', 1000)
    MainApp().run()
