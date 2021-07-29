from app.view.simpleui import style_template
from app import app
from app.view import draw

COLOR_TEXT_LIGHT = (238, 238, 238)
COLOR_MAIN_DARK = (35, 35, 35)
COLOR_MAIN_LIGHT = (66, 66, 66)
COLOR_SEC_DARK = (43, 43, 43)
COLOR_SEC_LIGHT = (52, 52, 52)
col_rollover = draw.merge_color(COLOR_MAIN_DARK, COLOR_MAIN_LIGHT, 0.2)

colors = [COLOR_MAIN_DARK, COLOR_MAIN_LIGHT, col_rollover, "C_CONCRETE"]


font_panda3d, font_pil = draw.draw_get_font()

style_template.create_template(
    "command_button",
    text_scale=(12, 12),
    text_font=font_panda3d,
    font_pil=font_pil,
    text_fg=draw.get_color(COLOR_TEXT_LIGHT, "rgba"),
    colorList=colors,

)