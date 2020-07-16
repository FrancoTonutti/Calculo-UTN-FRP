from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from app.user_interface.colors import PaletteColor
from app.controller import console
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import inspect

# Se ubica por deabjo de la cinta de opciones y contendrá al espacio de trabajo y al panel lateral
class WidContentArea(BoxLayout):
    def __init__(self, panda_app):
        super(WidContentArea, self).__init__()

        left_panel = WidLeftPanel(panda_app)
        self.add_widget(left_panel)

        workspace = WidWorkspace(panda_app=panda_app)
        panda_app.kyvi_workspace = workspace
        self.add_widget(workspace)


# Panel lateral izquierdo
class WidLeftPanel(BoxLayout, PaletteColor):

    def __init__(self, panda_app):
        super(WidLeftPanel, self).__init__()
        self.orientation = 'vertical'
        self.add_widget(WidProperties(panda_app))
        self.add_widget(BoxLayout())


class WidProperties(GridLayout, PaletteColor):
    def __init__(self, panda_app):
        super(WidProperties, self).__init__()
        self.panda3d = panda_app
        panda_app.kyvy_wid_properties = self
        self.cols = 2
        self.row_default_height = 30
        self.size_hint_y = None
        self.entity_data = dict()
        self.entity = None
        lb = Label(text="Propiedades")
        self.add_widget(lb)
        lb = Label(text="")
        self.add_widget(lb)

        self.fields = []

    def add_property(self, prop, name, value=0):
        lb = Label(text=name)
        self.add_widget(lb)
        ti = PropInput(prop=prop, text=str(value))
        self.add_widget(ti)
        self.fields.append([lb, ti])

    def entity_read(self, entity=None):
        if len(self.fields):
            if self.panda3d.kyvi_focused_ti:
                self.panda3d.kyvi_focused_ti.on_text_validate()

        if self.entity and self.entity.geom:
            self.entity.geom.setTextureOff(0)
            self.entity.geom.clearColorScale()

        if entity:
            self.entity = entity
            if self.entity.geom:
                self.entity.geom.setTextureOff(1)
                self.entity.geom.setColorScale(1, 0, 0, 0.7)

        for wid in self.fields:
            self.remove_widget(wid[0])
            self.remove_widget(wid[1])
        #print("read")
        #print(dir(self.entity))
        for prop in self.entity.get_properties():
        #for prop in dir(self.entity):
            #if self.entity.is_public(prop):
            #self.add_property(prop, self.entity.prop_name(prop), inspect.getattr_static(self.entity, prop))
            self.add_property(prop, self.entity.prop_name(prop), getattr(self.entity, prop))

    def entity_set_prop(self, name, value):
        last_value = getattr(self.entity, name, None)
        val = value
        if isinstance(last_value, float):
            val = float(val)
        if type(last_value) is type(val):
            setattr(self.entity, name, val)
        else:
            print("El tipo de asignación no corresponde: {},{}->{}".format(name, type(self.entity.__dict__[name]), type(val)))


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
        if self.active and not self.panda3d.kyvi_focused_ti:
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

    def on_focus(self, instance, value):
        if value:
            self.parent.panda3d.kyvi_focused_ti = instance
        else:
            if self.parent.panda3d.kyvi_focused_ti is instance:
                self.parent.panda3d.kyvi_focused_ti = None


class PropInput(TextInput):
    def __init__(self, prop, **kwargs):
        super(PropInput, self).__init__(**kwargs)
        self.prop_name = prop
        self.multiline = False

    def on_text_validate(self):
        print(self.prop_name)
        if self.parent:
            self.parent.entity_set_prop(self.prop_name, self.text)

    def on_focus(self, instance, value):
        if self.parent:
            if value:
                self.parent.panda3d.kyvi_focused_ti = instance
            else:
                self.on_text_validate()

                if self.parent.panda3d.kyvi_focused_ti is instance:
                    self.parent.panda3d.kyvi_focused_ti = None

