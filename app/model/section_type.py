from app.model.entity import Entity
from app import app
from .profile_shapes import ProfileShapeFillRect

from .profile_shapes.profile_shape_I import ProfileShapeI
from .transaction import Transaction

shape_codes = {"1": "Ángulo",
               "2": "Ángulo lados desiguales",
               "3": "Sección doble T",
               "4": "Sección T",
               "5": "Tubo circular",
               "6": "Tubo rectangular",
               "7": "Tubo redondeado",
               "8": "Cajón",
               "9": "Canal recto",
               "10": "Canal alas oblicuas",
               "11": "Canal conformado en frío",
               "12": "Perfil C",
               "13": "Perfil U",
               "14": "Rectangular",
               "15": "Circular"}

section_shapes = {"ProfileShapeI": ProfileShapeI,
                  "ProfileShapeFillRect": ProfileShapeFillRect}

class SectionType(Entity):
    global shape_codes

    @staticmethod
    def create_from_object(obj):
        entity_id = obj.get("entity_id")
        name = obj.get("name")

        return SectionType(name, entity_id)

    def __init__(self, name, set_id=None):
        super().__init__(set_id)

        self._name = "None"
        self.name = name
        self.shape = None
        self._sections = []

        self.show_properties("name", "shape")
        self.set_prop_name(name="Nombre", shape="Forma")
        self.set_combo_box_properties("shape")

    def valid_values_shape(self):
        values = [None]

        '''for shape in shape_codes.values():
            values.append(shape)'''

        for name, shape_class in section_shapes.items():

            shapes = app.model_reg.find_entities(name)

            if not shapes:
                tr = Transaction()
                tr.start("Init section Shapes")
                shape = shape_class.create_from_object({})
                tr.commit()
            else:
                shape = list(shapes)[0]

            values.append(shape)

        return values

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        if isinstance(value, str):

            for name in section_shapes.keys():
                shape = app.model_reg.find_entities(name)
                shape = list(shape)
                if shape and shape[0].name == value:
                    value = shape[0]

                break
            else:
                return

        if isinstance(value, str):
            raise Exception("Shape is str")

        self._shape = value

    def add_section(self, section):
        if section not in self._sections:
            self._sections.append(section)

        if len(self._sections) > 0:
            self.set_read_only("shape")

    def remove_section(self, section):
        if section in self._sections:
            self._sections.remove(section)

        if len(self._sections) == 0:
            self.unset_read_only("shape")

    def get_sections(self):
        return self._sections

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):

        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("MaterialGroup")

        iterate = False

        i = 2

        for entity in entities:
            if entity is not self:
                if entity.name == value:
                    iterate = True

                    if not value[:-1].endswith("_copy"):
                        value += "_copy1"
                        i = 2
                    else:
                        i = int(value[-1])+1

        while iterate:
            iterate = False

            for entity in entities:
                if entity is not self:
                    if entity.name == value:
                        iterate = True
                        value = value[:-len(str(i-1))] + str(i)
                        i += 1
                        break

        self._name = value

    def delete(self, force_delete=False):

        if len(self._sections) > 0 and not force_delete:
            return False
        else:
            for material in self._sections:
                material.delete()

        return super(SectionType, self).delete()
