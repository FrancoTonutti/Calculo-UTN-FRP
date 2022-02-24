from enum import Enum

import pint

from app import app
from .layout_controller import Layout
from direct.showbase.DirectObject import DirectObject
from app.controller.console import execute
from app.view.simpleui.simple_entry import SimpleEntry
from app.view.simpleui.simple_label import SimpleLabel
from app.view.simpleui.simple_scrolled_frame import SimpleScrolledFrame
from app.view.simpleui import SimpleCheckBox, SimpleFrame

from panda3d.core import TextNode
from panda3d.core import WindowProperties
from direct.gui.DirectScrolledFrame import *

from .tools import create_label, PropEditor
from ...model import View
from ...model.transaction import Transaction

from app.view.interface.color_scheme import *

def execute_console(cmd):
    print(cmd)


class PropEditorModes(Enum):
    EDIT = 0
    CREATE = 1


class PropertiesEditor(DirectObject):
    def __init__(self, layout: Layout):
        self.frame = layout.prop_frame
        self.container = layout.work_container

        self.entity = None
        self.fields = []
        self.selection = []
        self.selection_limit = 1

        #self.accept("control-1", self.toogle_show)
        self.frame = layout.prop_frame
        label = SimpleLabel(
            text_fg=scheme_rgba(COLOR_TEXT_LIGHT),
            orginV="bottom",
            position=[0, 0],
            fontSize=12,
            text="Propiedadades",
            parent=self.frame,
            size=[None, 20],
            sizeHint=[0.50, None],
            frameColor="C_WHITE",
            alpha=0,
            align="left",
            textCenterX=False,
            margin=[10, 0, 0, 0]

        )




        self.name_label = SimpleLabel(
            text_fg=scheme_rgba(COLOR_TEXT_LIGHT),
            orginV="bottom",
            position=[0, 0],
            fontSize=14,
            text="Barra",
            parent=self.frame,
            size=[None, 20],
            sizeHint=[1, None],
            frameColor="C_WHITE",
            alpha=0,
            align="left",
            textCenterX=False,
            margin=[30, 0, 25, 25]

        )

        self.mode_status_bar = SimpleFrame(
            parent=self.frame,
            size=[None, 4],
            sizeHint=[1, None],
            frameColor=scheme_rgba(COLOR_MAIN_LIGHT)
        )

        self.prop_editor = PropEditor(self.frame, 250, self.update)
        self.mode = PropEditorModes.EDIT

    def set_mode(self, mode):
        self.mode = mode

        if self.mode is PropEditorModes.EDIT:
            self.mode_status_bar["frameColor"] = scheme_rgba(COLOR_MAIN_LIGHT)
        elif self.mode is PropEditorModes.CREATE:
            self.mode_status_bar["frameColor"] = scheme_rgba(COLOR_HIGHLIGHT)

    def deselect_all(self):
        for entity in self.selection:
            self.deselect(entity)

        entities = app.model_reg.get("View", {})

        if entities is None or len(entities) is 0:
            tr = Transaction("Create")
            tr.start("Create View")
            #View()
            tr.commit()

        entities = app.model_reg.get("View")
        entity = list(entities.values())[0]
        prop_editor = app.main_ui.prop_editor

        self.add_to_selection(entity)

    def add_to_selection(self, entity):
        print("add_to_selection", entity)

        if entity not in self.selection:

            if len(self.selection) < self.selection_limit:
                self.selection.append(entity)
            else:
                #pop = self.selection.pop(0)
                self.deselect(self.selection[0])
                self.selection.append(entity)

            if len(self.selection) is 1 and self.mode is PropEditorModes.EDIT:
                print(self.mode, PropEditorModes.EDIT)
                self.entity_read(self.selection[0])
            else:
                self.update_selection()

    def deselect(self, entity):
        if entity:
            tr = Transaction()
            tr.start("Deselect entity")
            entity.is_selected = False
            tr.commit()

        if entity in self.selection:
            self.selection.remove(entity)

        if entity and entity.geom:
            for geom in entity.geom:
                if geom:
                    geom.setTextureOff(0)

                    geom.clearColorScale()
                    if "render/lines" in str(geom):
                        col = geom.getPythonTag('defcolor')
                        if col is not None:
                            geom.setColorScale(col)

    def update_selection(self):
        for entity in self.selection:
            tr = Transaction()
            tr.start("Select entity")
            entity.is_selected = True
            tr.commit()
            if entity.geom is not None:
                for geom in entity.geom:
                    if geom:
                        if "render/lines" in str(geom):
                            # print(geom)
                            # geom.setColor(1, 0, 0, 0)
                            geom.setColorScale(1, 0, 0, 1)
                            # geom.node().setColor(1, 0, 0, 1)
                        else:
                            geom.setTextureOff(1)
                            geom.setColorScale(1, 0, 0, 0.7)


    def update(self):
        pass

    def entity_read(self, entity=None, update=False, mode="edit"):

        if entity:
            self.name_label["text"] = entity.category_name
        else:
            self.name_label["text"] = ""
        if entity != self.prop_editor.entity or update:

            if self.entity:
                tr = Transaction()
                tr.start("Deselect entity")
                self.entity.is_selected = False
                tr.commit()
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
                    tr = Transaction()
                    tr.start("Select entity")
                    self.entity.is_selected = True
                    tr.commit()
                    if self.entity.geom is not None:
                        for geom in self.entity.geom:
                            if geom:
                                if "render/lines" in str(geom):
                                    #print(geom)
                                    #geom.setColor(1, 0, 0, 0)
                                    print(geom)
                                    geom.setColorScale(1, 0, 0, 1)

                                    #geom.node().setColor(1, 0, 0, 1)
                                else:
                                    geom.setTextureOff(1)
                                    geom.setColorScale(1, 0, 0, 0.7)

                                #print("!!!!!!!!!!!!!!!!geom", geom, len(self.entity.geom))

        self.prop_editor.entity_read(entity)

