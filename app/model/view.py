from app.controller.console import execute
from app.model.entity import Entity, register
from app import app

class View(Entity):

    @staticmethod
    def create_from_object(obj):

        entity_id = obj.get("entity_id")
        work_plane_height = obj.get("work_plane_height")
        work_plane_vect = obj.get("work_plane_height")

        view = View(entity_id)
        view.work_plane_height = work_plane_height
        view.work_plane_vect = work_plane_vect

        return view

    def __init__(self, set_id=None):
        super().__init__(set_id)
        self.count_memory_references()

        #self.set_prop_name(work_plane_vect="Plano de Trabajo", worl_plane_height="Altura")
        #self.show_properties("work_plane_vect", "work_plane_height")

        self.set_prop_name(show_load="Carga visible")
        self.show_properties("show_load")

        self.set_prop_name(show_combination="Comb. visible")
        self.show_properties("show_combination")

        self.show_properties("scale")
        self.set_prop_name(scale="Escala Diagramas")

        self.show_properties("show_moment", "show_shear", "show_normal")
        self.set_prop_name(show_moment="Momento", show_shear="Corte", show_normal="Normal")

        self.set_combo_box_properties("show_load", "show_combination")

    @property
    def scale(self):
        return round(app.diagram_scale, 2)

    @scale.setter
    def scale(self, value):
        app.diagram_scale = value

        execute("regen")

    @property
    def show_load(self):
        return app.show_load

    @show_load.setter
    def show_load(self, value: str):
        app.show_load = value
        execute("regen")

    @staticmethod
    def valid_values_show_load():
        # Obtenemos el registro del modelo
        entities = app.model_reg.find_entities("LoadCase")

        values = [None]

        for ent in entities:
            values.append(ent.load_code)

        return values

    @property
    def show_moment(self):
        return app.show_moment

    @show_moment.setter
    def show_moment(self, value: str):
        app.show_moment = value
        execute("regen")

    @property
    def show_shear(self):
        return app.show_shear

    @show_shear.setter
    def show_shear(self, value: str):
        app.show_shear = value
        execute("regen")

    @property
    def show_normal(self):
        return app.show_normal

    @show_normal.setter
    def show_normal(self, value: str):
        app.show_normal = value
        execute("regen")

    @property
    def show_combination(self):
        return app.show_combination

    @show_combination.setter
    def show_combination(self, value: str):
        app.show_combination = value
        execute("regen")

    @staticmethod
    def valid_values_show_combination():
        # Obtenemos el registro del modelo
        entities = app.model_reg.find_entities("LoadCombination")

        values = [None]

        for ent in entities:
            values.append(ent.equation)

        return values

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