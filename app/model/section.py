from app.model.entity import Entity, register
from app.model.section_type import SectionType
from app import app

class Section(Entity):
    last_section = None

    @staticmethod
    def create_from_object(obj):
        entity_id = obj.get("entity_id")
        width, height = obj.get("size")

        return Section(width, height, entity_id)

    def __init__(self, name: str, section_type: SectionType, geometry: dict, set_id=None):
        super().__init__(set_id)
        width = 0
        height = 0
        self.name = name
        self.show_properties("name")
        self.size = [width, height]
        self._geometry = None
        self._section_type = None
        self.section_type = section_type
        self.set_geometry(geometry)



        register(self)
        Section.last_section = self

    def set_geometry(self, geometry):
        self._geometry = geometry

    @property
    def section_type(self):
        return self._section_type

    @section_type.setter
    def section_type(self, value):
        if not value or isinstance(value, str):
            print("Material section_type: {}".format(value))
            raise Exception("check this")
        else:
            reset_name = False
            if self._section_type:
                reset_name = True
                self._section_type.remove_section(self)

            value.add_section(self)
            self._section_type = value

            shape = value.shape

            #for param in shape.params:



            for param in shape.params:
                self.set_units(**{param: "mm"})
                setattr(self, param, 0*app.ureg("mm"))





            self.show_properties(*shape.params)
            '''if reset_name:
                self.name = self._name'''

    def delete(self):
        if self._section_type:
            self._section_type.remove_section(self)

        super(Section, self).delete()

    def inertia_x(self):
        b = self.size[0]
        h = self.size[1]
        return (b * pow(h, 3)) / 12

    def inertia_y(self):
        b = self.size[0]
        h = self.size[1]
        return (h * pow(b, 3)) / 12

    def area(self):
        return self.size[0] * self.size[1]

    def __str__(self):
        return "<class 'app.model.core.Section'>"
