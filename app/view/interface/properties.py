from app import app
from .layout_controller import Layout
from direct.showbase.DirectObject import DirectObject
from app.controller.console import execute
from app.view.simpleui.simple_entry import SimpleEntry
from app.view.simpleui.simple_label import SimpleLabel
from app.view.simpleui.simple_scrolled_frame import SimpleScrolledFrame
from panda3d.core import TextNode
from panda3d.core import WindowProperties
from direct.gui.DirectScrolledFrame import *


def execute_console(cmd):
    print(cmd)


class PropertiesEditor(DirectObject):
    def __init__(self, layout: Layout):
        self.frame = layout.prop_frame
        self.container = layout.work_container

        self.entity = None
        self.fields = []

        self.accept("control-1", self.toogle_show)

        entry = SimpleLabel(
            text_fg=(0, 0, 0, 1),
            orginV="bottom",
            position=[0, 0],
            text_scale=(12, 12),
            text="Propiedadades",
            parent=self.frame,
            size=[None, 20],
            sizeHint=[0.50, None],
            frameColor="C_WHITE",
            alpha=0,
            align="left",
            textCenterX=False,
            padding=[15, 0, 0, 0]

        )

        self.frame_scrolled = SimpleScrolledFrame(

            position=[0, 0],
            canvasSize=(0, 250 - 16, -500, 0),
            parent=self.frame,
            layout="GridLayout",
            layoutDir="X",
            gridCols=2,
            gridRows=10,
            frameColor="C_CARROT",
            alpha=0
        )
        self.add_property("test", "testname2", 22)
        self.add_property("test", "testname2", 22)
        self.add_property("test", "testname2", 22)
        self.add_property("test", "testname2", 22)
        self.add_property("test", "testname2", 22)

        """canvas = self.frame_scrolled.getCanvas()


        entry = SimpleLabel(
            text_fg=(0, 0, 0, 1),
            orginV="bottom",
            position=[0, 0],
            text_scale=(12, 12),
            text="Prop",
            parent=self.frame_scrolled.getCanvas(),
            size=[None, 20],
            sizeHint=[0.50, None],
            frameColor="C_WHITE",
            align="left",
            textCenterX=False,
            padding=[15, 0, 0, 0]

        )
        entry = SimpleEntry(
            text_fg=(0, 0, 0, 1),
            orginH="center",
            position=[0, 0],
            text_scale=(12, 12),
            width=20,
            label="Ingrese un comando",
            command=execute_console,
            parent=self.frame_scrolled.getCanvas(),
            size=[None, 20],
            sizeHint=[0.50, None],
            frameColor="C_WHITE"

        )
        self.add_property("test", "testname", 22)

        frame_scrolled = SimpleScrolledFrame(

            position=[400, 400],
            canvasSize=(0, 150, -1000, 0),
            layout="BoxLayout",
            layoutDir="Y",
            gridCols=2,
            gridRows=2,
            sizeHint=[0.25, 0.25],
            frameColor="C_CARROT",
            alpha=100
        )

        label = SimpleLabel(
            text_fg=(1, 0, 0, 1),
            orginV="bottom",
            position=[0, 0],
            text_scale=(12, 12),
            text="Prop",
            parent=frame_scrolled.getCanvas(),
            size=[50, 50],
            frameColor="C_CARROT",
            align="left",
            textCenterX=False,
            padding=[15, 0, 0, 0]
        )"""
        """SimpleFrame(position=[0, 0],
                    size=[250, 500],
                    sizeHint=[None, 1],
                    frameColor="C_NEPHRITIS",
                    layout="BoxLayout",
                    layoutDir="Y",
                    gridCols=2,
                    gridRows=2)"""
        # myframe = DirectScrolledFrame(canvasSize=(-2, 2, -2, 2), frameSize=(-.5, .5, -.5, .5))
        # myframe.setPos(0, 0, 0)

    def add_property(self, prop: str, fieldname: str, value=0):
        print("add_property")
        print("prop", prop)
        print("fieldname", fieldname)
        print("value", value)

        label = SimpleLabel(
            text_fg=(0, 0, 0, 1),
            orginV="bottom",
            position=[0, 0],
            text_scale=(12, 12),
            text=fieldname,
            parent=self.frame_scrolled.getCanvas(),
            size=[None, 20],
            sizeHint=[0.50, None],
            frameColor="C_WHITE",
            align="left",
            textCenterX=False,
            padding=[15, 0, 0, 0]

        )
        entry = SimpleEntry(
            text_fg=(0, 0, 0, 1),
            orginH="center",
            position=[0, 0],
            text_scale=(12, 12),
            width=20,
            align="left",
            textCenterX=False,
            command=self.entity_set_prop,
            extraArgs=[prop],
            focusOutCommand=self.entity_set_prop,
            focusOutExtraArgs=[prop],
            parent=self.frame_scrolled.getCanvas(),
            size=[None, 20],
            sizeHint=[0.50, None],
            frameColor="C_WHITE",
            initialText=str(value)

        )
        self.fields.append([label, entry])

    def entity_set_prop(self, new_value: any, name: str):
        print("new_value", new_value)
        print("name", name)
        old_value = getattr(self.entity, name, None)

        if new_value != "" and isinstance(old_value, float):
            new_value = float(new_value)
        if type(old_value) is type(new_value):
            if self.entity is not None:
                print("atributo establecido")
                setattr(self.entity, name, new_value)
        else:
            if self.entity is not None:
                print("El tipo de asignación no corresponde: {},{}->{}".format(name, type(old_value), type(new_value)))

    def entity_read(self, entity=None):

        for label, entry in self.fields:
            if entry['focus'] is True:
                entry.defocus()

        if self.entity and self.entity.geom:
            self.entity.geom.setTextureOff(0)
            self.entity.geom.clearColorScale()

        if entity:
            self.entity = entity
            if self.entity.geom:
                self.entity.geom.setTextureOff(1)
                self.entity.geom.setColorScale(1, 0, 0, 0.7)

        for label, entry in self.fields:
            label.destroy()
            entry.destroy()

        self.fields.clear()

        for prop in self.entity.get_properties():
            self.add_property(prop, self.entity.prop_name(prop), getattr(self.entity, prop))

        execute("regen_ui")

    def toogle_show(self):
        if self.frame.is_hidden():
            self.frame["size"] = [250, 500]
            self.frame.show()
        else:
            self.frame.hide()
            self.frame["size"] = [0, 500]

        execute("regen_ui")
