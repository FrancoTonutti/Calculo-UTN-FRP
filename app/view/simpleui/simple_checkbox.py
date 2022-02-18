from direct.gui.DirectCheckBox import *
from app.view.simpleui.simple_frame import SimpleFrame
from app.view import draw
from panda3d.core import TextProperties
from direct.gui.DirectCheckButton import *


class SimpleCheckBox(SimpleFrame):
    def __init__(self, parent=None, **kw):

        self.circle = loader.loadModel("data/geom/square.egg")

        # self.circle.node().setAttrib(ShadeModelAttrib.make(ShadeModelAttrib.MSmooth))

        self.geom_load = [self.circle, None]

        optiondefs = (
            ('numStates', 2, None),
            ('state', DGG.NORMAL, None),
            ('relief', DGG.RAISED, None),
            ('invertedFrames', (1,), None),
            ('pressEffect', 1, DGG.INITOPT),
            ('geom', None, self.setGeom),
            ('value', False, self.update_check),
            ('command', False, None),
            ('extraArgs', [], None),
            ('maxSize', 400, None),
            ('focus', False, None),
            ('colorDisabled', (0, 0, 0, 1), self.set_checkbox_colors),
            ('colorEnabled', (1, 1, 1, 1), self.set_checkbox_colors),


        )
        if "geom_scale" not in kw:
            kw.update({"geom_scale": (50, 1, 50)})
        self.defineoptions(kw, optiondefs)

        SimpleFrame.__init__(self, parent)

        self.comp_frame = self.createcomponent("frame", (), None,
                                               SimpleFrame, (self,),
                                               numStates=1,
                                               geom=self.circle,
                                               geom_scale=(1, 1, 1)
                                               )



        self.comp_content = self.createcomponent("content", (), None,
                                                 SimpleFrame, (self,),
                                                 numStates=1,
                                                 geom=self.circle,
                                                 geom_scale=(1, 1, 1)
                                                 )


        self.initialiseoptions(SimpleCheckBox)
        self.bind(DGG.B1PRESS, self.toggle)

    def set_checkbox_colors(self):
        self.comp_content.setColorScale(self["colorDisabled"])
        self.comp_frame.setColorScale(self["colorEnabled"])


    def toggle(self, args):
        self['value'] = not self['value']

        if self['command']:
            # Pass any extra args to command
            #print("toggle", self['value'])
            self['command'](self['value'], *self['extraArgs'])

    def update_check(self):
        if self['value'] is True:
            self.comp_content.hide()
        else:
            self.comp_content.show()

    def set_size(self):
        super().set_size()

        width, height = self.box_size()

        check_size = min(width, height, self['maxSize'])
        self.comp_frame.setScale(check_size, 1, check_size)
        self.comp_content.setScale(check_size, 1, check_size)

        padding = self["padding"]

        self.comp_frame["position"] = [check_size/2+padding[0], height/2]
        self.comp_content["position"] = [check_size/2+padding[0], height / 2]

        #print("super().set_size()",  self.comp_frame.getScale())

