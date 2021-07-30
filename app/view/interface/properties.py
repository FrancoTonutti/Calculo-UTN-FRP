from app import app
from .layout_controller import Layout
from direct.showbase.DirectObject import DirectObject
from app.controller.console import execute
from app.view.simpleui.simple_entry import SimpleEntry
from app.view.simpleui.simple_label import SimpleLabel
from app.view.simpleui.simple_scrolled_frame import SimpleScrolledFrame
from app.view.simpleui import SimpleCheckBox

from panda3d.core import TextNode
from panda3d.core import WindowProperties
from direct.gui.DirectScrolledFrame import *


def execute_console(cmd):
    print(cmd)

COLOR_TEXT_LIGHT = (238/255, 238/255, 238/255, 1)
COLOR_MAIN_DARK = (35/255, 35/255, 35/255, 255/255)
COLOR_MAIN_LIGHT = (66/255, 66/255, 66/255, 1)
COLOR_SEC_DARK = (43, 43, 43)
COLOR_SEC_LIGHT = (52, 52, 52)


class PropertiesEditor(DirectObject):
    def __init__(self, layout: Layout):
        self.frame = layout.prop_frame
        self.container = layout.work_container

        self.entity = None
        self.fields = []

        self.accept("control-1", self.toogle_show)

        label = SimpleLabel(
            text_fg=COLOR_TEXT_LIGHT,
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


    def add_property(self, prop: str, fieldname: str, value=0):


        label = SimpleLabel(
            text_fg=COLOR_TEXT_LIGHT,
            orginV="bottom",
            position=[0, 0],
            text_scale=(12, 12),
            text=fieldname,
            parent=self.frame_scrolled.getCanvas(),
            size=[None, 20],
            sizeHint=[0.50, None],
            frameColor="C_WHITE",
            alpha=0,
            align="left",
            textCenterX=False,
            padding=[15, 0, 0, 0]

        )
        if isinstance(value, bool):
            entry = SimpleCheckBox(
                position=[0, 0],
                size=[None, 20],
                sizeHint=[0.50, None],
                parent=self.frame_scrolled.getCanvas(),
                command=self.entity_set_prop,
                extraArgs=[prop],
                value=value,
                frameColor="C_WHITE",
                maxSize=16
            )
        else:
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
        old_value = getattr(self.entity, name, None)



        if new_value != "" and isinstance(old_value, float):
            new_value = float(new_value)

        if isinstance(old_value, bool):
            if new_value == "True":
                new_value = True
            elif new_value == "False":
                new_value = False

        if old_value == new_value:
            return None

        if type(old_value) is type(new_value):
            if self.entity is not None:
                print("atributo establecido {}: {}".format(name,new_value))
                setattr(self.entity, name, new_value)
                print("verif {}: {}".format(name, getattr(self.entity, name, "undefined")))
        else:
            if self.entity is not None:
                print("El tipo de asignación no corresponde: {},{}->{}".format(name, type(old_value), type(new_value)))

    def entity_read(self, entity=None):
        if entity != self.entity:
            for label, entry in self.fields:
                if entry['focus'] is True:
                    entry.defocus()

            if self.entity:
                self.entity.is_selected = False
                if self.entity.geom:
                    for geom in self.entity.geom:
                        if geom:
                            geom.setTextureOff(0)

                            geom.clearColorScale()
                            if "render/lines" in str(geom):
                                col = geom.getPythonTag('defcolor')
                                if col is not None:
                                    geom.setColorScale(col)

            if entity:
                self.entity = entity
                if self.entity:
                    self.entity.is_selected = True
                    if self.entity.geom is not None:
                        for geom in self.entity.geom:
                            if geom:
                                if "render/lines" in str(geom):
                                    print(geom)
                                    #geom.setColor(1, 0, 0, 0)
                                    geom.setColorScale(1, 0, 0, 1)
                                    #geom.node().setColor(1, 0, 0, 1)
                                else:
                                    geom.setTextureOff(1)
                                    geom.setColorScale(1, 0, 0, 0.7)

                                print("!!!!!!!!!!!!!!!!geom", geom, len(self.entity.geom))

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
