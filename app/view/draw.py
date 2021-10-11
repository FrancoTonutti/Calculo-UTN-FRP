from app import app
from PIL import ImageFont
from panda3d.core import DynamicTextFont, TextNode, LineSegs, NodePath, WindowProperties, Filename
from typing import Type
import builtins
from direct.showbase.Loader import Loader
from direct.gui import DirectGuiGlobals as DGG
import direct.showbase.ShowBaseGlobal as SBG

DRAW_DATA = {
    "fonts": {
        "_active": "arial",
        "_size": 12
    },
    "_active_color": "C_RAISIN_BLACK"
}


def draw_set_font(font_name=None, font_size=None):
    if font_name is not None:
        fonts = DRAW_DATA.get("fonts")
        fonts.update({"_active": font_name})
        if font_size is not None:
            fonts.update({"_size": font_size})

    font = draw_get_font()

    DGG.setDefaultFont(font[0])

    return font


def draw_get_font(font_name: str = None, font_size: int = None) -> (
Type[DynamicTextFont], Type[ImageFont.FreeTypeFont]):
    """
    Devuelve la fuente activa, o la fuente especificada como parámetro

    """
    fonts = DRAW_DATA.get("fonts")

    if font_name is None:
        font_name = fonts.get("_active")
    if font_size is None:
        font_size = fonts.get("_size")

    if font_name not in fonts:
        loader = app.get_show_base().loader
        font_panda3d = loader.loadFont("data/fonts/{}.ttf".format(font_name))
        font_panda3d.setPixelSize(30)
        font_pil = ImageFont.truetype("data/fonts/{}.ttf".format(font_name), font_size)
        fonts[font_name] = {"panda3d": font_panda3d, "pil{}".format(font_size): font_pil}

        #fonts.update({font_name: {"panda3d": font_panda3d, "pil{}".format(font_size): font_pil}})

    else:
        font = fonts.get(font_name)
        font_panda3d = font.get("panda3d")
        font_pil = font.get("pil{}".format(font_size))

        if not font_pil:
            font_pil = ImageFont.truetype(
                "data/fonts/{}.ttf".format(font_name), font_size)

            font_data = fonts.get(font_name)
            font_data.update({"pil{}".format(font_size): font_pil})



    fonts.update({"_active": font_name})

    return font_panda3d, font_pil


C_AQUA = (0, 255, 255)
C_BLACK = (0, 0, 0)
C_BLUE = (0, 0, 255)
C_DKGRAY = (64, 64, 64)
C_RED = (255, 0, 0)
C_GREEN = (0, 128, 0)
C_LIME = (0, 255, 0)
C_WHITE = (255, 255, 255)

# https://www.webnots.com/flat-ui-color-codes/
C_TURQUOISE = (26, 188, 156)
C_GREEN_SEA = (22, 160, 133)
C_EMERALD = (46, 204, 113)
C_NEPHRITIS = (39, 174, 96)
C_PETER_RIVER = (52, 152, 219)
C_BELIZE_HOLE = (41, 128, 185)
C_AMETHYST = (155, 89, 182)
C_WISTERIA = (142, 68, 173)
C_WET_ASPHALT = (52, 73, 94)
C_MIDNIGHT_BLUE = (44, 62, 80)
C_SUN_FLOWER = (241, 196, 15)
C_ORANGE = (243, 156, 18)
C_CARROT = (230, 126, 34)
C_PUMPKIN = (211, 84, 0)
C_ALIZARIN = (231, 76, 60)
C_POMEGRANATE = (192, 57, 43)
C_CLOUDS = (236, 240, 241)
C_SILVER = (189, 195, 199)
C_CONCRETE = (149, 165, 166)
C_ASBESTOS = (127, 140, 141)

# https://www.schemecolor.com/flat-black.php
C_DARK_LIVER = (77, 77, 77)
C_RAISIN_BLACK = (38, 38, 38)


def get_color(color_name, color_format="RGB", alpha=255):
    if isinstance(color_name, str):
        color = globals().get(color_name, (0, 0, 0))
    else:
        color = color_name

    if color_format.islower():
        color = tuple(val / 255 for val in color)

    if (color_format is "RGBA" or color_format is "rgba") and len(color) < 4:
        if color_format is "rgba" and alpha > 1:
            alpha /= 255
        color += (alpha,)

    return color


