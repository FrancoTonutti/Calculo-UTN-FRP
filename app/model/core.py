from kivy.app import App
import uuid

def register(category, entity):
    app = App.get_running_app()
    model_reg = app.root.panda3D.model_reg

    cat = model_reg.get(category, None)
    if cat is None:
        cat = list()
        model_reg.update({category: cat})

    cat.append(entity)


class Node:
    def __init__(self, x, y, z=0, name=""):
        self.id = str(uuid.uuid4())
        self.position = [x, y, z]
        self.name = name
        self.geom = None
        register("Node", self)

    def __str__(self):
        return "<class 'app.model.core.Node'>"


class Bar:
    def __init__(self, start, end, section, material=None):
        self.id = str(uuid.uuid4())
        self.start = start
        self.end = end
        self.section = section
        self.material = material
        self.geom = None
        register("Bar", self)

    def __str__(self):
        return "<class 'app.model.core.Bar'>"


class Section:
    def __init__(self, width, height):
        self.id = str(uuid.uuid4())
        self.size = [width, height]
        register("Section", self)

    def __str__(self):
        return "<class 'app.model.core.Section'>"
