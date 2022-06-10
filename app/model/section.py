import random

import numpy as np
from panda3d.core import GeomVertexFormat, GeomVertexData, Geom, \
    GeomVertexWriter, GeomTristrips, GeomNode, GeomTriangles

from app.model.entity import Entity, register
from app.model.section_type import SectionType
from app import app


class Section(Entity):
    last_section = None
    gformat = GeomVertexFormat.get_v3n3c4()

    @staticmethod
    def create_from_object(obj):
        entity_id = obj.get("entity_id")

        def entity_get(string):
            return app.model_reg.get_entity(obj.get(string))

        name = obj.get("name")
        section_type = entity_get("shape")
        section_type.shape = entity_get("shape")

        geometry = obj.get("geometry")

        section = Section(name, section_type, geometry, set_id=entity_id)

        return section

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

        self._contour_points = None
        self._vertex_data = None

        register(self)
        Section.last_section = self

    def set_geometry(self, geometry):
        self._geometry = geometry

        for attr, value in geometry.items():
            if isinstance(value, str):
                setattr(self, attr, app.ureg(value))
            else:
                setattr(self, attr, value*app.ureg("cm"))

    def __str__(self):
        return self.name

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, value):
        self.set_geometry(value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):

        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("Section")

        entities = filter(lambda x: x.section_type == self.section_type, entities)

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
                        i = int(value[-1]) + 1

        while iterate:
            iterate = False

            for entity in entities:
                if entity is not self:
                    if entity.name == value:
                        iterate = True
                        value = value[:-len(str(i - 1))] + str(i)
                        i += 1
                        break

        self._name = value

    @property
    def section_type(self):
        if hasattr(self, "_section_type"):
            return self._section_type
        else:
            return None

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

            print("shape {}")
            print(type(shape))
            print(type(shape.__reference__))
            print(shape.__reference__.params)
            print(shape.__reference__.__dict__)

            for param in shape.params:
                self.set_units(**{param: "mm"})
                setattr(self, param, 0*app.ureg("mm"))


            self.show_properties(*shape.params)
            self.bind_to_model(*shape.params)
            '''if reset_name:
                self.name = self._name'''

    def delete(self):
        if self._section_type:
            self._section_type.remove_section(self)

        super(Section, self).delete()

    def update_model(self):
        self._contour_points = None
        self._vertex_data = None

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

    def get_contour_points(self):

        geometry = {}

        for attr in self.section_type.shape.params:
            value = getattr(self, attr)
            geometry.update({attr: value})

        if self._contour_points is None:
            self._contour_points = self.section_type.get_contour_points(**geometry)

        return self._contour_points

    def get_vertex_data(self):
        if self._vertex_data is None:
            self._vertex_data = self.generate_vertex_data()

        return self._vertex_data

    def generate_geom(self):
        vdata, prim = self.get_vertex_data()
        section_geom = Geom(vdata)
        section_geom.addPrimitive(prim)

        node = GeomNode('gnode')
        node.addGeom(section_geom)

        # noinspection PyUnresolvedReferences
        nodePath = render.attachNewNode(node)
        #nodePath.set_two_sided(True)

        return nodePath

    def generate_vertex_data(self):
        points = self.get_contour_points()

        vdata = GeomVertexData('name', Section.gformat, Geom.UHStatic)
        n = len(points)
        total_vertex = n * 2 + (n - 1)*4

        vdata.setNumRows(total_vertex)

        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color = GeomVertexWriter(vdata, 'color')
        prim = GeomTriangles(Geom.UHStatic)

        triangles = triangulate(points.copy(), self.section_type.shape.is_clockwise)

        i = 0
        for triangle in triangles:
            for point in triangle:
                x, z = point
                vertex.addData3(x, 0, z)
                normal.addData3(0, -1, 0)
                color.addData4(1, 1, 1, 1)
                prim.addVertex(i)
                i += 1
            prim.closePrimitive()

        for triangle in triangles:

            for point in triangle[::-1]:
                x, z = point

                vertex.addData3(x, 1, z)
                normal.addData3(0, 1, 0)
                color.addData4(1, 1, 1, 1)
                prim.addVertex(i)
                i += 1
            prim.closePrimitive()

        if self.section_type.shape.is_clockwise:
            points = points[::-1]

        for i_point in range(n):
            i_start = i
            x0, z0 = points[i_point]
            x1, z1 = points[(i_point + 1) % n]

            vec_x = x1 - x0
            vec_z = z1 - z0

            normal_x = vec_z
            normal_z = -vec_x

            vertex.addData3(x1, 0, z1)
            normal.addData3(normal_x, 0, normal_z)
            color.addData4(1, 1, 1, 1)
            i += 1

            vertex.addData3(x0, 0, z0)
            normal.addData3(normal_x, 0, normal_z)
            color.addData4(1, 1, 1, 1)
            i += 1

            vertex.addData3(x1, 1, z1)
            normal.addData3(normal_x, 0, normal_z)
            color.addData4(1, 1, 1, 1)
            i += 1

            vertex.addData3(x0, 1, z0)
            normal.addData3(normal_x, 0, normal_z)
            color.addData4(1, 1, 1, 1)
            #prim.addVertex(i)
            i += 1

            prim.addVertex(i_start)
            prim.addVertex(i_start+1)
            prim.addVertex(i_start+2)
            prim.closePrimitive()
            prim.addVertex(i_start + 3)
            prim.addVertex(i_start + 2)
            prim.addVertex(i_start + 1)
            prim.closePrimitive()

        return vdata, prim




