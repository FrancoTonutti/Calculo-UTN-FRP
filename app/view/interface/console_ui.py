from app import app
from .layout_controller import Layout
from direct.showbase.DirectObject import DirectObject
from app.view import draw
from app.view.widgets.entry import Entry
from app.view.simpleui.simple_entry import SimpleEntry
from direct.task.Task import TaskManager
from app.controller.console import execute





class ConsoleUI(DirectObject):
    def __init__(self, layout: Layout):
        self.tsk = TaskManager()
        self.frame = layout.work_area
        self.font_size = 14
        self.args_size = 15
        self.entry = self.create_input(20, "Ingrese un comando", pos=0, command=execute)
        self.entry.hide()

        app.console_input = self.entry
        app.console = self

        self._args_input = dict()
        self._activecommand = None
        self._activearg = None
        self._command_name = ""

    def get_active_command_name(self):
        if self.tsk.hasTaskNamed("command_task"):
            return self._command_name
        else:
            self._command_name = ""
            return None


    @property
    def active_command(self):
        return self._activecommand

    @active_command.setter
    def active_command(self, value):

        if value is None:
            #self.entry.show()
            print("ACTIVE COMMAND SETTER")

            for entry in self._args_input.values():
                entry.detachNode()

            self._args_input.clear()

        elif self._activecommand is not value:
            self._activecommand = value
            data = app.commands.get(value, None)
            if data is not None:
                print("data", data)
                args = data.get("args")
                if args is not None:

                    self.entry.hide()
                    print("entry hide", self.entry.get_value())

                    total_width = (self.args_size * self.font_size) * len(args) + 40 * (len(args) - 1)
                    x0 = -total_width / 2
                    print("x0", x0)
                    for arg in args:
                        x0 += self.args_size * self.font_size / 2
                        entry = self.create_input(self.args_size, arg, x0,
                                                  command_focus=self.cmd_focus_in,
                                                  command_defocus=self.cmd_focus_out,
                                                  arg=arg)
                        x0 += self.args_size * self.font_size / 2 + 40

                        self._args_input.update({arg: entry})

    def cmd_focus_in(self, text, arg):
        self._activearg = arg

    def cmd_focus_out(self, text):
        self._activearg = None

    def get_active_arg(self):
        return self._activearg

    def get_arg(self, arg):
        entry = self._args_input.get(arg, None)

        if entry is not None:
            return entry.get_value()
        else:
            return None

    def set_arg(self, arg, value):
        entry = self._args_input.get(arg, None)

        if entry is not None:
            entry.enter_value(value)

    def set_arg_typefuc(self, arg, fuction):
        entry = self._args_input.get(arg, None)

        if entry is not None:
            entry["typeFunc"] = fuction

    def set_arg_suffix(self, arg, suffix):
        entry = self._args_input.get(arg, None)

        if entry is not None:
            entry["suffix"] = suffix

    def create_input(self, width, label, pos=0.0, command=None,command_focus=None,command_defocus=None, arg=None):
        entry = SimpleEntry(
            text_fg=(1, 1, 1, 1),
            orginH="center",
            orginV="bottom",
            position=[-width/2 * self.font_size + pos, -25],
            text_scale=(self.font_size, self.font_size),
            width=width,
            frameColor="C_DKGRAY",
            label=label,
            align="center",
            command=command,
            parent=self.frame,
            focusInCommand=command_focus,
            focusInExtraArgs=[arg],
            focusOutCommand=command_defocus

        )
        app.add_gui_region("console_input", entry)

        entry.setColorScale(1, 1, 1, 1)
        # entry.setBin("fixed", 1)
        c = draw.draw_cicle(0, 9, 9, "C_DKGRAY", entry)
        c.setBin("fixed", 0)
        c = draw.draw_cicle(width * self.font_size, 9, 9, "C_DKGRAY", entry)
        c.setBin("fixed", 0)

        return entry

    def command_ended(self, task):
        self._command_name = ""
        app.main_ui.status_bar.command_ended()

    def start_command(self, task, name="Comando"):
        if not self.tsk.hasTaskNamed("command_task"):
            self.tsk.add(task, "command_task", uponDeath=self.command_ended)
            self._command_name = name
            app.main_ui.status_bar.command_start(name)

    def close_command(self):
        print("close_command start")
        if self.active_command:
            print("close_command", self.tsk.hasTaskNamed("command_task"))

            self.tsk.remove("command_task")
            self.active_command = None
