from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from app.user_interface.colors import PaletteColor
from app.controller import console


# Se ubica por deabjo de la cinta de opciones y contendrá al espacio de trabajo y al panel lateral
class WidContentArea(BoxLayout):
    def __init__(self, panda_app):
        super(WidContentArea, self).__init__()

        left_panel = WidLeftPanel()
        self.add_widget(left_panel)

        workspace = WidWorkspace(panda_app=panda_app)
        panda_app.kyvi_workspace = workspace
        self.add_widget(workspace)


# Panel lateral izquierdo
class WidLeftPanel(BoxLayout, PaletteColor):
    pass


# Widget del espacio de trabajo donde se muestra el modelo
class WidWorkspace(BoxLayout):
    # offset [left, top, right, bottom]
    offset = [0, 0, 0, 0]
    box_input = None
    active = True

    def __init__(self, panda_app):
        super(WidWorkspace, self).__init__()
        self.panda3d = panda_app
        panda_app.task_mgr.add(self.keystroke_task, "keystroke_task")
        self.show_text_input()

    def show_text_input(self):
        self.box_input = BoxInput(font_size=12,
                                  size_hint_y=None,
                                  height=30,
                                  multiline=False)
        self.add_widget(self.box_input)
        self.offset[3] = 30

    def hide_text_input(self):
        pass

    def keystroke_task(self, task):
        if self.active and not self.box_input.focused:
            keys = "abcdefghijklmñopqrstuvwxyz.0123456789"
            watcher = self.panda3d.mouseWatcherNode
            for key in keys:
                if watcher.isButtonDown(key):

                    self.box_input.focused = True
                    self.box_input.text = key
                    print(key)
        elif self.active:
            watcher = self.panda3d.mouseWatcherNode
            if watcher.isButtonDown("arrow_right"):
                print(self.panda3d.commands.get(self.box_input.text, None))

        return task.cont

    def console_enter(self):
        console.execute(self.box_input.text)


class BoxInput(TextInput):
    def __init__(self, **kwargs):
        super(BoxInput, self).__init__(**kwargs)

    def on_text_validate(self):
        self.parent.console_enter()
