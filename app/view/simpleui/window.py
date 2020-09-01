import os
import sys
from panda3d.core import Multifile
from panda3d.core import WindowProperties, Filename, MouseWatcher

from app import app

cursor_dir = "data/cursors/"
cr_arrow = "arrow.cur"
cr_link = "link.cur"
cr_cross = 3
cr_beam = "beam.cur"
cr_size_nesw = 5
cr_size_ns = 6
cr_size_nwse = 7
cr_size_we = 8
cr_uparrow = 9
cr_hourglass = 10
cr_appstart = 11
cr_handpoint = 12
cr_size_all = 13


def set_cursor_dir(directory: str):
    """
    set te default cursor directory for .cur files

    ex: path/to/cursors/

    """
    global cursor_dir
    if directory[-1] != "/":
        directory += "/"
    cursor_dir = directory


def set_cursor(cursor: str):
    """
    change the current filename cursor from the default cursor directory
    """
    global cursor_dir
    cursor_filename = cursor_dir + cursor

    winprops = WindowProperties()
    winprops.setCursorFilename(cursor_filename)

    base = app.get_show_base()
    base.win.requestProperties(winprops)


def set_window_icon(file: str):
    winprops = WindowProperties()
    winprops.setIconFilename(file)

    base = app.get_show_base()
    base.win.requestProperties(winprops)



