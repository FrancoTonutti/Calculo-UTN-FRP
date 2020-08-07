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

from panda3d.core import *
from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectGuiBase import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenGeom import OnscreenGeom
from direct import directtools
from app.view import draw
from app import app
import sys

if sys.version_info >= (3, 0):
    stringType = str
else:
    stringType = basestring


class SimpleFrame(DirectGuiWidget):
    DefDynGroups = ('text', 'geom', 'image')

    def __init__(self, parent=None, **kw):

        # Inherits from DirectGuiWidget
        optiondefs = (
            # Define type of DirectGuiWidget
            ('pgFunc', PGItem, None),
            ('numStates', 1, None),
            ('state', self.inactiveInitState, None),
            # Frame can have:
            # A background texture
            ('image', None, self.set_image),
            # A midground geometry item
            ('geom', None, self.set_geom),
            # A foreground text node
            ('text', None, self.set_text),
            # Change default value of text mayChange flag from 0
            # (OnscreenText.py) to 1
            ('textMayChange', 1, None),
            ('frameColor', "C_CARROT", self.setFrameColor),
            ('position', [0, 0], self.set_position),
            ('size', [None, None], self.set_size),
            ('orginV', "top", self.set_position),
            ('orginH', "left", self.set_position),
            ('sizeHint', [None, None], self.set_size)
        )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs,
                           dynamicGroups=SimpleFrame.DefDynGroups)

        # Initialize superclasses
        if parent is None:
            parent = pixel2d

        DirectGuiWidget.__init__(self, parent)

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

    def set_size(self):
        width, height = self["size"]
        hint_x, hint_y = self["sizeHint"]

        if self.parent == pixel2d:
            parent_width = app.get_show_base().win.getXSize()
            parent_height = app.get_show_base().win.getYSize()
        else:
            #size = self.parent["frameSize"]
            size = None
            if size is not None:
                parent_width = size[1] - size[0]
                parent_height = size[3] - size[2]
            else:
                parent_width = 0
                parent_height = 0

        if hint_x is not None:
            width = parent_width * hint_x

        if hint_y is not None:
            height = parent_height * hint_y

        self["frameSize"] = (0, width, -height, 0)

        if hasattr(self, "text_pos"):
            txt_x, txt_y = self["text_pos"]
            size_x, size_y = self["text_scale"]
            if self["textCenterX"]:
                txt_x = width / 2
            if self["textCenterY"]:
                txt_y = -(height / 2 + size_y / 2)
            self["text_pos"] = (txt_x, txt_y)

    def set_position(self):
        if self.parent == pixel2d:
            frame_width = app.get_show_base().win.getXSize()
            frame_height = app.get_show_base().win.getYSize()

        else:
            print("self", type(self))
            print("parent", type(self.getParent()))
            print("children", type(self.parent.children.getPaths()[0]))
            #size = self.parent["frameSize"]
            #size = getattr(self.parent, "frameSize")
            size = None
            if size is not None:
                frame_width = size[1] - size[0]
                frame_height = size[3] - size[2]
            else:
                frame_width = 0
                frame_height = 0

        x0, y0 = 0, 0
        x, y = self["position"]

        if self["orginH"] is "left":
            x0 = 0
        elif self["orginH"] is "center":
            x0 = frame_width / 2
        elif self["orginH"] is "right":
            x0 = frame_width

        if self["orginV"] is "top":
            y0 = 0
        elif self["orginV"] is "middle":
            y0 = -frame_height / 2
        elif self["orginV"] is "bottom":
            y0 = -frame_height

        self.setPos(x0 + x, 0, y0 - y)
        # height = h2-h1
        # self["frameSize"] = (0, win_width, 0, -height)

    def set_color_string(self):
        col = draw.get_color(self["colorString"], color_format="rgba", alpha=self["alpha"])
        print("set_color_string",col)
        self["frameColor"] = col

    """ DEFAULT METHODS"""

    def setFrameColor(self):
        # this might be a single color or a list of colors
        colors = self['frameColor']
        if isinstance(colors, str):
            print("COLORS STRIGGG")
            colors = draw.get_color(colors, color_format="rgba")
        elif isinstance(colors[0], str):
            for index, color in enumerate(colors):
                colors[index] = draw.get_color(color, color_format="rgba")

        if type(colors[0]) == int or \
                type(colors[0]) == float:
            colors = (colors,)

        for i in range(self['numStates']):
            if i >= len(colors):
                color = colors[-1]
            else:
                color = colors[i]
            print("color", color)
            self.frameStyle[i].setColor(color[0], color[1], color[2], color[3])
        self.updateFrameStyle()

    def destroy(self):
        DirectGuiWidget.destroy(self)

    def clear_text(self):
        self['text'] = None
        self.set_text()

    def set_text(self, text=None):
        if text is not None:
            self['text'] = text

        # Determine if user passed in single string or a sequence
        if self['text'] is None:
            text_list = (None,) * self['numStates']
        elif isinstance(self['text'], stringType):
            # If just passing in a single string, make a tuple out of it
            text_list = (self['text'],) * self['numStates']
        else:
            # Otherwise, hope that the user has passed in a tuple/list
            text_list = self['text']
        # Create/destroy components
        for i in range(self['numStates']):
            component = 'text' + repr(i)
            # If fewer items specified than numStates,
            # just repeat last item
            try:
                text = text_list[i]
            except IndexError:
                text = text_list[-1]

            if self.hascomponent(component):
                if text is None:
                    # Destroy component
                    self.destroycomponent(component)
                else:
                    self[component + '_text'] = text
            else:
                if text is None:
                    return
                else:
                    from direct.gui.OnscreenText import OnscreenText
                    self.createcomponent(
                        component, (), 'text',
                        OnscreenText,
                        (), parent=self.stateNodePath[i],
                        text=text, scale=1, mayChange=self['textMayChange'],
                        sort=DGG.TEXT_SORT_INDEX,
                    )

    def clear_geom(self):
        self['geom'] = None
        self.set_geom()

    def set_geom(self, geom=None):
        if geom is not None:
            self['geom'] = geom

        # Determine argument type
        geom = self['geom']

        if geom is None:
            # Passed in None
            geom_list = (None,) * self['numStates']
        elif isinstance(geom, NodePath) or \
                isinstance(geom, stringType):
            # Passed in a single node path, make a tuple out of it
            geom_list = (geom,) * self['numStates']
        else:
            # Otherwise, hope that the user has passed in a tuple/list
            geom_list = geom

        # Create/destroy components
        for i in range(self['numStates']):
            component = 'geom' + repr(i)
            # If fewer items specified than numStates,
            # just repeat last item
            try:
                geom = geom_list[i]
            except IndexError:
                geom = geom_list[-1]

            if self.hascomponent(component):
                if geom is None:
                    # Destroy component
                    self.destroycomponent(component)
                else:
                    self[component + '_geom'] = geom
            else:
                if geom is None:
                    return
                else:
                    self.createcomponent(
                        component, (), 'geom',
                        OnscreenGeom,
                        (), parent=self.stateNodePath[i],
                        geom=geom, scale=1,
                        sort=DGG.GEOM_SORT_INDEX)

    def clear_image(self):
        self['image'] = None
        self.set_image()

    def set_image(self, image=None):
        if image is not None:
            self['image'] = image

        # Determine argument type
        arg = self['image']
        if arg is None:
            # Passed in None
            image_list = (None,) * self['numStates']
        elif isinstance(arg, NodePath) or \
                isinstance(arg, Texture) or \
                isinstance(arg, stringType):
            # Passed in a single node path, make a tuple out of it
            image_list = (arg,) * self['numStates']
        else:
            # Otherwise, hope that the user has passed in a tuple/list
            if ((len(arg) == 2) and
                    isinstance(arg[0], stringType) and
                    isinstance(arg[1], stringType)):
                # Its a model/node pair of strings
                image_list = (arg,) * self['numStates']
            else:
                # Assume its a list of node paths
                image_list = arg
        # Create/destroy components
        for i in range(self['numStates']):
            component = 'image' + repr(i)
            # If fewer items specified than numStates,
            # just repeat last item
            try:
                image = image_list[i]
            except IndexError:
                image = image_list[-1]

            if self.hascomponent(component):
                if image is None:
                    # Destroy component
                    self.destroycomponent(component)
                else:
                    self[component + '_image'] = image
            else:
                if image is None:
                    return
                else:
                    self.createcomponent(
                        component, (), 'image',
                        OnscreenImage,
                        (), parent=self.stateNodePath[i],
                        image=image, scale=1,
                        sort=DGG.IMAGE_SORT_INDEX)


