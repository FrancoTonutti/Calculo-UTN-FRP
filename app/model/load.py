from app.model.entity import Entity, register
from app.model import Bar, Node
from app.view import draw
import numpy as np
from app import app


class Load(Entity):
    """
    bar: parent bar
    load_type: string  = "D", "L", "W", "S" etc.
    value: float
    """
    scale = 0.25

    def __init__(self, parent, value, angle=90, load_type="D"):
        super().__init__()
        self.parent = parent
        self.value = value
        self.angle = angle
        self.load_type = load_type

        self._scheme = dict()
        self.show_properties("value", "angle", "load_type")
        self.set_prop_name(value="Valor", angle="Ángulo", load_type="Tipo")
        self.bind_to_model("value", "angle")
        self.parent.add_child_model(self)

        register(self)
        self.create_model()

    def create_model(self):
        if isinstance(self.parent, Node):
            model = app.base.loader.loadModel("data/geom/beam")

            model.setTag('entity_type', self.__class__.__name__)
            model.setTag('entity_id', self.entity_id)
            model.hide()

            self.geom = [model, None]
        elif isinstance(self.parent, Bar):
            model = app.base.loader.loadModel("data/geom/plate")
            model.set_two_sided(True)
            model.setTag('entity_type', self.__class__.__name__)
            model.setTag('entity_id', self.entity_id)
            self.geom = [model]


        self.update_model()

    def update_model(self):
        if isinstance(self.parent, Node):
            x0, y0, z0 = self.parent.position
            x = self.value * Load.scale
            y = 0
            z = 0

            # Rotate points
            angle = np.deg2rad(self.angle)
            print("ANGLE", angle)

            x1 = x * np.cos(angle) - y * np.sin(angle)
            z1 = x * np.sin(angle) + z * np.cos(angle)

            x1 = x0 + x1
            y1 = 0
            z1 = z0 + z1
            print(x0, y0, z0, x1, y1, z1)
            model = self.geom[0]

            model.setPos(x0, y0, z0)
            model.lookAt(x1, y1, z1)
            model.reparentTo(app.base.render)
            model.setScale(0.1, self.value * Load.scale, 0.1)

            line = self.geom[1]
            if line is not None:
                line.removeNode()
            line = draw.draw_line_3d(x0, y0, z0, x1, y1, z1, color="C_ORANGE")

            self.geom = [model, line]
        elif isinstance(self.parent, Bar):
            x0, y0, z0 = self.parent.start.position
            x1, y1, z1 = self.parent.end.position
            model = self.geom[0]
            #model.setPos(x0, y0, z0)
            model.setHpr(0, 0, 90)
            #model.setColorScale(1, 0, 0, 1)

            model_parent = self.parent.geom[0]
            parent_scale = model_parent.getScale()
            #model.reparentTo(app.base.render)
            model.reparentTo(model_parent)

            h = self.value * Load.scale
            x = x1 - x0
            y = y1 - y0
            z = z1 - z0
            vector = [x, y, z]
            L = np.linalg.norm(vector)
            model.setScale(h/parent_scale[2], L/parent_scale[1],1/parent_scale[0])
            model.setPos(0, (L / 2)/parent_scale[1], 0.5*h/parent_scale[2])

            #model.wrtReparentTo(app.base.render)
            model.setLightOff()
            print("L", L)
            print("h", h)


    def delete_model(self):
        pass
