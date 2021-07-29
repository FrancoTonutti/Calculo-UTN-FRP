"""A DirectFrame is a basic DirectGUI component that acts as the base
class for various other components, and can also serve as a basic
container to hold other DirectGUI components.

A DirectFrame can have:

* A background texture (pass in path to image, or Texture Card)
* A midground geometry item (pass in geometry)
* A foreground text Node (pass in text string or OnscreenText)

Each of these has 1 or more states.  The same object can be used for
all states or each state can have a different text/geom/image (for
radio button and check button indicators, for example).

See the :ref:`directframe` page in the programming manual for a more in-depth
explanation and an example of how to use this class.
"""

__all__ = ['SimpleFrame']

from app.view import draw
from app import app
import sys
from direct.gui.DirectFrame import *

if sys.version_info >= (3, 0):
    stringType = str
else:
    stringType = basestring


class SimpleFrame(DirectFrame):
    """
    Crea un Frame que abarca el ancho de la pantalla

    Argumentos

    position -- Lista con las alturas inicial y final del marco, desde arriba hacia abajo (default: [0, 10])
    Ademas todos los parametros heredados de DirectFrame
    """

    def __init__(self, parent=None, override_default=False, **kw):

        if isinstance(parent, SimpleFrame):
            self.parent_gui = parent
        else:
            self.parent_gui = None

            #
            if parent is not None:
                if parent.hasPythonTag('simple_gui'):
                    self.parent_gui = parent.getPythonTag("simple_gui")

            """if parent is not None:
                if str(parent).endswith("/canvas"):
                    obj = parent.parent.parent
                    if obj.hasPythonTag('simple_gui'):
                        self.parent_gui = obj.getPythonTag("simple_gui")"""

        self.layout_size_hint = [None, None]

        optiondefs = (

            ('frameColor', "C_CARROT", self.setFrameColor),
            ('position', [0, 0], self.set_position),
            ('size', [None, None], self.set_size),
            ('orginV', "top", self.set_position),
            ('orginH', "left", self.set_position),
            ('sizeHint', [None, None], self.set_size),
            ('alpha', 255, self.setFrameColor),
            ('padding', [0, 0, 0, 0], self.set_size),
            ('layout', "FloatLayout", None),
            ('layoutDir', "X", None),
            ('gridCols', 1, None),
            ('gridRows', 1, None),
            ('rowDefaultHeight', None, None),
            ('colDefaultWidth', None, None),
            ('colsMinimum', {}, None),
            ('rowsMinimum', {}, None),
            ('frameSize', (0, 32, -32, 0), self.setFrameSize),
        )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        if parent is None:
            parent = pixel2d

        if override_default is False:
            DirectFrame.__init__(self, parent)

        self.setPythonTag('simple_gui', self)

        # Call option initialization functions
        self.initialiseoptions(SimpleFrame)

        self.set_position()
        size = self['frameSize']
        if size is not None:
            self.setPos(-size[0], 0, -size[3])
        else:
            self.setPos(0, 0, 0)
        self.flattenLight()
        self.set_position()
        self.parent_width, self.parent_height = self.get_parent_size()

    def set_size(self):

        pad = self["padding"]
        pad_x = pad[0] + pad[1]
        pad_y = pad[2] + pad[3]

        width, height = self.box_size()

        width = max(width - pad_x, 0)
        height = max(height - pad_y, 0)

        self["frameSize"] = (0, width, -height, 0)

        self.update_text_pos()
        self.set_position()

    def box_size(self):
        width, height = self["size"]
        hint_x, hint_y = self["sizeHint"]

        if hint_x is None and hint_y is None:
            hint_x, hint_y = self.layout_size_hint

        if width is None:
            width = 0
        if height is None:
            height = 0

        parent_width, parent_height = self.get_parent_size()

        if hint_x is not None:
            width = parent_width * hint_x

        if hint_y is not None:
            height = parent_height * hint_y

        return [width, height]

    def get_parent_size(self):
        if self.parent == pixel2d:
            parent_width = app.get_show_base().win.getXSize()
            parent_height = app.get_show_base().win.getYSize()
        else:

            if self.parent_gui is not None:
                size = self.parent_gui["frameSize"]

                if size is None:
                    print("size is None", self.parent_gui)

                if hasattr(self.parent_gui, "getCanvas"):
                    size = self.parent_gui["canvasSize"]

                parent_width = size[1] - size[0]
                parent_height = size[3] - size[2]
            else:
                parent_width = 0
                parent_height = 0

        return parent_width, parent_height

    def update_text_pos(self):
        pass

    def get_gui_childrens(self) -> list:
        childs = self.children
        if hasattr(self, "getCanvas"):
            childs = self.getCanvas().children

        for child in childs:
            child_gui = child.getPythonTag("simple_gui")
            if child_gui is not None:
                yield child_gui

    def set_position(self):

        if self["layout"].startswith("BoxLayout"):
            self.apply_box_layout()
        elif self["layout"].startswith("GridLayout"):
            self.apply_grid_layout()

        x0, y0 = 0, 0
        x, y = self["position"]

        if self.parent_gui is None or self.parent_gui["layout"] == "FloatLayout":

            parent_width, parent_height = self.get_parent_size()

            if self["orginH"] is "left":
                x0 = 0
            elif self["orginH"] is "center":
                x0 = parent_width / 2
            elif self["orginH"] is "right":
                x0 = parent_width

            if self["orginV"] is "top":
                y0 = 0
            elif self["orginV"] is "middle":
                y0 = -parent_height / 2
            elif self["orginV"] is "bottom":
                y0 = -parent_height

        padding = self["padding"]

        self.setPos(x0 + x + padding[0], 0, y0 - y - padding[3])
        self.update_text_pos()

    def apply_box_layout(self):
        orientation = 0
        if self["layoutDir"].upper() == "X":
            orientation = 0
        elif self["layoutDir"].upper() == "Y":
            orientation = 1

        size = self["frameSize"]
        frame_size = [size[1] - size[0], size[3] - size[2]]
        total_len = frame_size[orientation]

        free_size_widgets = list()

        frame_pos = 0
        for child in self.get_gui_childrens():
            size = child.box_size()

            if child["size"] == [None, None] and child["sizeHint"] == [None, None]:
                print("free_size_widgets")
                free_size_widgets.append(child)
            else:
                frame_pos += size[orientation]

        free_space = max(total_len - frame_pos, 0) / max(len(free_size_widgets), 1)
        print(total_len, frame_pos, free_space)
        # if free_space > 0:

        free_space_hint = free_space / total_len
        for child in free_size_widgets:
            if orientation == 0:
                child.layout_size_hint = [free_space_hint, 1]
            else:
                child.layout_size_hint = [1, free_space_hint]

        frame_pos = 0
        for child in self.get_gui_childrens():
            size = child.box_size()
            pos = child["position"]
            if orientation == 0:
                child["position"] = [frame_pos, pos[1]]
            else:
                child["position"] = [pos[0], frame_pos]
            frame_pos += size[orientation]

    def apply_grid_layout(self):

        """('gridCols', 1, None),
        ('gridRows', 1, None),
        ('rowDefaultHeight', None, None),
        ('colDefaultWidth', None, None),
        ('colDefaultWidth', None, None),
        ('colsMinimum', {}, None),
        ('rowsMinimum', {}, None),"""

        orientation = 0
        index_one_limit = 1
        if self["layoutDir"].upper() == "X":
            orientation = 0
            index_one_limit = self["gridCols"]
        elif self["layoutDir"].upper() == "Y":
            orientation = 1
            index_one_limit = self["gridRows"]

        size = self["frameSize"]
        if hasattr(self, "getCanvas"):
            size = self["canvasSize"]
        frame_size = [size[1] - size[0], size[3] - size[2]]
        total_len = frame_size[orientation]

        free_size_widgets = list()
        frame_pos = 0

        cols_min_width = self["colsMinimum"]
        row_min_height = self["rowsMinimum"]

        # Determina el tamaño que debe tener como mínimo cada fila y cada columna
        index_h = 0
        index_v = 0

        for child in self.get_gui_childrens():
            size = child.box_size()

            if child["size"] == [None, None] and child["sizeHint"] == [None, None]:
                # Si el elemento hijo no tiene un tamaño predefinido, lo agrega a la lista de elementos con tamaño libre
                free_size_widgets.append(child)
                size = [0, 0]

            # Busca el elemento de mayor ancho en cada columna para determinar
            # el menor ancho que podrá contener a todos los elementos
            max_width = cols_min_width.get(index_h, 0)
            max_width = max(max_width, size[0])
            cols_min_width.update({index_h: max_width})

            # Busca el elemento de mayor altura en cada fila para determinar
            # la menor altura que podrá contener a todos los elementos
            max_height = row_min_height.get(index_v, 0)
            max_height = max(max_height, size[1])
            row_min_height.update({index_v: max_height})

            # Incrementa los índices horizontal y vertical según la orientacion de la grilla
            if orientation is 0:
                index_h += 1
                if index_h >= index_one_limit:
                    index_h = 0
                    index_v += 1
            elif orientation is 1:
                index_v += 1
                if index_v >= index_one_limit:
                    index_v = 0
                    index_h += 1

        width_filled = sum(cols_min_width.values())
        height_filled = sum(row_min_height.values())
        filled = [width_filled, height_filled][orientation]
        order = [cols_min_width, row_min_height][orientation]

        print("cols_min_width1", cols_min_width)
        print("row_min_height1", row_min_height)

        if order != {} and filled < total_len:
            free_space = total_len - filled

            count = list(order.values()).count(0)
            if count == 0:
                count = len(order.values())
                free_space /= count

                for index, value in order.items():
                    order[index] += free_space
            else:
                free_space /= count
                for index, value in order.items():
                    if value == 0:
                        order[index] += free_space

        print("cols_min_width2", cols_min_width)
        print("row_min_height2", row_min_height)



        frame_pos_a = 0
        frame_pos_b = 0
        index_a = 0
        index_b = 0
        for child in self.get_gui_childrens():

            if orientation == 0:

                child["position"] = [frame_pos_a, frame_pos_b]
                frame_pos_a += cols_min_width.get(index_a, 0)

                index_a += 1
                if index_a >= index_one_limit:
                    index_a = 0
                    frame_pos_a = 0
                    frame_pos_b += row_min_height.get(index_b, 0)
                    index_b += 1

            else:
                child["position"] = [frame_pos_b, frame_pos_a]
                frame_pos_a += row_min_height.get(index_a, 0)

                index_a += 1
                if index_a >= index_one_limit:
                    index_a = 0
                    frame_pos_a = 0
                    frame_pos_b += cols_min_width.get(index_b, 0)
                    index_b += 1

            frame_pos += size[orientation]



    def setFrameColor(self):
        # this might be a single color or a list of colors
        colors = self['frameColor']
        if isinstance(colors, str):
            colors = draw.get_color(colors, color_format="rgba", alpha=self["alpha"])
        elif isinstance(colors[0], str):
            for index, color in enumerate(colors):
                colors[index] = draw.get_color(color, color_format="rgba", alpha=self["alpha"])

        if type(colors[0]) == int or \
                type(colors[0]) == float:
            colors = (colors,)

        for i in range(self['numStates']):
            if i >= len(colors):
                color = colors[-1]
            else:
                color = colors[i]
            self.frameStyle[i].setColor(color[0], color[1], color[2], color[3])
        self.updateFrameStyle()

