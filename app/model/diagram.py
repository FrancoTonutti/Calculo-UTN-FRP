from app.model.entity import Entity, register
from app.model import Bar, Node
from app.view import draw
import numpy as np
from app import app

from panda3d.core import GeomVertexArrayFormat, Geom, GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomTristrips,GeomNode



class Diagram(Entity):
    """
    bar: parent bar
    load_type: string  = "D", "L", "W", "S" etc.
    value: float
    """
    scale = 0.25

    """
    array = GeomVertexArrayFormat()
    array.addColumn("vertex", 3, Geom.NTFloat32, Geom.CPoint)
    array.addColumn("texcoord", 2, Geom.NTFloat32, Geom.CTexcoord)

    gformat = GeomVertexFormat()
    gformat.addArray(array)
    gformat = GeomVertexFormat.registerFormat(gformat)
    """
    gformat = GeomVertexFormat.get_v3c4()

    @staticmethod
    def create_from_object(obj):
        entity_id = obj.get("entity_id")
        values = obj.get("values")
        parent = app.model_reg.get_entity(obj.get("parent"))

        with Diagram(parent, values, entity_id) as ent:
            pass

    def __init__(self, parent, values, set_id=None):
        super().__init__(set_id)
        self.parent = parent
        self.values = values
        self.show = True

        self._scheme = dict()
        self.show_properties("show")
        #self.set_prop_name(show="Valor")
        self.bind_to_model("value", "angle")
        self.parent.add_child_model(self)


        self.create_model()

    def create_model(self):
        vdata = GeomVertexData('name', Diagram.gformat, Geom.UHStatic)
        vdata.setNumRows(len(self.values)*2)

        vertex = GeomVertexWriter(vdata, 'vertex')
        color = GeomVertexWriter(vdata, 'color')
        prim = GeomTristrips(Geom.UHStatic)

        i = 0
        for x, z in self.values:
            vertex.addData3(0, x, 0)
            color.addData4(0, 0, 1, 1)
            prim.addVertex(i)

            vertex.addData3(0, x, z/100)
            color.addData4(0, 0, 1, 1)
            prim.addVertex(i+1)

            print("Diagram point: {}; {}".format(x, z/100))

            i += 2

        print("longitude: {}".format(self.parent.longitude()))



        prim.closePrimitive()

        diagram_geom = Geom(vdata)
        diagram_geom.addPrimitive(prim)

        node = GeomNode('gnode')
        node.addGeom(diagram_geom)

        node.setTag('entity_type', self.__class__.__name__)
        node.setTag('entity_id', self.entity_id)

        model_parent = self.parent.geom[0]
        parent_scale = model_parent.getScale()

        nodePath = render.attachNewNode(node)
        nodePath.reparentTo(model_parent)
        nodePath.set_two_sided(True)
        nodePath.setLightOff()

        node_parent = self.parent.start.geom[0]



        L = self.parent.longitude()
        h = 1
        nodePath.setScale(h / parent_scale[2], 1 / parent_scale[1], 1)

        nodePath.wrtReparentTo(node_parent)
        """
        model = app.base.loader.loadModel("data/geom/plate")
        model.set_two_sided(True)
        model.setTag('entity_type', self.__class__.__name__)
        model.setTag('entity_id', self.entity_id)
        self.geom = [model]"""

        self.update_model()

    def update_model(self):
        pass

    def delete_model(self):
        pass
