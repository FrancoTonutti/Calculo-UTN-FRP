from direct.gui.OnscreenGeom import OnscreenGeom
from direct.gui.OnscreenText import OnscreenText
from direct.showbase import ShowBaseGlobal

from app.view.simpleui import SimpleEntry, SimpleFrame, SimpleButton
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
        self.combo_box_init = False
        self.btn_rollover = None
        optiondefs = (
            # Define type of DirectGuiWidget
            ('options', [], self.update_options),
            ('dropdownColor', (1, 1, 1, 1), None),
            ('colorList', None, None)
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
        # self.onscreenText.removeNode()

        # Call option initialization function
        self.initialiseoptions(SimpleComboBox)
        self.set_position()

        self.initialized = True

        w, h = self.box_size()
        self.combo_box_symbol_0 = self.createcomponent(
            'text1', (), 'text1',
            OnscreenText,
            (), parent=self.stateNodePath[0],
            text='◄', scale=12, mayChange=1,
            sort=0,
            pos=(w - 20, -h / 2 - 4),
            fg=(1, 1, 1, 1)
        )

        '''geom = loader.loadModel("data/geom/square.egg")

        self.createcomponent(
            "component", (), "geom",
            OnscreenGeom,
            (), parent=self.stateNodePath[0],
            geom=geom, scale=(w, 1, -170), pos=(w/2, 0, -170/2-h),
            sort=DGG.GEOM_SORT_INDEX)'''

        if self["options"]:
            n = len(self["options"])
        else:
            n = 1

        self.dropdown_frame = SimpleFrame(position=[2, h + 2],
                                          size=[w - 4, h*n],
                                          parent=self,#.stateNodePath[0],
                                          frameColor=self["dropdownColor"],
                                          padding=[1, 0, 0, 0],
                                          alpha=1,
                                          layout="BoxLayout",
                                          layoutDir="Y",
                                          sortOrder=1000
                                          )



        self.combo_box_symbol_1 = self.createcomponent(
            'text1', (), 'text1',
            OnscreenText,
            (), parent=self.stateNodePath[1],
            text='▼', scale=12, mayChange=1,
            sort=100,
            pos=(w - 20, -h / 2 - 4),
            fg=(1, 1, 1, 1)
        )
        self.btn_list = list()
        self.combo_box_init = True
        self.set_size()
        self.update_options()

        self.dropdown_frame.hide()


    def set_size(self):
        super(SimpleComboBox, self).set_size()

        if self.combo_box_init:
            w, h = self.box_size()

            self.combo_box_symbol_0["pos"] = (w - 20, -h / 2 - 4)
            self.combo_box_symbol_1["pos"] = (w - 20, -h / 2 - 4)

    def update_options(self):
        if self.combo_box_init:
            options = self["options"]
            w, h = self.box_size()
            text_comp = self.component("text")
            fg = text_comp.textNode.getTextColor()
            for option in options:
                new_btn = SimpleButton(text=str(option),
                                       text_scale=(12, 12),
                                       #text_font=font_panda3d,
                                       text_fg=fg,
                                       command=self.set_option,
                                       parent=self.dropdown_frame,
                                       extraArgs=[option],
                                       colorList=self["colorList"],
                                       #position=[0, 0],
                                       #padding=padding,
                                       size=[None, h],
                                       sizeHint=[1, None]
                                       #margin=margin
                                       )

                self.btn_list.append(new_btn)

            self.dropdown_frame.update_layout()

    def on_defocus(self, event=None):
        super(SimpleComboBox, self).on_defocus(event)

        for btn in self.btn_list:

            if btn.is_rollover:
                self.btn_rollover = btn
                break

        else:
            if self.dropdown_frame:

                self.dropdown_frame.hide()

    def on_focus(self, event=None):

        self.btn_rollover = False
        self.dropdown_frame.show()
        super(SimpleComboBox, self).on_focus(event)


    def set_option(self, value):
        print("SET_OPTION", value)
        self.enter_value(value)
        self.commandFunc(None)
        if self.btn_rollover:
            pass
            self.btn_rollover.on_leave(None)
        print(type(self.dropdown_frame))
        #self.dropdown_frame.hide()

    def focusOutCommandFunc(self):
        for btn in self.btn_list:

            if btn.is_rollover:
                self.btn_rollover = btn
                break
        else:
            super(SimpleComboBox, self).focusOutCommandFunc()

