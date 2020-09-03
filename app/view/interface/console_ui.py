from app import app
from .layout_controller import Layout
from direct.showbase.DirectObject import DirectObject
from app.view import draw
from app.view.widgets.entry import Entry
from app.view.simpleui.simple_entry import SimpleEntry

from app.controller.console import execute


def execute_console(cmd):
    execute(cmd)


class ConsoleUI(DirectObject):
    def __init__(self, layout: Layout):
        self.frame = layout.work_area

        entry = SimpleEntry(
            text_fg=(1, 1, 1, 1),
            orginH="center",
            orginV="bottom",
            position=[-10 * 15, -25],
            text_scale=(14, 14),
            width=20,
            frameColor="C_DKGRAY",
            label="Ingrese un comando",
            align="center",
            command=execute_console,
            parent=self.frame

        )
        app.console_input = entry
        app.add_gui_region("console_input", entry)

        entry.setColorScale(1, 1, 1, 1)
        #entry.setBin("fixed", 1)
        c = draw.draw_cicle(0, 9, 9, "C_DKGRAY", entry)
        c.setBin("fixed", 0)
        c = draw.draw_cicle(20 * 14, 9, 9, "C_DKGRAY", entry)
        c.setBin("fixed", 0)
