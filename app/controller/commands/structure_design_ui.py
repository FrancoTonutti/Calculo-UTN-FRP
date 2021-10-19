from app.controller.console import command, execute
from app.model.code_checks.code_check_CIRSOC_201 import CodeCheckCIRSOC201
from app.view.interface.tools import *
from app.view.simpleui import SimpleFrame


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

        new_button("Tramo", parent=self.btn_container1)
        new_button("Apoyo 1", parent=self.btn_container1)
        new_button("Apoyo 2", parent=self.btn_container1)

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

        new_button("Flexión", parent=self.btn_container2)
        new_button("Corte", parent=self.btn_container2)



        self.selected_bar = None
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
                                    # frameColor=scheme_rgba(COLOR_SEC_LIGHT),
                                    padding=[1, 0, 0, 0],
                                    alpha=1,
                                    layout="BoxLayout",
                                    layoutDir="X")

        self.subcol_1 = SimpleFrame(sizeHint=[0.4, 1],
                                parent=self.subcol_container,
                                frameColor=scheme_rgba(COLOR_SEC_LIGHT),
                                padding=[1, 0, 0, 0],
                                alpha=0.5,
                                layout="BoxLayout",
                                layoutDir="Y")

        create_label("Memoria de cálculo", self.subcol_1,
                     margin=[0, 0, 10, 0], font_size=16)

        self.subcol_2 = SimpleFrame(sizeHint=[0.3, 1],
                                    parent=self.subcol_container,
                                    frameColor=scheme_rgba(COLOR_SEC_LIGHT),
                                    padding=[1, 0, 0, 0],
                                    alpha=0.5,
                                    layout="BoxLayout",
                                    layoutDir="Y")
        self.subcol_3 = SimpleFrame(sizeHint=[0.3, 1],
                                    parent=self.subcol_container,
                                    frameColor=scheme_rgba(COLOR_SEC_LIGHT),
                                    padding=[1, 0, 0, 0],
                                    alpha=0.5,
                                    layout="BoxLayout",
                                    layoutDir="Y")

        self.log_label = create_label("LOG", self.subcol_1, margin=[0, 0, 0, 0], alpha=0)

        self.explore_bar(self.selected_bar)

        execute("regen_ui")

    def update(self):

        for btn in self.bar_list_buttons:
            btn.destroy()
        self.bar_list_buttons.clear()

        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("Bar")

        self.selected_bar = None

        for bar in entities:
            if self.selected_bar is None:
                self.selected_bar = bar

            btn = new_button(str(bar), parent=self.col1.canvas,
                             command=self.explore_bar, args=[bar])
            self.bar_list_buttons.append(btn)

        self.explore_bar(self.selected_bar)

        execute("regen_ui")

    def explore_bar(self, bar_entity):
        if bar_entity:
            self.selected_bar = bar_entity

            self.title["text"] = str(bar_entity)

            if self.selected_bar.behavior == "Viga":
                self.log_label["text"] = self.code_check.verify_beam(
                    self.selected_bar)
            else:
                self.log_label["text"] = self.code_check.verify_column(
                    self.selected_bar)


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
