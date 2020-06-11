from kivy.uix.boxlayout import BoxLayout
from modules.user_interface.colors import PaletteColor

from modules.user_interface import widgets

from kivy.uix.label import Label
import ctypes, win32gui, win32con
from pandac.PandaModules import WindowProperties

"""

Este modulo no es usado actualmente y posiblemente sea eliminado en el futuro.

Se deja unicamete como referencia a las funciones win32 necesarias para el control de la ventana

"""


class WidTitleBar(BoxLayout, PaletteColor):

    def __init__(self):
        super(WidTitleBar, self).__init__()

        self.add_widget(Label(text='Hello world'))
        btn = widgets.WidButton("img/icon_minimize.png", call=self.minimize)
        btn.size_hint = (None, 1)
        btn.width = 34
        self.add_widget(btn)
        btn = widgets.WidButton("img/icon_maximize.png", call=self.maximize)
        btn.size_hint = (None, 1)
        btn.width = 34
        self.add_widget(btn)
        btn = widgets.WidButton(img_dir="img/icon_close.png", call=self.close)
        btn.size_hint = (None, 1)
        btn.width = 34
        self.add_widget(btn)

    def close(self):
        print("close")
        self.parent.panda3D.destroy()

    def minimize(self):
        print("minimize")

        properties = self.parent.panda3D.win.getProperties()

        title = properties.getTitle()

        window = ctypes.windll.user32.FindWindowW(None, title)
        ctypes.windll.user32.ShowWindow(window, 6)  # SW_MINIMIZE
        # https://docs.microsoft.com/es-es/windows/win32/api/winuser/nf-winuser-showwindow?redirectedfrom=MSDN

    def maximize(self):
        print("maximize")

        properties = self.parent.panda3D.win.getProperties()

        title = properties.getTitle()

        window = ctypes.windll.user32.FindWindowW(None, title)


        # window = win32gui.FindWindow("Notepad", None)
        if window:
            tup = win32gui.GetWindowPlacement(window)
            if tup[1] == win32con.SW_SHOWMAXIMIZED:
                print("maximized")
                ctypes.windll.user32.ShowWindow(window, win32con.SW_RESTORE)  # SW_RESTORE=9
            elif tup[1] == win32con.SW_SHOWMINIMIZED:
                print("minimized")
                ctypes.windll.user32.ShowWindow(window, win32con.SW_MAXIMIZE)  # SW_MAXIMIZE=3
            elif tup[1] == win32con.SW_SHOWNORMAL:
                print("normal")
                ctypes.windll.user32.ShowWindow(window, win32con.SW_MAXIMIZE)  # SW_MAXIMIZE=3

        properties.setFullscreen(False)

    def minimize2(self):
        properties = self.parent.panda3D.win.getProperties()
        properties.setMinimized(True)
        print(properties)

        notepad_handle = ctypes.windll.user32.FindWindowW(None, "Untitled - Notepad")
        ctypes.windll.user32.ShowWindow(notepad_handle, 6)
