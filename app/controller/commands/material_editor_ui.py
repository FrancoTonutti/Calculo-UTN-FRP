import pint
from direct.gui import DirectGuiGlobals as DGG

from app.controller.console import command, execute
from app.controller.commands import render
from app import app
import numpy as np
from panda3d.core import LineSegs, NodePath
from app.view import draw
from app.view.interface.color_scheme import *

from app.view.interface.tools import *

__tab_title__ = "Editor de materiales"

from app.view.simpleui import SimpleFrame
from app.model import MaterialGroup, Material


@command("material_editor")
def section_editor():
    tab_manager = app.main_ui.tab_manager

    index = 0
    for tab in tab_manager.tabs:

        if tab.title == __tab_title__:
            tab_manager.set_active_tab(index)
            return None
        index += 1

    new_tab = tab_manager.create_new_tab(__tab_title__)
    frame = new_tab.frame
    frame["frameColor"] = scheme_rgba(COLOR_SEC_LIGHT)
    frame["layoutDir"] = "Y"

    UI(frame)

class UI:
    def __init__(self, frame):

        create_label("Materiales", frame, padding=[10, 0, 0, 0], margin=[0, 0, 0, 10])
        content  = SimpleFrame(
            parent=frame,
            sizeHint=[1, 1],
            layout="BoxLayout",
            layoutDir="Y",
            margin=[10, 10, 35, 0],
            alpha=0
        )

        btn_container = SimpleFrame(
            parent=content,
            sizeHint=[1, None],
            size=[None, 25],
            layout="BoxLayout",
            layoutDir="X",
            alpha=0,
            margin=[0,0,10,10]
        )
        columns_container = SimpleFrame(
            parent=content,
            sizeHint=[None, None],
            size=[None, None],
            layout="BoxLayout",
            layoutDir="X",
            alpha=0,
            margin=[0, 0, 10, 10]
        )

        btn1 = new_button("Agregar Material", parent=btn_container,
                          command=self.create_material_group)
        btn2 = new_button("Agregar Subtipo", parent=btn_container,
                          command=self.create_material_subtype, margin=[10, 0, 0, 0])

        #btn2['state'] = DGG.DISABLED

        self.col1 = SimpleScrolledFrame(position=[0, 0],
                                        canvasSize=(0, 250, -200, 0),
                                        size=[250, None],
                                        sizeHint=[None, 1],
                                        parent=columns_container,
                                        frameColor=scheme_rgba(
                                            COLOR_SEC_DARK),
                                        alpha=1,
                                        padding=[0, 1, 0, 0],
                                        layout="GridLayout",
                                        layoutDir="X",
                                        gridCols=2,
                                        gridRows=10)

        col2 = SimpleFrame(
            parent=columns_container,
            sizeHint=[None, 1],
            size=[250, None],
            layout="BoxLayout",
            layoutDir="Y",
            alpha=0,
            margin=[20, 0, 0, 0],
        )

        col3 = SimpleFrame(
            parent=columns_container,
            sizeHint=[None, 1],
            size=[300, None],
            layout="BoxLayout",
            layoutDir="Y",
            alpha=1,
            margin=[20, 0, 0, 0],
        )

        #create_label("Materiales", col2, padding=[10, 0, 0, 5])

        self.material_name_input = SimpleEntry(
            label="Ingrese un nombre...",
            text_fg=scheme_rgba(COLOR_TEXT_LIGHT),
            orginH="center",
            position=[0, 0],
            text_scale=(12, 12),
            width=20,
            align="left",
            textCenterX=False,
            command=self.update_material_name,
            focusOutCommand=self.update_material_name,
            parent=col2,
            size=[None, 20],
            sizeHint=[0.50, None],
            frameColor="C_WHITE",
            alpha=0,
            initialText="Material",
            margin=[0,0,5,0]

        )


        self.scroll2 = SimpleScrolledFrame(position=[0, 0],
                                        canvasSize=(0, 250, -200, 0),
                                        size=[None, None],
                                        sizeHint=[None, None],
                                        parent=col2,
                                        frameColor=scheme_rgba(
                                            COLOR_SEC_DARK),
                                        alpha=1,
                                        margin=[0, 0, 0, 0],
                                        layout="GridLayout",
                                        layoutDir="X",
                                        gridCols=2,
                                        gridRows=10)

        self.scroll3 = SimpleScrolledFrame(position=[0, 0],
                                           canvasSize=(0, 300, -200, 0),
                                           size=[None, None],
                                           sizeHint=[None, None],
                                           parent=col3,
                                           frameColor=scheme_rgba(
                                               COLOR_SEC_DARK),
                                           alpha=1,
                                           margin=[0, 0, 0, 0],
                                           layout="GridLayout",
                                           layoutDir="X",
                                           gridCols=2,
                                           gridRows=10)

        self.material_list_btns = []


        col_rollover = draw.merge_color(COLOR_SEC_DARK, COLOR_MAIN_LIGHT, 0.8)
        self.default_colors = [COLOR_SEC_DARK, COLOR_MAIN_LIGHT, col_rollover,
                               COLOR_MAIN_LIGHT]
        self.selected_colors = [COLOR_MAIN_LIGHT, COLOR_MAIN_LIGHT,
                                col_rollover,
                                COLOR_MAIN_LIGHT]

        self.selected_group = None
        self.selected_group_btn = None

        self.submaterial_list_btns = []
        self.selected_subtype = None
        self.selected_subtype_btn = None

        self.fields = []

        self.update_list()

    def update_material_name(self, new_value):
        if new_value != "":
            self.selected_group.name = new_value

            self.update_list()

    def update_list(self):

        for btn in self.material_list_btns:
            btn.destroy()

        self.material_list_btns.clear()

        model_reg = app.model_reg
        entities = model_reg.find_entities("MaterialGroup")

        entities = sorted(entities, key=lambda x: x.name)

        for group in entities:

            btn = new_button(group.name, parent=self.col1.canvas,
                             command=self.open_group, args=[group], colors=self.default_colors)

            del_btn = new_button("X", parent=self.col1.canvas,
                             command=self.delete_group, args=[group], colors=self.default_colors)

            if self.selected_group is None:
                self.open_group(group, btn)
            elif self.selected_group is group:
                self.open_group(group, btn)


            btn["extraArgs"] = [group, btn]

            self.material_list_btns.append(btn)
            self.material_list_btns.append(del_btn)



        execute("regen_ui")

    def delete_group(self, group: MaterialGroup):

        group.delete()

        self.update_list()

    def open_group(self, group: MaterialGroup, btn):
        print("open_group")

        if self.selected_group_btn:
            self.selected_group_btn["colorList"] = self.default_colors
            pass

        if self.selected_group is not group:
            self.selected_subtype = None

        self.selected_group_btn = btn
        self.selected_group_btn["colorList"] = self.selected_colors
        self.selected_group = group
        self.material_name_input.enter_value(group.name)

        for btn in self.submaterial_list_btns:
            btn.destroy()

        self.submaterial_list_btns.clear()

        model_reg = app.model_reg
        entities = model_reg.find_entities("Material")
        print(entities)
        for ent in entities:
            print(ent.material_group is self.selected_group)
            print(type(ent.material_group))
            print(type(self.selected_group))

        entities = filter(lambda x: x.material_group == self.selected_group, entities)
        entities = sorted(entities, key=lambda x: x.name)
        print(entities)

        for subtype in entities:

            btn_name = subtype.name

            if subtype.is_default_material:
                btn_name += " [Default]"

            btn = new_button(btn_name, parent=self.scroll2.canvas,
                             command=self.open_subtype, args=[subtype], colors=self.default_colors)

            del_btn = new_button("X", parent=self.scroll2.canvas,
                                 command=self.delete_subtype, args=[subtype],
                                 colors=self.default_colors)

            if self.selected_subtype is None:
                self.open_subtype(subtype, btn)
            elif self.selected_subtype is group:
                self.open_subtype(subtype, btn)


            btn["extraArgs"] = [subtype, btn]
            self.submaterial_list_btns.append(btn)
            self.submaterial_list_btns.append(del_btn)

        execute("regen_ui")

    def delete_subtype(self, material: Material):

        material.delete()

        self.update_list()

    def open_subtype(self, material, btn):

        if self.selected_subtype_btn:
            self.selected_subtype_btn["colorList"] = self.default_colors

        if self.selected_subtype is material and not material.is_default_material:
            material.set_default_material()
            self.update_list()
        else:
            self.selected_subtype_btn = btn
            self.selected_subtype_btn["colorList"] = self.selected_colors
            self.selected_subtype = material
            #self.material_name_input.enter_value(material.name)

            self.entity_read()
            execute("regen_ui")

    def create_material_group(self):
        tr = Transaction()
        tr.start("Create MaterialGroup")
        mg = MaterialGroup("Material")
        tr.commit()

        self.update_list()

    def create_material_subtype(self):
        tr = Transaction()
        tr.start("Create Material")
        mat = Material("Subtipo", self.selected_group)
        tr.commit()

        self.update_list()

    def add_property(self, prop: str, fieldname: str, value=0):

        label = SimpleLabel(
            text_fg=scheme_rgba(COLOR_TEXT_LIGHT),
            orginV="bottom",
            position=[0, 0],
            text_scale=(12, 12),
            text=fieldname,
            parent=self.scroll3.getCanvas(),
            size=[None, 20],
            sizeHint=[0.50, None],
            frameColor=scheme_rgba(COLOR_MAIN_LIGHT),
            alpha=1,
            align="left",
            textCenterX=False,
            padding=[5, 0, 0, 0]

        )
        if isinstance(value, bool):
            entry = SimpleCheckBox(
                position=[0, 0],
                size=[None, 20],
                sizeHint=[0.50, None],
                parent=self.scroll3.getCanvas(),
                command=self.entity_set_prop,
                extraArgs=[prop],
                value=value,
                frameColor="C_WHITE",
                maxSize=16
            )
        else:
            if self.selected_subtype.is_read_only(prop):
                entry = SimpleLabel(
                    orginH="center",
                    orginV="bottom",
                    position=[0, 0],
                    text_scale=(12, 12),
                    text=str(value),
                    parent=self.scroll3.getCanvas(),
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
                    text_fg=scheme_rgba(COLOR_TEXT_LIGHT),
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
                    parent=self.scroll3.getCanvas(),
                    size=[None, 20],
                    sizeHint=[0.50, None],
                    frameColor="C_WHITE",
                    initialText=initial_value,
                    alpha=0,
                    padding=[10, 0, 0, 0],
                    suffix=value_unit

                )
        self.fields.append([label, entry])

    def entity_set_prop(self, new_value: any, name: str):
        old_value = getattr(self.selected_subtype, name, None)

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
            if self.selected_subtype is not None:
                print("atributo establecido {}: {}".format(name, new_value))
                setattr(self.selected_subtype, name, new_value)
                print("verif {}: {}".format(name, getattr(self.selected_subtype, name, "undefined")))

        else:
            if self.selected_subtype is not None:
                print("El tipo de asignación no corresponde: {},{}->{}".format(name, type(old_value), type(new_value)))

        self.update_list()

    def entity_read(self):

        for label, entry in self.fields:
            if hasattr(entry, "enter_value"):
                if entry['focus'] is True:
                    entry.defocus()

        for label, entry in self.fields:
            label.destroy()
            entry.destroy()

        self.fields.clear()
        print("entity_read")
        print(self.selected_subtype)
        print(list(self.selected_subtype.get_properties()))
        for prop in self.selected_subtype.get_properties():

            self.add_property(prop, self.selected_subtype.prop_name(prop), getattr(self.selected_subtype, prop))

        execute("regen_ui")