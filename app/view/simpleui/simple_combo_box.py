from direct.gui.OnscreenText import OnscreenText
from direct.showbase import ShowBaseGlobal

from app.view.simpleui import SimpleEntry
from app.view import draw
from panda3d.core import TextProperties, TextPropertiesManager, TextNode
from direct.gui import DirectGuiGlobals as DGG



class SimpleComboBox(SimpleEntry):
    """
    label = None
    textCenterX = True
    textCenterY = True
    align = "center"  # "left" or "right"
    fontSize = 12
    """
    def __init__(self, parent=None, **kw):
        self.initialized2 = False
        optiondefs = (
            # Define type of DirectGuiWidget
            ('options', [], None),
        )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        if parent is None:
            parent = pixel2d

        SimpleEntry.__init__(self, parent, override_default=True)

        self["text_font"] = draw.draw_get_font()[0]

        if self['entryFont'] == None:
            font = DGG.getDefaultFont()
        else:
            font = self['entryFont']



        # We can get rid of the node path since we're just using the
        # onscreenText as an easy way to access a text node as a
        # component
        #self.onscreenText.removeNode()



        # Call option initialization function
        self.initialiseoptions(SimpleComboBox)
        self.set_position()

        self.initialized = True
        self.set_size()



        """self.combo_box_symbol = self.createcomponent(
            'text1', (), 'text1',
            OnscreenText,
            (),
            text='AASDAA', scale=1, mayChange=self['textMayChange'],
            sort=DGG.TEXT_SORT_INDEX,
            pos=(0,0),
            fg=(1,0,0,1)
        )"""

