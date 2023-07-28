from app.model.entity import Entity
import numpy as np
from app.view import draw
from app import app
from .material import Material
from .rebar_set import RebarSet, RebarType, RebarLocation
from . import unit_manager

from typing import TYPE_CHECKING
from typing import List

from .transaction import LoadModelAction, TM

if TYPE_CHECKING:
    # Imports only for IDE type hints
    from app.model import *

import ifc_tools


class Bar(Entity):

    @staticmethod
    def create_from_object(obj):
        print("intentando crear desde objeto")

        def get(string):
            return app.model_reg.get_entity(obj.get(string))
    
        start = get("start")
        end = get("end")
        sec = get("section")
        mat = get("material")
        entity_id = obj.get("entity_id")
        name = obj.get("name")

        bar = Bar(start, end, sec, mat, entity_id)
        bar.name = name
        bar.behavior = obj.get("behavior")

        return bar


    def __init__(self, start, end, section, material=None, set_id=None):
        super().__init__(set_id)
        self.name = ""
        self._start = start
        self._end = end

        self.start: Node = start
        self.end: Node = end
        self._section: Section = section

        if material is None:
            #material = Material(20 * (10 ** 9))
            material = app.default_material
        self._material: Material = material
        self.material = str(material)
        self._width = 0.2
        self._height = 0.3
        self.borders = True
        self._behavior = "Barra"
        self._section_vertex_data_id = None

        self.loads: List[Load] = []

        self.start.add_child_model(self)
        self.end.add_child_model(self)
        self.max_moment = 0
        self.min_moment = 0

        self.show_properties("name")
        #self.show_properties("width", "height")
        self.set_temp_properties("start_x", "start_y", "start_z")
        self.set_temp_properties("end_x", "end_y", "end_z")
        self.set_temp_properties("borders", "height","width", "max_moment", "min_moment")

        #self.show_properties("start_x", "start_y", "start_z")
        self.show_properties("start_x", "start_z")
        self.set_prop_name(start_x="Incio x", start_y="Incio y", start_z="Incio z")
        #self.show_properties("end_x", "end_y", "end_z")
        self.show_properties("end_x", "end_z")
        self.set_prop_name(end_x="Fin x", end_y="Fin y", end_z="Fin z")

        self.section_type = section.section_type # type: SectionType
        self.show_properties("section_type")
        self.set_prop_name(section_type="Catálogo")
        self.set_combo_box_properties("section_type")

        self.show_properties("section")
        self.set_prop_name(section="Sección")
        self.set_combo_box_properties("section")
        self.bind_to_model("section")

        self.show_properties("material")
        self.set_prop_name(material="Material")

        self.show_properties("behavior")
        self.set_prop_name(behavior="Comportamiento")

        self.cc = 2 * unit_manager.ureg("cm")
        self.set_prop_name(cc="Recubrimiento")
        self.show_properties("cc")
        self.show_properties("lenght")
        self.set_prop_name(lenght="Longitud")
        self.set_read_only("lenght")
        self.set_units(lenght="m")
        #self.show_properties("max_moment", "min_moment")
        #self.set_prop_name(max_moment="Momento Máx.", min_moment="Momento Min.")

        self.bind_to_model("width", "height", "loads", "start", "end")

        self.rebar_sets = list()

        self.set_combo_box_properties("behavior", "material")


        self.create_model()

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        print("--set start--")
        print(type(self.start.__reference__))
        print(self.start)
        check = self.start and self.start.__reference__ != None

        if self.start and self.start.__reference__ != None:
            check2 = self.start and self.start.__reference__ != None
            try:
                self.start.remove_child_model(self)
            except Exception as ex:
                print("----")
                print(self.start)
                print(self.start.__reference__)
                print(self.start.__reference__ is not None)
                print(check)
                print(check2)
                check3 = self.start and self.start.__reference__ != None
                print(check3)
                print("----")
                raise Exception(ex)

        self._start = value

        if value:
            self._start.add_child_model(self)



    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        if self.end:
            self.end.remove_child_model(self)

        self._end = value
        if value:
            self.end.add_child_model(self)

    @staticmethod
    def valid_values_section_type():
        values = [None]
        for section_type in app.model_reg.find_entities("SectionType"):
            values.append(section_type)

        return values

    @staticmethod
    def valid_values_behavior():
        return ["Barra", "Viga", "Columna"]

    @property
    def behavior(self):
        return self._behavior

    @behavior.setter
    def behavior(self, value: str):
        if value in ["Barra", "Viga", "Columna"]:
            self._behavior = value

    def valid_values_section(self):
        values = [None]

        for sec in self.section_type.get_sections():
            values.append(sec)

        return values

    @property
    def section(self):
        return self._section

    @section.setter
    def section(self, value):

        if hasattr(self, "_section") and self._section:
            old_sec = self._section # type: Section
            old_sec.remove_child_model(self)

        if type(value).__name__ == "EntityReference":
            value.add_child_model(self)
            self._section = value
        else:
            raise Exception(type(value).__name__)

    @staticmethod
    def valid_values_material():
        groups = app.model_reg.find_entities("MaterialGroup") #type: List[MaterialGroup]
        values = [None]
        for group in groups:
            mats = group.get_materials() #type: List[Material]
            for mat in mats:
                values.append("{}: {}".format(group.name, mat.name))

        return values

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, value: str):
        if ": " not in value and ":" in value:
            value = value.replace(":", ": ", 1)

        if ": " in value:
            group, mat_name = value.split(": ", 1)
            entities = app.model_reg.find_entities("MaterialGroup")

            for material_group in entities:
                if material_group.name == group:
                    material_list = material_group.get_materials()
                    for material_elem in material_list:
                        if material_elem.name == mat_name:
                            self._material = material_elem
                            break
                    break
            else:
                print("material_group no encontrado")

        elif value == "":
            self._material = app.default_material


    def __str__(self):
        if self.name is "":
            name_start = self.start.name
            name_end = self.end.name

            if name_start is not "" and name_end is not "":
                name = "{} {}-{}".format(self.behavior, name_start, name_end)
            else:
                name = None
        else:
            name = "{} {}".format(self.behavior, self.name)

        if name is None:
            return super().__str__()
        else:
            return name

    def add_load(self, new_load):
        self.loads.append(new_load)

    def set_load(self, new_load):
        self.loads = [new_load]

    def get_loads(self):
        for load_entity in self.loads:
            yield load_entity

    @property
    def lenght(self):
        return self.longitude()

    def longitude(self):
        start = self.start.position[0], self.start.position[1], self.start.position[2]
        end = self.end.position[0], self.end.position[1], self.end.position[2]

        delta_x = end[0] - start[0]
        delta_y = end[1] - start[1]
        delta_z = end[2] - start[2]

        long = np.linalg.norm([delta_x, delta_y, delta_z])
        #long = ( delta_x**2 + delta_y**2)**0.5
        return long


    '''@property
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
        self.section.size[1] = value'''

    @property
    def start_x(self):
        return self.start.x

    @start_x.setter
    def start_x(self, value: str):
        self.start.x = value

    @property
    def start_y(self):
        return self.start.y

    @start_y.setter
    def start_y(self, value: str):
        self.start.y = value

    @property
    def start_z(self):
        return self.start.z

    @start_z.setter
    def start_z(self, value: str):
        self.start.z = value

    @property
    def end_x(self):
        return self.end.x

    @end_x.setter
    def end_x(self, value: str):
        self.end.x = value

    @property
    def end_y(self):
        return self.end.y

    @end_y.setter
    def end_y(self, value: str):
        self.end.y = value

    @property
    def end_z(self):
        return self.end.z

    @end_z.setter
    def end_z(self, value: str):
        self.end.z = value

    def create_model(self):
        self.geom = [None, None]
        if self.section:
            self.geom[0] = self.section.generate_geom()
            self.geom[0].setTag('entity_type', self.__class__.__name__)
            self.geom[0].setTag('entity_id', self.entity_id)
            self._section_vertex_data_id = id(self.section.get_vertex_data())

            active_transaction = TM.get_active_transaction()
            action = LoadModelAction(self.geom[0])
            active_transaction.register_action(action)

        if not self.geom[0]:
            self.geom[0] = self.load_model("data/geom/beam")

        #self.geom[0].set_two_sided(True)
        self.update_model()

    def update_model(self):
        if self._section_vertex_data_id != id(self.section.get_vertex_data()):
            self.geom[0].removeNode()

            self.geom[0] = self.section.generate_geom()
            self.geom[0].setTag('entity_type', self.__class__.__name__)
            self.geom[0].setTag('entity_id', self.entity_id)
            self._section_vertex_data_id = id(self.section.get_vertex_data())


        geom = self.geom[0]
        x0, y0, z0 = self.start.position
        x1, y1, z1 = self.end.position
        geom.setPos(x0, y0, z0)

        b = 1
        h = 1

        x = x1 - x0
        y = y1 - y0
        z = z1 - z0
        vector = [x, y, z]
        norm = np.linalg.norm(vector)
        norm = max(norm, 0.001)
        geom.setScale(b, norm, h)
        geom.setShaderInput("showborders", self.borders, self.borders, self.borders, self.borders)

        geom.lookAt(self.end.geom[0])



        if app.wireframe is True:
            geom.hide()
            geom.setScale(0.01, norm, 0.05)

            line = self.geom[1]
            if line is not None:
                line.removeNode()
            if not self.hidden:
                line = self.draw_line_3d(x0, y0, z0, x1, y1, z1, 3, "C_BLUE")

                line.setDepthOffset(1)
                self.geom[1] = line

        else:
            if not self.hidden:
                geom.show()

            line = self.geom[1]
            if line is not None:
                line.removeNode()
                self.geom[1] = None

    def show(self):
        self.hidden = False
        self.update_model()

    def generate_ifc(self, ifc_file):
        owner_history = ifc_file.by_type("IfcOwnerHistory")[0]
        context = ifc_file.by_type("IfcGeometricRepresentationContext")[0]

        x0 = float(self.start.x)
        y0 = float(self.start.y)
        z0 = float(self.start.z)

        x1, y1, z1 = self.end.position
        x = float(x1 - x0)
        y = float(y1 - y0)
        z = float(z1 - z0)
        vector = [x, y, z]
        norm = np.linalg.norm(vector)

        placement = ifc_tools.create_ifclocalplacement(ifc_file,
                                                       relative_to=ifc_file.storey_placement,
                                                       point=(x0, y0, z0),
                                                       dir1=(x, y, z))
        polyline = ifc_tools.create_ifcpolyline(ifc_file, [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)])

        axis_representation = ifc_file.create_entity(type="IfcShapeRepresentation",
                                                     ContextOfItems=context,
                                                     RepresentationIdentifier="Axis",
                                                     RepresentationType="Curve2D",
                                                     Items=[polyline])

        extrusion_placement = ifc_tools.create_ifcaxis2placement(ifc_file, (0.0, 0.0, 0.0))

        h, w = self.section.size
        w = float(w)
        h = float(h)

        point_list_extrusion_area = [(0.0, -0.1, 0.0),
                                     (0.2, -0.1, 0.0),
                                     (0.2, 0.1, 0.0),
                                     (0.0, 0.1, 0.0),
                                     (0.0, -0.1, 0.0)]

        point_list_extrusion_area = [(-w/2, -h/2, 0.0),
                                     ( w/2, -h/2, 0.0),
                                     ( w/2,  h/2, 0.0),
                                     (-w/2,  h/2, 0.0),
                                     (-w/2, -h/2, 0.0)]

        solid = ifc_tools.create_ifcextrudedareasolid(ifc_file, point_list_extrusion_area, extrusion_placement,
                                                      (0.0, 0.0, 1.0), norm)

        body_representation = ifc_file.createIfcShapeRepresentation(ContextOfItems=context,
                                                                    RepresentationIdentifier="Body",
                                                                    RepresentationType="SweptSolid",
                                                                    Items=[solid])

        product_shape = ifc_file.createIfcProductDefinitionShape(
            Representations=[axis_representation, body_representation])

        print("id: {}".format(self.entity_id))
        ifcid = ifc_tools.create_guid()
        print("GlobalId: {}".format(ifcid))

        #IfcStructuralCurveMember
        self.ifc_entity = ifc_file.create_entity(type="IfcBeam",
                                                 GlobalId=self.entity_id,
                                                 OwnerHistory=owner_history,
                                                 Name="Mi Columna",
                                                 Description="Soy una columna",
                                                 ObjectPlacement=placement,
                                                 Representation=product_shape
                                                 )

        return self.ifc_entity

    def get_lower_main_rebar(self):
        for rebar in self.rebar_sets:
            if rebar.rebar_type is RebarType.DEFAULT:
                if rebar.location is RebarLocation.LOWER:
                    return rebar

    def get_upper_main_rebar(self):
        for rebar in self.rebar_sets:
            if rebar.rebar_type is RebarType.DEFAULT:
                if rebar.location is RebarLocation.UPPER:
                    return rebar


