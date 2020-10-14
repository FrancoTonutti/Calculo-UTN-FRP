from app.model.entity import Entity, register
from app import app

class View(Entity):
    def __init__(self):
        super().__init__()

        self.set_prop_name(work_plane_vect="Plano de Trabajo", worl_plane_height="Altura")
        self.show_properties("work_plane_vect", "work_plane_height")
        register(self)

    @property
    def work_plane_vect(self):
        x, y, z = app.work_plane_vect
        x = round(x, 2)
        y = round(y, 2)
        z = round(z, 2)

        return "{}, {}, {}".format(x, y, z)

    @work_plane_vect.setter
    def work_plane_vect(self, value: str):
        value = value.split(",", 3)
        if len(value) is 3:
            x, y, z = value
            x = float(x)
            y = float(y)
            z = float(z)
            app.work_plane_vect = [x, y, z]

    @property
    def work_plane_height(self):
        x, y, z = app.work_plane_point
        z = str(round(z, 2))
        return z

    @work_plane_height.setter
    def work_plane_height(self, value: str):
        try:
            z = float(value)
            app.work_plane_point = (0, 0, z)
        except Exception as ex:
            print(ex)