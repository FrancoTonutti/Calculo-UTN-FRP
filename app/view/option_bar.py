from app import app
from app.view import draw
from app.view.interface.color_scheme import *
from app.view.widgets.wideFrame import WideFrame
from app.controller.console import execute
from app.view.simpleui.simple_frame import SimpleFrame
from app.view.simpleui.simple_button import SimpleButton

# Soporte para funcionalidad de traducción en un futuro
import gettext

_ = gettext.gettext

INTERFACE = {
    _("Archivo"): {
        "Archivo": {
            "Nuevo": {"command": "new_file"},
            "Abrir": {"command": "open_file"},
            "Guardar": {"command": "save"},
            #"Exportar IFC": {"command": "save_ifc"},
        }
    },
    _("Estructura"): {
        "Construir": {
            #"Muro de carga": {},
            "Barra": {"command": "barra"},
            "Pilar": {"command": "barra"},
            "Viga": {"command": "beam"},
        },
        "Modelo": {
            "Agregar carga": {"command": "load"},
            "Combinaciones": {"command": "load_combinations"},
            # "Regen": {"command": "regen"},
            "Ver secciones": {"command": "wire"}
        },
        "Definiciones": {
            "Materiales": {"command": "material_editor"},
            "Secciones": {"command": "section_editor"}
        },
    },
    _("Cálculo"): {
        "Cálculo": {
            "Calcular": {"command": "matricial"},
            "Combinaciones": {"command": "load_combinations"},
            "Resultados": {"command": "view_results"},
            "Borrar": {"command": "remove_diagrams"},
        },
    }
}

"""COLOR_MAIN_DARK = "C_NEPHRITIS"
COLOR_MAIN_LIGHT = "C_WHITE"
COLOR_TEXT_LIGHT = (238, 238, 238)
COLOR_MAIN_DARK = (35, 35, 35)
COLOR_MAIN_LIGHT = (66, 66, 66)
COLOR_SEC_DARK = (43, 43, 43)
COLOR_SEC_LIGHT = (52, 52, 52)"""




def new_button(text, x, y, colors=None, command=None, args=None, parent=None, size=None, padding=None, margin=None):
    if args is None:
        args = []
    font_panda3d, font_pil = draw.draw_get_font()
    if colors is None:
        col_rollover = draw.merge_color(COLOR_MAIN_DARK, COLOR_MAIN_LIGHT, 0.2)
        colors = [COLOR_MAIN_DARK, COLOR_MAIN_LIGHT, col_rollover, "C_CONCRETE"]
    if size is None:
        width = font_pil.getsize(text)[0]
        size = [width, 20]

    if padding is None:
        padding = [0, 0, 0, 0]

    if margin is None:
        margin = [0, 0, 0, 0]

    btn = SimpleButton(text=text,
                       text_scale=(12, 12),
                       text_font=font_panda3d,
                       text_fg=draw.get_color(COLOR_TEXT_LIGHT, "rgba"),
                       command=command,
                       parent=parent,
                       extraArgs=args,
                       colorList=colors,
                       position=[x, y],
                       padding=padding,
                       margin=margin,
                       size=size
                       )

    return btn


class OptionBar:
    def __init__(self):

        self.panda3d = app.get_show_base()

        #self.options_frame = WideFrame(position=[0, 125], colorString=COLOR_MAIN_DARK)
        """self.options_frame = SimpleFrame(position=[0, 0],
                                       size=[1366, 150],
                                       sizeHint=[1, None],
                                       alpha=0,
                                       padding=[0, 0, 0, 0],
                                       layout="BoxLayout",
                                       layoutDir="Y")"""
        self.options_frame = app.layout.options_bar
        self.options_bar_titles = app.layout.options_bar_titles
        #self.button_tabs_frame = SimpleFrame(size=[None, 25], parent=self.options_frame, sizeHint=[1, 0.5])

        workspace = SimpleFrame(position=[0, 0], sizeHint=[1, 1], alpha=0, padding=[250, 0, 30, 150])



        self.tab_btn = []
        self.tab_frames = []
        self.active_tab = 0
        # frame2 = WideFrame(position=[25, 100], colorString="C_WHITE", parent=self.options_frame)

        self.create_tab_buttons()
        self.set_active_tab(0)

    def create_tab_buttons(self):
        x = 0
        for tab, sections in INTERFACE.items():
            index = len(self.tab_btn)
            # Se crea el botón que permite seleccionar una pestaña del menu
            btn = new_button(tab, x, 5, parent=self.options_bar_titles, command=self.set_active_tab, args=[index], padding=[10, 10, 0, 0])
            self.tab_btn.append(btn)
            width = btn.box_size()[0]
            x += width + 50

            # Se crea el marco que contendrá los botones de la pestaña y se lo oculta por defecto
            tab_frame = WideFrame(position=[25, 125], colorString=COLOR_MAIN_LIGHT, parent=self.options_frame)
            self.tab_frames.append(tab_frame)
            tab_frame.hide()

            xx = 0
            for section, buttons in sections.items():
                xx_start = xx
                for button, button_data in buttons.items():
                    c1 = COLOR_MAIN_LIGHT
                    c2 = COLOR_MAIN_DARK
                    col_rollover = draw.merge_color(c1, c2, 0.2)
                    colors = [c1, c2, col_rollover, "C_CONCRETE"]

                    b = new_button(button, xx, 2.5, colors=colors, parent=tab_frame, padding=[10, 10, 0, 0])
                    if button_data.get("command"):
                        b["command"] = execute
                        b["extraArgs"] = [button_data.get("command")]
                    # b["text_wordwrap"] = 4
                    b["textCenterY"] = False
                    posx, posy = b["text_pos"]
                    b["text_pos"] = (posx, -60)
                    size = b["size"]
                    b["size"] = [size[0], 70]
                    # b["frameSize"] =(-50,50,0,20)
                    width = b.box_size()[0]
                    xx += width + 5

                colors = [COLOR_MAIN_LIGHT, COLOR_MAIN_LIGHT]
                new_button(section, xx_start, 75 + 2.5, parent=tab_frame, size=[xx - xx_start - 5, 20], colors=colors)

                draw.draw_line_2d(xx_start, 75, xx - 5, 75, parent=tab_frame, color=COLOR_MAIN_DARK)
                draw.draw_line_2d(xx - 2.5, 5, xx - 2.5, 95, parent=tab_frame, color=COLOR_MAIN_DARK)
                # draw.draw_text((xx+xx_start)/2, 90, section, parent=tab_frame)

                # draw.draw_text(xx,100,section)

    def set_active_tab(self, index):
        btn = self.tab_btn[self.active_tab]
        col_rollover = draw.merge_color(COLOR_MAIN_DARK, COLOR_MAIN_LIGHT, 0.2)
        btn["colorList"] = [COLOR_MAIN_DARK, COLOR_MAIN_LIGHT, col_rollover, "C_CONCRETE"]
        frame = self.tab_frames[self.active_tab]
        frame.hide()

        self.active_tab = index
        btn = self.tab_btn[self.active_tab]
        btn["colorList"] = [COLOR_MAIN_LIGHT, COLOR_MAIN_LIGHT]
        frame = self.tab_frames[self.active_tab]
        frame.show()
