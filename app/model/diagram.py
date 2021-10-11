from app.controller.console import execute
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
        combination = app.model_reg.get_entity(obj.get("combination"))
        parent = app.model_reg.get_entity(obj.get("parent"))

        print("VALUES!!!",type(values))
        print("VALUES[0]!!!", type(values[0]))

        Diagram(parent, combination, values, entity_id)

    def __init__(self, parent, combination, diagram_type, values, set_id=None):
        super().__init__(set_id)
        self.parent: Bar = parent
        self.values = values
        self.show = True

        self._scheme = dict()
        self.show_properties("scale")
        self.set_prop_name(scale="Escala")
        self.parent.add_child_model(self)

        self.combination = combination
        self.diagram_type = diagram_type

        self.show_properties("comb_name", "equation")
        self.set_prop_name(comb_name="Combinación", equation="Ecuación")
        self.set_read_only("comb_name", "equation")

        if self.values is not None:

            self.max = self.values[0][1]
            self.min = self.values[0][1]
            for pos, value in self.values:
                self.max = max(value, self.max)
                self.min = min(value, self.min)

            self.max = round(self.max, 2)
            self.min = round(self.min, 2)

            self.percent0 = round(self.values[0][1], 2)
            percent0_pos = round(self.values[0][0], 2)
            self.percent25 = round(self.values[4][1], 2)
            percent25_pos = round(self.values[4][0], 2)
            self.percent50 = round(self.values[7][1], 2)
            percent50_pos = round(self.values[7][0], 2)
            self.percent75 = round(self.values[10][1], 2)
            percent75_pos = round(self.values[10][0], 2)
            self.percent100 = round(self.values[14][1], 2)
            percent100_pos = round(self.values[14][0], 2)

            self.show_properties("max", "min", "percent0", "percent0", "percent25", "percent50", "percent75", "percent100")
            self.set_read_only("max", "min", "percent0", "percent0", "percent25", "percent50", "percent75", "percent100")

            self.set_prop_name(max="Máximo", min="Mínimo")
            self.set_prop_name(percent0="0% ({} [m])".format(percent0_pos))
            self.set_prop_name(percent25="25% ({} [m])".format(percent25_pos))
            self.set_prop_name(percent50="50% ({} [m])".format(percent50_pos))
            self.set_prop_name(percent75="75% ({} [m])".format(percent75_pos))
            self.set_prop_name(percent100="100% ({} [m])".format(percent100_pos))



        self.create_model()

    def is_visible(self):
        return (app.show_combination == self.combination.index)\
               and ((app.show_moment and self.diagram_type == "M")
                    or (app.show_shear and self.diagram_type == "S")
                    or (app.show_normal and self.diagram_type == "N"))

    @property
    def equation(self):
        return self.combination.equation

    @property
    def comb_name(self):
        return self.combination.name

    @property
    def scale(self):
        return round(app.diagram_scale, 2)

    @scale.setter
    def scale(self, value):
        app.diagram_scale = value

        execute("regen")


    def delete(self):
        print("delete override by diagram")
        self.parent.remove_child_model(self)

        return super(Diagram, self).delete()

    def create_model(self):
        if not self.is_visible():
            print("hide combination", app.show_combination, self.combination.index)
            print("hide combination", type(app.show_combination),
                  type(self.combination.index))
            return None

        vdata = GeomVertexData('name', Diagram.gformat, Geom.UHStatic)
        vdata.setNumRows(len(self.values)*2)

        vertex = GeomVertexWriter(vdata, 'vertex')
        color = GeomVertexWriter(vdata, 'color')
        prim = GeomTristrips(Geom.UHStatic)

        i = 0
        for x, z in self.values:
            vertex.addData3(0, x, 0)
            #color.addData4(0, 0, 1, 1)
            if self.diagram_type == "M":
                color.addData4(1, 125/255, 0, 1)
            elif self.diagram_type == "S":
                color.addData4(1, 71/255, 0, 1)
            else:
                color.addData4(193/255, 0, 1, 1)
            prim.addVertex(i)

            vertex.addData3(0, x, -z/100)
            #color.addData4(0, 0, 1, 1)
            if self.diagram_type == "M":
                color.addData4(1, 125/255, 0, 1)
            elif self.diagram_type == "S":
                color.addData4(1, 71/255, 0, 1)
            else:
                color.addData4(193/255, 0, 1, 1)

            prim.addVertex(i+1)


            i += 2




        prim.closePrimitive()

        diagram_geom = Geom(vdata)
        diagram_geom.addPrimitive(prim)

        node = GeomNode('gnode')
        node.addGeom(diagram_geom)


        model_parent = self.parent.geom[0]
        parent_scale = model_parent.getScale()

        nodePath = render.attachNewNode(node)
        nodePath.reparentTo(model_parent)
        nodePath.set_two_sided(True)
        nodePath.setLightOff()

        nodePath.setTag('entity_type', self.__class__.__name__)
        nodePath.setTag('entity_id', self.entity_id)

        self.geom = [nodePath]

        node_parent = self.parent.start.geom[0]

        L = self.parent.longitude()
        h = 1
        nodePath.setScale(1 / parent_scale[0], 1 / parent_scale[1], self.scale/parent_scale[2])

        nodePath.wrtReparentTo(node_parent)
        """
        model = app.base.loader.loadModel("data/geom/plate")
        model.set_two_sided(True)
        model.setTag('entity_type', self.__class__.__name__)
        model.setTag('entity_id', self.entity_id)
        self.geom = [model]"""



    def update_model(self):
        self.delete_model()
        if self.is_visible():
            self.create_model()


    def delete_model(self):
        print("delete_model override by diagram")
        if self.geom:
            num = len(self.geom)
        else:
            num = 0
        print("delete models {}".format(num))
        if self.geom:
            for geomnode in self.geom:  # type: GeomNode
                if geomnode:
                    print("delete model", geomnode)

                    geomnode.removeNode()

