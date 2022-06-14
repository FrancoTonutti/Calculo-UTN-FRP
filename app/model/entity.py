import ctypes
import sys

from panda3d.core import GeomNode, CollisionSegment, CollisionNode

from app import app
from .entity_reference import EntityReference
from .transaction import TM, SetAttrAction, EntityCreationAction, \
    LoadModelAction, EntityDeleteAction, Transaction
import uuid



from typing import TYPE_CHECKING
from typing import List

from ..view import draw

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


class EntityMeta(type):
    def __instancecheck__(cls, inst):
        """Implement isinstance(inst, cls)."""

        check = any(
            cls.__subclasscheck__(c) for c in {type(inst), inst.__class__})

        #print('hi Entity __instancecheck__ {}'.format(check))
        #print('self {}'.format(cls))
        #print('other {}'.format(inst))

        if isinstance(inst, EntityReference):
            return isinstance(inst.__reference__, cls)

        return check

    def __subclasscheck__(cls, sub):
        """Implement issubclass(sub, cls)."""
        candidates = cls.__dict__.get("__subclass__", set()) | {cls}
        check = any(c in candidates for c in sub.mro())
        #print('hi __subclasscheck__ {}'.format(check))
        #print('self {}'.format(cls))
        #print('other {}'.format(sub))

        return check


