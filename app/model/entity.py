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
        self._editor_properties = []
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

    """def is_public(self, name):
        print("is_public")
        print(type(name))

        if name in self._editor_properties:
            return True

        if (name[0] is "_" or name in self._hide) or name not in self.__dir__:
            response = False
        else:
            response = True

        return response"""

    def hide_properties(self, *args):
        for prop in args:
            if prop in self._editor_properties:
                self._editor_properties.remove(prop)

    def show_properties(self, *args):
        for arg in args:
            if arg not in self._editor_properties:
                self._editor_properties.append(arg)

    def set_prop_name(self, **kwargs):
        self._namespace.update(kwargs)

    def get_properties(self):

        for prop in self._editor_properties:
            yield prop

    """def get_properties(self):
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
        return attr2"""


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