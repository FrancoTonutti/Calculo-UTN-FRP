from panda3d.core import SamplerState, TransparencyAttrib

import app
from app.controller.console import command, execute
from app.model import RebarSet
from app.model.code_checks.code_check_CIRSOC_201 import CodeCheckCIRSOC201
from app.view.interface.tools import *
from app.view.simpleui import SimpleFrame
import math
from PIL import Image, ImageDraw

class UI:
    def __init__(self, frame):
        model_reg = app.model_reg
        entities = model_reg.find_entities("CodeCheckCIRSOC201")
        if entities:
            entities = list(entities)
            self.code_check = entities[0]
        else:
            self.code_check = CodeCheckCIRSOC201()

        create_label("Dimensionado", frame, padding=[10, 0, 0, 0],
                     margin=[0, 0, 0, 10], font_size=14)

        content = SimpleFrame(
            parent=frame,
            sizeHint=[1, 1],
            layout="BoxLayout",
            layoutDir="Y",
            margin=[10, 10, 35, 0],
            alpha=0
        )
        create_label("Seleccione una barra", content, margin=[0,0,10,10])

        columns_container = SimpleFrame(
            parent=content,
            sizeHint=[None, None],
            size=[None, None],
            layout="BoxLayout",
            layoutDir="X",
            alpha=0,
            margin=[0, 0, 10, 10]
        )

        execute("regen_ui")

        self.col1 = SimpleScrolledFrame(position=[0, 0],
                                        canvasSize=(0, 100, -200, 0),
                                        size=[250, None],
                                        sizeHint=[0.25, 1],
                                        parent=columns_container,
                                        frameColor=scheme_rgba(
                                            COLOR_SEC_LIGHT),
                                        alpha=1,
                                        padding=[0, 1, 0, 0],
                                        layout="GridLayout",
                                        layoutDir="X",
                                        gridCols=1,
                                        gridRows=10)

        self.col2 = SimpleFrame(position=[0, 0],
                                sizeHint=[0.75, 1],
                                parent=columns_container,
                                frameColor=scheme_rgba(COLOR_SEC_LIGHT),
                                padding=[1, 0, 0, 0],
                                alpha=1,
                                layout="BoxLayout",
                                layoutDir="Y")

        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("Bar")

        self.title = create_label("Seleccione una barra", self.col2,
                                  padding=[0, 0, 0, 0], font_size=16)

        self.btn_container1 = SimpleFrame(position=[0, 0],
                                                     sizeHint=[1, None],
                                                     size=[None, 30],
                                                     parent=self.col2,
                                                     frameColor=scheme_rgba(
                                                         COLOR_SEC_LIGHT),
                                                     padding=[1, 0, 0, 0],
                                                     alpha=1,
                                                     layout="BoxLayout",
                                                     layoutDir="X",
                                         margin=[0,0, 0, 15])
        self.btn_container2_list = list()


        self.btn_container2 = SimpleFrame(position=[0, 0],
                                          sizeHint=[1, None],
                                          size=[None, 30],
                                          parent=self.col2,
                                          frameColor=scheme_rgba(
                                              COLOR_SEC_LIGHT),
                                          padding=[1, 0, 0, 0],
                                          alpha=1,
                                          layout="BoxLayout",
                                          layoutDir="X",
                                          margin=[0, 0, 0, 0])

        col_rollover = draw.merge_color(COLOR_SEC_DARK, COLOR_MAIN_LIGHT, 0.8)
        self.default_colors = [COLOR_SEC_DARK, COLOR_MAIN_LIGHT, col_rollover,
                               COLOR_MAIN_LIGHT]
        self.selected_colors = [COLOR_MAIN_LIGHT, COLOR_MAIN_LIGHT,
                                col_rollover,
                                COLOR_MAIN_LIGHT]

        new_button("Flexión", parent=self.btn_container1, colors=self.selected_colors)
        new_button("Corte", parent=self.btn_container1)

        self.selected_bar = None
        self.selected_bar_btn = None

        self.selected_rebar = None
        self.selected_rebar_btn = None

        self.bar_list_buttons = list()

        for bar in entities:
            if self.selected_bar is None:
                self.selected_bar = bar

            btn = new_button(str(bar), parent=self.col1.canvas,
                             command=self.explore_bar, args=[bar])
            self.bar_list_buttons.append(btn)

        model = []

        execute("regen_ui")
        self.subcol_container = SimpleFrame(position=[0, 0],
                                    parent=self.col2,
                                    frameColor=scheme_rgba(COLOR_SEC_LIGHT),
                                    padding=[1, 0, 0, 0],
                                    alpha=1,
                                    layout="BoxLayout",
                                    layoutDir="X")

        self.subcol_1 = SimpleFrame(size=[300, None],
                                    sizeHint=[None, 1],
                                    parent=self.subcol_container,
                                    frameColor=scheme_rgba(COLOR_SEC_DARK),
                                    padding=[10, 10, 10, 10],
                                    alpha=1,
                                    layout="BoxLayout",
                                    layoutDir="Y")

        self.subcol_2 = SimpleFrame(#sizeHint=[None, 1],
                                    parent=self.subcol_container,
                                    frameColor=scheme_rgba(COLOR_SEC_DARK),
                                    margin=[10, 0, 0, 0],
                                    padding=[10, 10, 10, 10],
                                    alpha=1,
                                    layout="BoxLayout",
                                    layoutDir="Y")
        self.subcol_3 = SimpleFrame(#sizeHint=[0.3, 1],
                                    parent=self.subcol_container,
                                    frameColor=scheme_rgba(COLOR_SEC_DARK),
                                    margin=[10, 0, 0, 0],
                                    padding=[10, 10, 10, 10],
                                    alpha=0,
                                    layout="BoxLayout",
                                    layoutDir="Y")

        create_label("Configuración", self.subcol_1,
                     margin=[5, 0, 10, 5], font_size=16)

        self.prop_editor = PropEditor(self.subcol_1, 300, self.update)

        create_label("Memoria de cálculo", self.subcol_2,
                     margin=[5, 0, 10, 5], font_size=16)

        create_label("Esquemas", self.subcol_3,
                     margin=[5, 0, 10, 5], font_size=16)

        self.log_label = create_label("LOG", self.subcol_2, margin=[10, 0, 0, 0], alpha=0)

        #tex = app.base.loader.loadTexture("data\\img\\logo-utn.png")
        #tex.setMagfilter(SamplerState.FT_nearest)

        tex = None


        self.image_frame = SimpleFrame(  # sizeHint=[0.3, 1],
            parent=self.subcol_3,
            #frameColor=scheme_rgba(COLOR_SEC_DARK),
            size=[40, 46],
            margin=[10, 0, 0, 0],
            #padding=[10, 10, 10, 10],
            #image=tex,
            #image_scale=(tex.x_size, tex.z_size, tex.y_size),
            #image_pos=(tex.x_size, 0, -tex.y_size)
            #image="circle.png"
            alpha=0
            )

        self.image_frame.setTransparency(TransparencyAttrib.MAlpha)




        #self.explore_bar(self.selected_bar)

        self.update()

        execute("regen_ui")

    def update(self):

        for btn in self.bar_list_buttons:
            btn.destroy()
        self.bar_list_buttons.clear()

        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("Bar")



        for bar in entities:


            btn = new_button(str(bar), parent=self.col1.canvas,
                             command=self.explore_bar, args=[bar])

            btn["extraArgs"] = [bar, btn]

            self.bar_list_buttons.append(btn)

            if self.selected_bar is None:
                self.explore_bar(bar, btn)
            elif self.selected_bar is bar:
                self.explore_bar(bar, btn)


        execute("regen_ui")

    def explore_bar(self, bar_entity, btn):
        if bar_entity:
            if bar_entity is not self.selected_bar:
                print("reset open_rebar_set", bar_entity, self.selected_bar)
                self.open_rebar_set(None, None)

            self.selected_bar = bar_entity
            if self.selected_bar_btn and not self.selected_bar_btn.isEmpty():
                self.selected_bar_btn["colorList"] = self.default_colors

            self.selected_bar_btn = btn
            if not btn.isEmpty():
                self.selected_bar_btn["colorList"] = self.selected_colors

            self.title["text"] = str(bar_entity)

            if bar_entity.behavior == "Viga" and not bar_entity.rebar_sets:
                RebarSet(bar_entity, "Tramo", 0)
                RebarSet(bar_entity, "Perchas", 1)

                '''rebar_start = RebarSet(bar_entity, "Apoyo 1")
                rebar_start.end = app.ureg("20 percent")
                rebar_end = RebarSet(bar_entity, "Apoyo 2")
                rebar_end.start = app.ureg("80 percent")'''

            if self.selected_bar.behavior == "Viga":
                self.log_label["text"] = self.code_check.verify_beam(
                    self.selected_bar)
            else:
                self.log_label["text"] = self.code_check.verify_column(
                    self.selected_bar)

            for btn in self.btn_container2_list:
                btn.destroy()
            self.btn_container2_list.clear()

            rebars = sorted(bar_entity.rebar_sets, key=lambda x: x.name)

            for rebar in rebars:
                btn = new_button(rebar.name, parent=self.btn_container2,
                                 command=self.open_rebar_set, args=[rebar])
                self.btn_container2_list.append(btn)

                btn["extraArgs"] = [rebar, btn]

                if self.selected_rebar is None:
                    self.open_rebar_set(rebar, btn)
                elif self.selected_rebar is rebar:
                    self.open_rebar_set(rebar, btn)






            #new_button("Tramo", parent=self.btn_container1)
            #new_button("Apoyo 1", parent=self.btn_container1)
            #new_button("Apoyo 2", parent=self.btn_container1)



            scale = 240

            tex = self.code_check.generate_rebar_image(self.selected_bar, scale)

            self.image_frame["image"] = tex
            self.image_frame["image_scale"] = (tex.x_size/2, tex.z_size/2, -tex.y_size/2)
            #self.image_frame["image_scale"] = (256/2, 1, 256/2)
            #print("tex.x_size", tex.x_size)
            #print("tex.z_size", tex.z_size)
            #print("tex.y_size", tex.y_size)

            self.image_frame["image_pos"] = (tex.x_size/2, 0, -tex.y_size/2)
            w,h = self.selected_bar.section.size
            self.image_frame["size"] = (round(w*scale), round(h*scale))

            execute("regen_ui")

    def open_rebar_set(self, rebar_set, btn):
        self.selected_rebar = rebar_set
        if self.selected_rebar_btn:
            self.selected_rebar_btn["colorList"] = self.default_colors

        self.selected_rebar_btn = btn
        if self.selected_rebar_btn:
            self.selected_rebar_btn["colorList"] = self.selected_colors

        self.prop_editor.entity_read(rebar_set)


@command(name="view_design")
def view_results():
    tab_manager = app.main_ui.tab_manager

    index = 0
    for tab in tab_manager.tabs:

        if tab.title == "Dimensionado":
            tab_manager.set_active_tab(index)
            return None
        index += 1

    new_tab = tab_manager.create_new_tab("Dimensionado")
    frame = new_tab.frame
    frame["frameColor"] = scheme_rgba(COLOR_SEC_LIGHT)
    frame["layoutDir"] = "Y"

    ui = UI(frame)
    new_tab.ev_focus_in = ui.update
