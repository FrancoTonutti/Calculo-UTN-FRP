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

        for attr, value in geometry.items():
            if isinstance(value, str):
                setattr(self, attr, app.ureg(value))
            else:
                setattr(self, attr, value*app.ureg("cm"))

    def __str__(self):
        return self.name

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

    def get_contour_points(self):

        geometry = {}

        for attr in self.section_type.shape.params:
            value = getattr(self, attr)
            geometry.update({attr: value})

        return self.section_type.get_contour_points(**geometry)

    def get_geom(self):
        points = self.get_contour_points()

        vdata = GeomVertexData('name', Section.gformat, Geom.UHStatic)
        n = len(points)
        total_vertex = n * 2 + (n - 1)*4

        vdata.setNumRows(total_vertex)

        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color = GeomVertexWriter(vdata, 'color')
        #prim = GeomTristrips(Geom.UHStatic)
        prim = GeomTriangles(Geom.UHStatic)


        triangles = triangulate(points.copy())
        print("-------------------------")
        print(points)
        print(triangles)
        print("-------------------------")

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

        '''i = 0
        for x, z in points:
            vertex.addData3(x, 0.25, z)
            normal.addData3(0, -1, 0)
            color.addData4(1, 125 / 255, 0, 1)
            prim.addVertex(i)
            i += 1

        prim.closePrimitive()

        for x, z in points:
            vertex.addData3(x, 0.75, z)
            normal.addData3(0, 1, 0)
            color.addData4(1, 125 / 255, 0, 1)
            prim.addVertex(i)
            i += 1

        prim.closePrimitive()'''

        '''i = 0
        for x, z in points:
            prim.addVertex(i)
            prim.addVertex(i + len(points))
            i += 1

        prim.closePrimitive()'''


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

        '''i = 0
        for x, z in points:

            vertex.addData3(x, 0, z)
            color.addData4(1, 125 / 255, 0, 1)
            prim.addVertex(i)
            i += 1

            vertex.addData3(x, 1, z)
            color.addData4(1, 125 / 255, 0, 1)
            prim.addVertex(i)

            i += 1'''



        section_geom = Geom(vdata)
        section_geom.addPrimitive(prim)

        node = GeomNode('gnode')
        node.addGeom(section_geom)

        nodePath = render.attachNewNode(node)
        #nodePath.set_two_sided(True)

        return nodePath


############

def angle(p1, p2, p3):
    v1 = [p2[0] - p1[0], p2[1] - p1[1]]
    v2 = [p2[0] - p3[0], p2[1] - p3[1]]

    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    dot_product = np.dot(v1, v2)
    angle = np.arccos(dot_product / (norm1 * norm2))

    return angle


def is_clockwise(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    det = (x2 - x1) * (x3 - x1) - (x3 - x1) * (y2 - y1)

    return det < 0


def clamp_index(x, a, b):

    if a <= x <= b:
        return x
    elif x > b:
        return a
    else:
        return b


def triangulate(points):
    n = len(points)
    m = n

    max_x = points[0][0]
    j = 0

    for i in range(n):
        if points[i][0] > max_x:
            max_x = points[i][0]
            j = i

    i0 = clamp_index(j-1, 0, n-1)
    i2 = clamp_index(j+1, 0, n-1)

    p1 = points[i0]
    p2 = points[j]
    p3 = points[i2]

    poly_clockwise = is_clockwise(p1, p2, p3)

    angles = [0]*n

    for i in range(n):
        p1 = points[i]
        p2 = points[(i+1) % n]
        p3 = points[(i+2) % n]

        theta = angle(p1, p2, p3)
        triangle_clockwise = is_clockwise(p1, p2, p3)

        if triangle_clockwise != poly_clockwise:
            theta = 2*np.pi - theta

        angles[(i+1) % n] = theta

    triangles = []

    for i in range(m-2):
        min_ang = min(angles)
        min_ang_index = angles.index(min_ang)

        i0 = clamp_index(min_ang_index-1, 0, n-1)
        i2 = clamp_index(min_ang_index+1, 0, n - 1)

        p1 = points[i0]
        p2 = points[min_ang_index]
        p3 = points[i2]

        triangles.append([p1, p2, p3])

        if p2 == p3:
            raise Exception(str([i0, min_ang_index, i2]))

        p1 = points[clamp_index(i0-1, 0, n-1)]
        p2 = points[min_ang_index]
        p3 = points[i2]

        theta = angle(p1, p2, p3)
        triangle_clockwise = is_clockwise(p1, p2, p3)

        if triangle_clockwise != poly_clockwise:
            theta = 2*np.pi - theta

        angles[i0] = theta

        p1 = points[i0]
        p2 = points[i2]
        p3 = points[clamp_index(i2+1, 0, n-1)]

        triangle_clockwise = is_clockwise(p1, p2, p3)

        if triangle_clockwise != poly_clockwise:
            theta = 2 * np.pi - theta

        angles[i2] = theta

        points.pop(min_ang_index)
        angles.pop(min_ang_index)

        n -= 1

    return triangles