def draw_get_color(color_name=None, color_format="RGB", alpha=255):
    """
    Devuelve la fuente activa, o la fuente especificada como parámetro

    """
    if color_name is None:
        color_name = DRAW_DATA.get("_active_color")

    return get_color(color_name, color_format, alpha)


def draw_set_color(color_name):
    """
    Devuelve la fuente activa, o la fuente especificada como parámetro

    """
    if isinstance(color_name, tuple):
        colors_keys = list(globals().keys())
        colors_value = list(globals().values())
        index = colors_value.index(color_name)
        color_name = colors_keys[index]

    DRAW_DATA.update({"_active_color": color_name})


def merge_color(color1, color2, amount=0.5, color_format="RGB"):
    color1 = get_color(color1, color_format)
    color2 = get_color(color2, color_format)

    color = []
    for component1, component2 in zip(color1, color2):
        color.append(round(component1 + (component2 - component1) * amount))

    return tuple(color)


def draw_text(x, y, text, font_size=None, text_color=None, parent=None) -> TextNode:
    """
    Dibuja un texto en la posición indicada, por defecto toma la fuente, tamaño y color del modulo draw

    Argumentos:
    x -- distancia de izquierda a derecha
    y -- distancia de arriba hacia abajo
    text -- texto a dibujar
    font_size -- tamaño de la fuente (default None)
    text_color -- color del texto (default None)
    """
    font_panda, font_pil = draw_get_font()

    text_color = draw_get_color(color_format="rgba")
    fonts = DRAW_DATA.get("fonts")
    if font_size is None:
        font_size = fonts.get("_size")

    new_text = TextNode('node name')
    new_text.setText(text)
    new_text.setTextColor(text_color)

    if parent is None:
        parent = pixel2d

    text_node_path = parent.attachNewNode(new_text)
    text_node_path.setScale(font_size)
    text_node_path.setPos(x, 0, -y)

    return new_text


def draw_line_2d(x1, y1, x2, y2, w=1, color=None, parent=None):
    """
    Dibuja un segmento de linea, teniendo como origen de cordenadas la esquina superior izquierda de la pantalla
    """

    line = LineSegs()
    line.setThickness(w)

    color = draw_get_color(color, color_format="rgba")

    line.setColor(color)
    line.moveTo(x1, 0, -y1)
    line.drawTo(x2, 0, -y2)

    node = line.create(dynamic=False)

    if parent is None:
        parent = pixel2d

    np = NodePath(node)
    np.reparentTo(parent)

    return np


def draw_line_3d(x1, y1, z1, x2, y2, z2, w=1, color=None, parent=None, dynamic=False):
    """
    Dibuja un segmento de linea, teniendo como origen de cordenadas la esquina superior izquierda de la pantalla
    """

    line = LineSegs()
    line.setThickness(w)

    color = draw_get_color(color, color_format="rgba")

    line.setColor((1, 1, 1, 1))
    line.moveTo(x1, y1, z1)
    line.drawTo(x2, y2, z2)

    node = line.create(dynamic=dynamic)

    print("draw_line_3d_1", node)
    base = app.get_show_base()
    if parent is None:
        parent = base.render

    np = NodePath(node)
    print("draw_line_3d_2", np)
    np.reparentTo(parent)
    np.setColorScale(color)
    np.setLightOff()
    np.setPythonTag('line', line)
    np.setPythonTag('defcolor', color)
    if dynamic:
        return np, line
    else:
        return np


def draw_cicle(x, y, r, col=None, parent=None):
    base = app.get_show_base()
    loader = Loader(base)
    model = loader.loadModel("data/geom/circle.egg")

    col = draw_get_color(col, color_format="rgba")

    if parent is None:
        parent = builtins.pixel2d

    model.reparentTo(parent)

    model.setPos(x, 0, -y)
    model.setScale(r, 1, r)

    # model.setColorScale(1, 0, 0, 1)
    model.setColor(col)

    return model


def change_cursor(cursor_file):
    winprops = WindowProperties()
    filename = Filename.binaryFilename(cursor_file)
    print("filename", filename.exists())
    winprops.setCursorFilename(filename)
    base = app.get_show_base()
    base.win.requestProperties(winprops)
