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
    scale = 0.5

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

    def delete_model(self):
        pass