class Entity(metaclass=EntityMeta):
    global TM
    def __init__(self, set_id=None):

        active_transaction = TM.get_active_transaction()
        if active_transaction:
            if not set_id:
                self._entity_id = guid.new()
            else:
                self._entity_id = set_id
            self.__is_deleted__ = False
            self.__references__ = []

            action = EntityCreationAction(self)
            active_transaction.register_action(action)

            self._units = dict()

            self._geom = None
            self._editor_properties = []
            self._read_only = []
            self._namespace = dict()
            self._child_models = list()
            self._bind_model = list()
            self._analysis_results = dict()
            self._temp_properties = []
            self.is_selectable = True
            self.is_editable = True
            self._is_selected = False
            #self.is_selected = False
            self.ifc_entity = None
            self.enabled_save = True

            self.hidden = False
            self._combo_box_properties = []


            self.register()
        else:
            raise Exception("No existe una transacción activa")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None

    def isinstance(self, cls):
        return isinstance(self, cls)

    def add_refence(self, ref):
        if ref not in self.__references__:
            self.__references__.append(ref)

    def remove_reference(self, ref):
        if ref in self.__references__:
            self.__references__.remove(ref)

    def remove_all_references(self):
        for ref in self.__references__:
            ref.__dispose__()

    @property
    def is_selected(self):
        return self._is_selected

    @is_selected.setter
    def is_selected(self, value: bool):
        if self._is_selected != value:
            if value:
                self.on_select()
            else:
                self.on_deselect()

        self._is_selected = value

    def on_select(self):
        pass

    def on_deselect(self):
        pass

    def set_analysis_results(self, load_combination, name, value):

        if isinstance(load_combination, str):
            comb_id = load_combination
        else:
            comb_id = load_combination.entity_id

        combination_results = self._analysis_results.get(comb_id, None)

        if combination_results is None:
            combination_results = dict()

        combination_results.update({name: value})

        self._analysis_results.update({comb_id: combination_results})

    def get_analysis_results(self, load_combination, name):

        if isinstance(load_combination, str):
            comb_id = load_combination
        else:
            comb_id = load_combination.entity_id

        combination_results = self._analysis_results.get(comb_id, None)

        if combination_results is None:
            return None

        return combination_results.get(name, None)

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

    def set_units(self, **kwargs):
        self._units.update(kwargs)

    def set_temp_properties(self, *args):
        for prop in args:
            if prop not in self._temp_properties:
                self._temp_properties.append(prop)

    def is_temp_property(self, prop):
        return prop in self._temp_properties

    def set_combo_box_properties(self, *args):
        for prop in args:
            if prop not in self._combo_box_properties:
                self._combo_box_properties.append(prop)

    def is_combo_box_property(self, prop):
        return prop in self._combo_box_properties

    def get_combo_box_values(self, prop):
        if self.is_combo_box_property(prop) and hasattr(self, "valid_values_"+prop):
            method = getattr(self, "valid_values_"+prop)
            return method()
        else:
            return [None]

    def get_properties(self):
        for prop in self._editor_properties:
            yield prop

    def set_read_only(self, *args):
        for arg in args:
            if arg not in self._read_only:
                self._read_only.append(arg)

    def unset_read_only(self, *args):
        for arg in args:
            if arg in self._read_only:
                self._read_only.remove(arg)

    def is_read_only(self, prop_name: str):
        return prop_name in self._read_only

    def load_model(self, model, set_id=True, parent=None):

        active_transaction = TM.get_active_transaction()
        if active_transaction:
            if parent is None:
                parent = app.base.render

            node = app.base.loader.loadModel(model)
            action = LoadModelAction(node)
            active_transaction.register_action(action)

            if set_id:
                print("entity_type", self.__class__.__name__)
                node.setTag('entity_type', self.__class__.__name__)
                node.setTag('entity_id', self.entity_id)

            node.reparentTo(parent)
            return node
        else:
            raise Exception("No existe una transacción activa")

    def draw_line_3d(self, x1, y1, z1, x2, y2, z2, w=1, color=None, parent=None, dynamic=False, set_id=True):
        result = draw.draw_line_3d(x1, y1, z1, x2, y2, z2, w, color, parent, dynamic)

        if dynamic:
            node, line = result
        else:
            node = result

        if set_id:
            '''center_x = (x1+x2)/2
            center_y = (x1 + x2) / 2
            center_z = (x1 + x2) / 2
            
            segment =CollisionBox(Point3(center_x, y1, z1),Point3(maxx, maxy, maxz)) CollisionSegment(x1, y1, z1, x2, y2, z2)
            cnodePath = node.attachNewNode(CollisionNode('cnode'))
            cnodePath.node().addSolid(segment)'''
            print("entity_type", self.__class__.__name__)
            node.setTag('entity_type', self.__class__.__name__)
            node.setTag('entity_id', self.entity_id)


        return result

    def create_model(self):
        pass

    def update_model(self):
        pass

    def delete_model(self):
        if self.geom:
            num = len(self.geom)
        else:
            num = 0
        if self.geom:
            for geomnode in self.geom:  # type: GeomNode
                if geomnode:
                    geomnode.removeNode()

    def update_tree(self):
        self.update_model()
        for child in self._child_models:
            child.update_tree()

    def add_child_model(self, child):
        self._child_models.append(child)

    def remove_child_model(self, child):
        if child in self._child_models:
            self._child_models.remove(child)

    def bind_to_model(self, *args):
        for prop in args:
            if prop not in self._bind_model:
                self._bind_model.append(prop)

    def __setattr__(self, name, new_value):
        if hasattr(self, "_units"):
            unit = self._units.get(name)
            if unit and (isinstance(new_value, float) or new_value is None):
                if new_value is None:
                    new_value = 0
                new_value = new_value * app.ureg(unit)

        if not isinstance(new_value, EntityReference) and isinstance(new_value, Entity):
            new_value = EntityReference(new_value)
        
        if hasattr(self, name):
            old_value = getattr(self, name)

            if old_value != new_value:
                active_transaction = TM.get_active_transaction()
                if active_transaction:
                    update = False
                    if hasattr(self, "_bind_model") and name in self._bind_model:
                        update = True

                    super(Entity, self).__setattr__(name, new_value)

                    if active_transaction.is_register_enabled():

                        action = SetAttrAction(self, name, old_value, new_value)
                        active_transaction.register_action(action)

                    if update:
                        self.update_tree()
                else:
                    raise Exception("No existe una transacción activa")
        else:
            super(Entity, self).__setattr__(name, new_value)

    @property
    def category_name(self):
        return type(self).__name__

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

            #action = EntityRegisterAction(self)
            #active_transaction.register_action(action)

        self.registered = True

    def unregister(self):
        model_reg = app.model_reg
        # Leemos el nombre de la clase
        name = type(self).__name__

        # Extraemos el diccionario con todos los elementos de la categoría
        category_dict = model_reg.get(name, None)

        # Eliminamos la entidad del diccionario
        category_dict.pop(self.entity_id)
        model_reg.entity_register.pop(self.entity_id)

    def delete(self):

        active_transaction = TM.get_active_transaction()
        if active_transaction:
            self.delete_model()
            self.unregister()

            if active_transaction.is_register_enabled():
                pass
            _tr = Transaction()
            _tr.disable_register()
            _tr.start()
            self.__is_deleted__ = True
            _tr.commit()

        self.remove_all_references()

        print("!!! Remaining references after deleting:", ctypes.c_long.from_address(id(self)).value)

        return True

    def count_memory_references(self):
        try:
            print("!!! References to {}:".format(self),
                  ctypes.c_long.from_address(id(self)).value)
        except Exception as ex:
            print("!!! References to {}:".format(self.category_name),
                  ctypes.c_long.from_address(id(self)).value)

    def __del__(self):
        print("Entidad liberada en memoria")


    @staticmethod
    def create_from_object(obj):
        print("intentando crear desde objeto")
        pass

    def hide(self):
        self.hidden = True
        if self.geom:
            for geom in self.geom:
                if geom:
                    geom.hide()

    def show(self):
        self.hidden = False
        if self.geom:
            for geom in self.geom:
                if geom:
                    geom.show()

        self.update_model()

def register(entity):
    return None
    print("OLD REGISTER {}".format(entity.entity_id))
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

