from app import app
import uuid

LANG = {
    "start": "Inicio",
    "end": "Fin",
    "section": "Sección",
    "material": "Material",
    "width": "Ancho",
    "height": "Alto",
    "name": "Nombre"
}


class Entity:
    def __init__(self):
        self._entity_id = str(uuid.uuid4())
        self._geom = None
        self._hide = []
        self._show = []
        self._read_only = []
        self._namespace = dict()

    @property
    def entity_id(self):
        return self._entity_id

    @property
    def geom(self):
        return self._geom

    @geom.setter
    def geom(self, data):
        self._geom = data

    def prop_name(self, prop):
        if prop in self._namespace:
            return self._namespace.get(prop, None)
        if prop in LANG:
            return LANG.get(prop)
        else:
            return prop

    def is_public(self, name):
        print("is_public")
        print(type(name))

        if name in self._show:
            return True

        if (name[0] is "_" or name in self._hide) or name not in self.__dir__:
            response = False
        else:
            response = True

        return response

    def hide_properties(self, *args):
        for arg in args:
            if arg not in self._hide:
                self._hide.append(arg)

    def show_properties(self, *args):
        for arg in args:
            if arg not in self._show:
                self._show.append(arg)

    def set_prop_name(self, **kwargs):
        self._namespace.update(kwargs)

    def get_properties(self):
        attrs = list(self.__dict__.keys())
        i = 0
        attr2 = list()
        for attr in attrs:
            name = str(attr)
            if name[0] is "_" or name in self._hide:
                pass
            else:
                attr2.append(attr)
            i += 1

        for prop in self._show:
            if prop not in attr2:
                attr2.append(prop)
        return attr2


def register(entity):
    # Obtenemos el registro del modelo
    model_reg = app.model_reg

    # Leemos el nombre de la clase
    name = type(entity).__name__

    # Extraemos el diccionario con todos los elementos de la categoría, si no existe lo creamos
    category_dict = model_reg.get(name, None)
    if category_dict is None:
        category_dict = dict()
        model_reg.update({name: category_dict})

    # Agregamos el modelo al diccionario
    category_dict.update({entity.entity_id: entity})


class View(Entity):
    def __init__(self):
        super().__init__()

        self.hide_properties("panda3d")
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


class Node(Entity):
    def __init__(self, x, y, z=0, name=""):
        super().__init__()
        self.position = [x, y, z]
        self.name = name
        self.hide_properties("position")
        self.set_prop_name(position_str="Posición")
        self.show_properties("position_str")
        register(self)

    def __str__(self):
        x = round(self.position[0]*100)/100
        z = round(self.position[2]*100)/100
        return "{}, {}".format(x, z)

    @property
    def position_str(self):
        x, y, z = self.position
        x = round(x, 2)
        y = round(y, 2)
        z = round(z, 2)

        return "{}, {}, {}".format(x, y, z)

    @position_str.setter
    def position_str(self, value: str):
        value = value.split(",", 3)
        if len(value) is 3:
            x, y, z = value
            x = float(x)
            y = float(y)
            z = float(z)
            self.position = [x, y, z]


class Bar(Entity):

    def __init__(self, start, end, section, material=None):
        super().__init__()
        self.start = start
        self.end = end
        self.section = section
        self.material = material
        self._width = 0.2
        self._height = 0.3
        self.hide_properties("section", "material", "start", "end")
        self.set_prop_name(start_str="Incio", end_str="Fin")
        self.show_properties("width", "height", "start_str", "end_str")
        register(self)

    @property
    def width(self):
        return self.section.size[0]

    @width.setter
    def width(self, value):
        print("setter width")
        self.section.size[0] = value

    @property
    def height(self):
        return self.section.size[1]

    @height.setter
    def height(self, value):
        print("setter height")
        self.section.size[1] = value

    @property
    def start_str(self):
        return self.start.position_str

    @start_str.setter
    def start_str(self, value: str):
        self.start.position_str = value

    @property
    def end_str(self):
        return self.end.position_str

    @end_str.setter
    def end_str(self, value: str):
        self.end.position_str = value

    def __str__(self):
        return "<class 'app.model.core.Bar'>"










class Section:
    def __init__(self, width, height):
        self.entity_id = str(uuid.uuid4())
        self.size = [width, height]
        register(self)

    def __str__(self):
        return "<class 'app.model.core.Section'>"
