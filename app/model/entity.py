from app import app
import uuid



from typing import TYPE_CHECKING
from typing import List
if TYPE_CHECKING:
    # Imports only for IDE type hints
    pass
from ifcopenshell import guid
from ifcopenshell.file import file

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
    def __init__(self, set_id=None):
        #self._entity_id = str(uuid.uuid1())
        if not set_id:
            self._entity_id = guid.new()
        else:
            self._entity_id = set_id

        self._geom = None
        self._editor_properties = []
        self._read_only = []
        self._namespace = dict()
        self._child_models = list()
        self._bind_model = list()
        self._analysis_results = dict()
        self.is_selectable = True
        self.is_editable = True
        self.is_selected = False
        self.ifc_entity = None

        self.register()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None

    def set_analysis_results(self, name, value):
        self._analysis_results.update({name: value})

    def get_analysis_results(self, name):
        return self._analysis_results.get(name, None)

    def on_click(self):
        pass

    def generate_ifc(self, ifc_file: file):
        pass

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

    def load_model(self, model, set_id=True, parent=None):
        if parent is None:
            parent = app.base.render

        node = app.base.loader.loadModel(model)
        if set_id:
            print("entity_type", self.__class__.__name__)
            node.setTag('entity_type', self.__class__.__name__)
            node.setTag('entity_id', self.entity_id)

        node.reparentTo(parent)
        return node

    def create_model(self):
        pass

    def update_model(self):
        pass

    def delete_model(self):
        pass

    def update_tree(self):
        self.update_model()
        for child in self._child_models:
            child.update_tree()

    def add_child_model(self, child):
        self._child_models.append(child)

    def bind_to_model(self, *args):
        for prop in args:
            if prop not in self._bind_model:
                self._bind_model.append(prop)

    def __setattr__(self, name, value):
        update = False
        if hasattr(self, "_bind_model") and name in self._bind_model:
            if getattr(self, name) != value:
                update = True
                
        super(Entity, self).__setattr__(name, value)

        if update:
            self.update_tree()

    def register(self):
        # Obtenemos el registro del modelo
        model_reg = app.model_reg

        # Leemos el nombre de la clase
        name = type(self).__name__

        # Extraemos el diccionario con todos los elementos de la categoría, si no existe lo creamos
        category_dict = model_reg.get(name, None)
        if category_dict is None:
            category_dict = dict()
            model_reg.update({name: category_dict})

        # Agregamos el modelo al diccionario
        category_dict.update({self.entity_id: self})

        if self.entity_id in model_reg.entity_register:
            raise Exception("ID duplicada")
        else:
            model_reg.entity_register.update({self.entity_id: self})

    def delete(self):
        pass

    @staticmethod
    def create_from_object(obj):
        print("intentando crear desde objeto")
        pass


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