############

def angle(p1, p2, p3):
    v1 = [p2[0] - p1[0], p2[1] - p1[1]]
    v2 = [p2[0] - p3[0], p2[1] - p3[1]]

    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if norm1 == 0 or norm2 == 0:
        raise Exception("divide by 0")

    dot_product = np.dot(v1, v2)
    angle = np.arccos(dot_product / (norm1 * norm2))

    return angle


def merge_colinear_edges(points):
    n = len(points)
    i = 0
    while i < n and n >= 3:
        i0 = clamp_index(i - 1, 0, n - 1)
        i2 = clamp_index(i + 1, 0, n - 1)

        p0 = points[i0]
        p1 = points[i]
        p2 = points[i2]

        if angle(p0, p1, p2) == 0:
            points.pop(i)
            n = len(points)
        else:
            i += 1

    return points


def get_internal_angles(points, poly_clockwise):
    n = len(points)
    angles = [0] * n
    if n >= 3:
        for i in range(n):
            p1 = points[i]
            p2 = points[(i + 1) % n]
            p3 = points[(i + 2) % n]
            theta = angle(p1, p2, p3)
            triangle_clockwise = is_clockwise(p1, p2, p3)

            if triangle_clockwise != poly_clockwise:
                theta = 2 * np.pi - theta

            angles[(i + 1) % n] = theta

    return angles


def is_clockwise(p0, p, p2):
    vec_to_p0 = [p0[0] - p[0], p0[1] - p[1]]
    vec_to_p2 = [p2[0] - p[0], p2[1] - p[1]]

    det = vec_to_p0[0] * vec_to_p2[1] - vec_to_p0[1] * vec_to_p2[0]

    return det > 0


def cross_product(vec_to_p0, vec_to_p2):
    return vec_to_p0[0] * vec_to_p2[1] - vec_to_p0[1] * vec_to_p2[0]


def clamp_index(x, a, b):
    if a <= x <= b:
        return x
    elif x > b:
        return a
    else:
        return b


def point_in_triangle(p, p0, p1, p2):
    # From https://stackoverflow.com/a/20861130
    s = (p0[0] - p2[0]) * (p[1] - p2[1]) - (p0[1] - p2[1]) * (p[0] - p2[0])
    t = (p1[0] - p0[0]) * (p[1] - p0[1]) - (p1[1] - p0[1]) * (p[0] - p0[0])

    if (s < 0) != (t < 0) and s != 0 and t != 0:
        return False

    d = (p2[0] - p1[0]) * (p[1] - p1[1]) - (p2[1] - p1[1]) * (p[0] - p1[0])

    return d == 0 or (d < 0) == (s + t <= 0)


def get_first_valid_triangle(points, poly_clockwise):
    n = len(points)
    indexs = list(range(n))

    angles = get_internal_angles(points, poly_clockwise)

    indexs_sorted = sorted(indexs, key=lambda index: angles[index])

    for i in indexs_sorted:
        i0 = clamp_index(i - 1, 0, n - 1)
        i2 = clamp_index(i + 1, 0, n - 1)

        p0 = points[i0]
        p1 = points[i]
        p2 = points[i2]

        if is_valid_triangle(points, p0, p1, p2):
            return i0, i, i2

    else:
        print("All triangles are invalid")
        i = indexs_sorted[0]
        i0 = clamp_index(i - 1, 0, n - 1)
        i2 = clamp_index(i + 1, 0, n - 1)

        return i0, i, i2


def is_valid_triangle(points, p0, p1, p2):
    triangle = [p0, p1, p2]
    for point in points:
        if point not in triangle:
            if point_in_triangle(point, p0, p1, p2):
                return False

    return True


def triangulate(points, poly_clockwise):
    points = merge_colinear_edges(points)
    n = len(points)

    triangles = []

    while n >= 3:

        i0, i, i2 = get_first_valid_triangle(points, poly_clockwise)

        p1 = points[i0]
        p2 = points[i]
        p3 = points[i2]

        triangles.append([p1, p2, p3])

        points.pop(i)

        points = merge_colinear_edges(points)

        n = len(points)

        if n < 3:
            break

    return triangles


