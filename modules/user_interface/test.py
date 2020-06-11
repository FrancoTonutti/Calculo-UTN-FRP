from panda3d_kivy.app import App

#from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window

from kivy.uix.button import Button


class MousePosDemo(Button):

    def __init__(self, **kwargs):
        super(MousePosDemo, self).__init__(**kwargs)
        self.label = Label()
        self.add_widget(self.label)
        Window.bind(mouse_pos=self.mouse_pos)

    def mouse_pos(self, window, pos):
        self.label.text = str(pos)


class TestApp(App):
    title = "Kivy Mouse Pos Demo"

    def build(self):
        return MousePosDemo()


if __name__ == "__main__":
    #TestApp().run()
    pass

from direct.showbase.ShowBase import ShowBase

class PandaApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.kivy_app = kivy_app = TestApp(self)
        kivy_app.run()


program = PandaApp()
program.run()