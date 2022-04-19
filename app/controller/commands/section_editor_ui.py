from direct.gui import DirectGuiGlobals as DGG

from app.controller.console import command, execute
from app.controller.commands import render
from app import app
import numpy as np
from panda3d.core import LineSegs, NodePath

from app.model import Section
from app.model.section_type import SectionType
from app.view import draw
from app.view.interface import tools
from app.view.interface.color_scheme import *

from app.view.interface.tools import *

__tab_title__ = "Catálogo de secciones"

from app.view.simpleui import SimpleFrame


@command("section_editor")
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

        btn1 = new_button("Agregar Perfil", parent=btn_container,
                          command=self.create_section_type)
        self.btn2 = new_button("Agregar Sección", parent=btn_container,
                          command=self.create_section, margin=[10, 0, 0, 0])
        self.btn2['state'] = DGG.DISABLED

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

        self.col2 = SimpleFrame(
            parent=columns_container,
            sizeHint=[None, 1],
            size=[300, None],
            layout="BoxLayout",
            layoutDir="Y",
            alpha=0,
            margin=[20, 0, 0, 0],
        )

        self.col3 = SimpleFrame(
            parent=columns_container,
            sizeHint=[None, 1],
            size=[250, None],
            layout="BoxLayout",
            layoutDir="Y",
            alpha=1,
            margin=[20, 0, 0, 0],
        )

        self.col4 = SimpleFrame(
            parent=columns_container,
            sizeHint=[None, 1],
            size=[300, None],
            layout="BoxLayout",
            layoutDir="Y",
            alpha=0,
            margin=[20, 0, 0, 0],
        )

        #create_label("Materiales", col2, padding=[10, 0, 0, 5])

        '''self.material_name_input = SimpleEntry(
            label="Ingrese un nombre...",
            text_fg=scheme_rgba(COLOR_TEXT_LIGHT),
            orginH="center",
            position=[0, 0],
            text_scale=(12, 12),
            width=20,
            align="left",
            textCenterX=False,
            command=self.update_section_type_name,
            focusOutCommand=self.update_section_type_name,
            parent=self.col2,
            size=[None, 20],
            sizeHint=[0.50, None],
            frameColor="C_WHITE",
            alpha=0,
            initialText="Material",
            margin=[0,0,5,0]

        )'''

        self.label1 = tools.create_label("Propiedades del perfil", self.col2, alpha=0, padding=[0,0,0,10])

        self.label1 = tools.create_label("Propiedades de la sección", self.col4,
                                         alpha=0, padding=[0, 0, 0, 10])



        self.scroll2 = SimpleScrolledFrame(position=[0, 0],
                                        canvasSize=(0, 250, -200, 0),
                                        size=[None, None],
                                        sizeHint=[None, None],
                                        parent=self.col3,
                                        frameColor=scheme_rgba(
                                            COLOR_SEC_DARK),
                                        alpha=1,
                                        margin=[0, 0, 0, 0],
                                        layout="GridLayout",
                                        layoutDir="X",
                                        gridCols=2,
                                        gridRows=10)

        '''self.scroll3 = SimpleScrolledFrame(position=[0, 0],
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
                                           gridRows=10)'''

        self.prop_editor_section_type = PropEditor(self.col2, 300,
                                              self.update_section_type)

        self.prop_editor_section = PropEditor(self.col4, 300, self.update_section)

        self.material_list_btns = []


        col_rollover = draw.merge_color(COLOR_SEC_DARK, COLOR_MAIN_LIGHT, 0.8)
        self.default_colors = [COLOR_SEC_DARK, COLOR_MAIN_LIGHT, col_rollover,
                               COLOR_MAIN_LIGHT]
        self.selected_colors = [COLOR_MAIN_LIGHT, COLOR_MAIN_LIGHT,
                                col_rollover,
                                COLOR_MAIN_LIGHT]

        self.selected_section_type = None
        self.selected_section_type_btn = None

        self.submaterial_list_btns = []
        self.selected_section = None
        self.selected_section_btn = None

        self.fields = []

        self.update_list()

    def update_section(self):
        self.update_list()

    def update_section_type(self):
        self.update_list()

    def update_section_type_name(self, new_value):
        if new_value != "":
            tr = Transaction()
            tr.start("Update section type name")
            self.selected_section_type.name = new_value
            tr.commit()

            self.update_list()

    def update_list(self):
        self.btn2['state'] = DGG.DISABLED

        for btn in self.material_list_btns:
            btn.destroy()

        self.material_list_btns.clear()

        model_reg = app.model_reg
        entities = model_reg.find_entities("SectionType")

        entities = sorted(entities, key=lambda x: x.name)

        for group in entities:

            btn = new_button(group.name, parent=self.col1.canvas,
                             command=self.open_section_type, args=[group], colors=self.default_colors)

            del_btn = new_button("X", parent=self.col1.canvas,
                             command=self.open_section_type, args=[group], colors=self.default_colors)

            if self.selected_section_type is None:
                self.open_section_type(group, btn)
            elif self.selected_section_type is group:
                self.open_section_type(group, btn)


            btn["extraArgs"] = [group, btn]

            self.material_list_btns.append(btn)
            self.material_list_btns.append(del_btn)

            if self.selected_section_type.shape:
                self.btn2['state'] = DGG.NORMAL
            else:
                self.btn2['state'] = DGG.DISABLED



        execute("regen_ui")

    def delete_section_type(self, group: SectionType):

        group.delete()

        self.update_list()

    def open_section_type(self, group: SectionType, btn):
        print("open_group")

        if self.selected_section_type_btn:
            self.selected_section_type_btn["colorList"] = self.default_colors
            pass

        if self.selected_section_type is not group:
            self.selected_section = None

        self.selected_section_type_btn = btn
        self.selected_section_type_btn["colorList"] = self.selected_colors
        self.selected_section_type = group
        #self.material_name_input.enter_value(group.name)

        for btn in self.submaterial_list_btns:
            btn.destroy()

        self.submaterial_list_btns.clear()

        model_reg = app.model_reg
        entities = model_reg.find_entities("Section")

        entities = filter(lambda x: x.section_type == self.selected_section_type, entities)
        entities = sorted(entities, key=lambda x: x.name)
        print(entities)

        for subtype in entities:

            btn_name = subtype.name

            btn = new_button(btn_name, parent=self.scroll2.canvas,
                             command=self.open_section, args=[subtype], colors=self.default_colors)

            del_btn = new_button("X", parent=self.scroll2.canvas,
                                 command=self.delete_section, args=[subtype],
                                 colors=self.default_colors)

            if self.selected_section is None:
                self.open_section(subtype, btn)
            elif self.selected_section is group:
                self.open_section(subtype, btn)

            btn["extraArgs"] = [subtype, btn]
            self.submaterial_list_btns.append(btn)
            self.submaterial_list_btns.append(del_btn)

        self.entity_read_section_type()



        execute("regen_ui")

    def delete_section(self, material: Section):

        material.delete()

        self.update_list()

    def open_section(self, section, btn):

        if self.selected_section_btn:
            self.selected_section_btn["colorList"] = self.default_colors

        if self.selected_section is section:
            self.update_list()
        else:
            self.selected_section_btn = btn
            self.selected_section_btn["colorList"] = self.selected_colors
            self.selected_section = section
            #self.material_name_input.enter_value(material.name)

            self.entity_read_section()
            execute("regen_ui")

    def create_section_type(self):
        tr = Transaction()
        tr.start("Create MaterialGroup")
        mg = SectionType("Perfil")
        tr.commit()

        self.update_list()

    def create_section(self):
        tr = Transaction()
        tr.start("Create Material")
        mat = Section("10x10cm", self.selected_section_type, geometry={"d": 10})
        tr.commit()

        self.update_list()

    def entity_read_section_type(self):
        self.prop_editor_section_type.entity_read(self.selected_section_type)

        if self.selected_section_type.shape:
            self.btn2['state'] = DGG.NORMAL
        else:
            self.btn2['state'] = DGG.DISABLED

    def entity_read_section(self):
        self.prop_editor_section.entity_read(self.selected_section)

    def entity_read_section_old(self):

        for label, entry in self.fields:
            if hasattr(entry, "enter_value"):
                if entry['focus'] is True:
                    entry.defocus()

        for label, entry in self.fields:
            label.destroy()
            entry.destroy()

        self.fields.clear()
        print("entity_read_section")
        print(self.selected_section)
        print(list(self.selected_section.get_properties()))
        for prop in self.selected_section.get_properties():

            self.add_property(prop, self.selected_section.prop_name(prop), getattr(self.selected_section, prop))

        execute("regen_ui")