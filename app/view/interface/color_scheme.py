from app.view import draw

COLOR_TEXT_LIGHT = (238, 238, 238)
COLOR_TEXT_DARK = (35, 35, 35)

COLOR_MAIN_DARK = (35, 35, 35)
COLOR_MAIN_LIGHT = (66, 66, 66)
COLOR_SEC_DARK = (43, 43, 43)
COLOR_SEC_LIGHT = (52, 52, 52)


def scheme_rgba(color):
    return draw.get_color(color, "rgba")

def scheme_rgb(color):
    return draw.get_color(color, "rgb")