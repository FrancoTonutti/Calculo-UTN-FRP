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


class Line(Entity):

    @staticmethod
    def create_from_object(obj):
        print("intentando crear desde objeto")

        def get(string):
            return app.model_reg.get_entity(obj.get(string))
    
        start = get("start")
        end = get("end")

        entity_id = obj.get("entity_id")
        name = obj.get("name")

        line = Line(start, end, entity_id)
        line.name = name
        line.behavior = obj.get("behavior")

        return line

    def __init__(self, start, end, set_id=None):
        super().__init__(set_id)
        self.name = ""
        self._start = start
        self._end = end

        self.start: Node = start
        self.end: Node = end

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

        self.show_properties("lenght")
        self.set_prop_name(lenght="Longitud")
        self.set_read_only("lenght")
        self.set_units(lenght="m")

        self.bind_to_model("loads", "start", "end")

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

    def __str__(self):
        if self.name is "":
            name_start = self.start.name
            name_end = self.end.name

            if name_start is not "" and name_end is not "":
                name = "Línea {}-{}".format(name_start, name_end)
            else:
                name = None
        else:
            name = "Línea {}".format(self.name)

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
        """        
        if self.section:
            self.geom[0] = self.section.generate_geom()
            self.geom[0].setTag('entity_type', self.__class__.__name__)
            self.geom[0].setTag('entity_id', self.entity_id)
            self._section_vertex_data_id = id(self.section.get_vertex_data())

            active_transaction = TM.get_active_transaction()
            action = LoadModelAction(self.geom[0])
            active_transaction.register_action(action)
        """
        if not self.geom[0]:
            self.geom[0] = self.load_model("data/geom/beam")

        #self.geom[0].set_two_sided(True)
        self.update_model()

    def update_model(self):
        """if self._section_vertex_data_id != id(self.section.get_vertex_data()):
            self.geom[0].removeNode()

            self.geom[0] = self.section.generate_geom()
            self.geom[0].setTag('entity_type', self.__class__.__name__)
            self.geom[0].setTag('entity_id', self.entity_id)
            self._section_vertex_data_id = id(self.section.get_vertex_data())"""

        geom = self.geom[0]
        x0, y0, z0 = self.start.position
        x1, y1, z1 = self.end.position
        #geom.setPos(x0, y0, z0)

        b = 1
        h = 1

        x = x1 - x0
        y = y1 - y0
        z = z1 - z0
        vector = [x, y, z]
        norm = np.linalg.norm(vector)
        norm = max(norm, 0.001)
        #geom.setScale(b, norm, h)
        #geom.setShaderInput("showborders", self.borders, self.borders, self.borders, self.borders)

        #geom.lookAt(self.end.geom[0])



        if True:
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
        raise Exception("Not implemented")

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