class PropertiesEditorOld(DirectObject):
    def __init__(self, layout: Layout):
        self.frame = layout.prop_frame
        self.container = layout.work_container

        self.entity = None
        self.fields = []

        self.accept("control-1", self.toogle_show)

        label = SimpleLabel(
            text_fg=scheme_rgba(COLOR_TEXT_LIGHT),
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
            margin=[10, 0, 0, 0]

        )

        self.name_box = SimpleFrame(
            parent=self.frame,
            size=[None, 75],
            sizeHint=[1, None]
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
            text_fg=scheme_rgba(COLOR_TEXT_LIGHT),
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
            padding=[5, 0, 0, 0]

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
            if self.entity.is_read_only(prop):
                entry = SimpleLabel(
                    orginH="center",
                    orginV="bottom",
                    position=[0, 0],
                    text_scale=(12, 12),
                    text=str(value),
                    parent=self.frame_scrolled.getCanvas(),
                    size=[None, 20],
                    sizeHint=[0.50, None],
                    frameColor="C_WHITE",
                    alpha=1,
                    align="left",
                    textCenterX=False,
                    padding=[5, 0, 0, 0]

                )

            else:
                initial_value = str(value)
                value_unit = ""
                if isinstance(value, pint.quantity.Quantity):
                    initial_value = str(value.magnitude)
                    value_unit = " [{}]".format(format(value.u, '~'))

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
                    initialText=initial_value,
                    suffix=value_unit

                )
        self.fields.append([label, entry])

    def entity_set_prop(self, new_value: any, name: str):
        old_value = getattr(self.entity, name, None)

        if isinstance(old_value, bool):

            if new_value == "True":
                new_value = True
            elif new_value == "False":
                new_value = False
        elif new_value != "" and isinstance(old_value, float):
            new_value = float(new_value)

        elif new_value != "" and isinstance(old_value, int):
            new_value = int(new_value)

        elif new_value != "" and isinstance(old_value, pint.quantity.Quantity):
            new_value = float(new_value) * app.ureg(str(old_value.units))

        if old_value == new_value:
            return None

        if type(old_value) is type(new_value):
            if self.entity is not None:
                print("atributo establecido {}: {}".format(name,new_value))

                tr = Transaction()
                tr.start("Edit propery")
                setattr(self.entity, name, new_value)
                tr.commit()

                print("verif {}: {}".format(name, getattr(self.entity, name, "undefined")))
        else:
            if self.entity is not None:
                print("El tipo de asignación no corresponde: {},{}->{}".format(name, type(old_value), type(new_value)))

    def entity_read(self, entity=None, update=False):
        if entity != self.entity or update:
            for label, entry in self.fields:
                if hasattr(entry, "enter_value"):
                    if entry['focus'] is True:
                        entry.defocus()

            if self.entity:
                tr = Transaction()
                tr.start("Deselect entity")
                self.entity.is_selected = False
                tr.commit()
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
                    tr = Transaction()
                    tr.start("Select entity")
                    self.entity.is_selected = True
                    tr.commit()
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
