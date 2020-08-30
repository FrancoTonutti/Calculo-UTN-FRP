from app import app
from .layout_controller import Layout
from direct.showbase.DirectObject import DirectObject
from app.controller.console import execute
from app.view.simpleui.simple_entry import SimpleEntry
from app.view.simpleui.simple_label import SimpleLabel
from app.view.simpleui.simple_scrolled_frame import SimpleScrolledFrame
from panda3d.core import TextNode
from panda3d.core import WindowProperties
from direct.gui.DirectScrolledFrame import *

def execute_console(cmd):
    print(cmd)


class PropertiesEditor(DirectObject):
    def __init__(self, layout: Layout):
        self.frame = layout.prop_frame
        self.container = layout.work_container
        self.accept("control-1", self.toogle_show)

        entry = SimpleLabel(
            text_fg=(0, 0, 0, 1),
            orginV="bottom",
            position=[0, 0],
            text_scale=(12, 12),
            text="Propiedadades",
            parent=self.frame,
            size=[None, 20],
            sizeHint=[0.50, None],
            frameColor="C_WHITE",
            alpha=0,
            align="left",
            textCenterX=False,
            padding=[15, 0, 0, 0]

        )

        frame_scrolled = SimpleScrolledFrame(

            position=[0, 0],
            canvasSize=(0, 250-16, -500, 0),
            parent=self.frame,
            layout="GridLayout",
            layoutDir="X",
            gridCols=2,
            gridRows=2,
            frameColor="C_CARROT",
            alpha=0
        )

        canvas = frame_scrolled.getCanvas()


        entry = SimpleLabel(
            text_fg=(0, 0, 0, 1),
            orginV="bottom",
            position=[0, 0],
            text_scale=(12, 12),
            text="Prop",
            parent=frame_scrolled.getCanvas(),
            size=[None, 20],
            sizeHint=[0.50, None],
            frameColor="C_WHITE",
            align="left",
            textCenterX=False,
            padding=[15, 0, 0, 0]

        )
        entry = SimpleEntry(
            text_fg=(0, 0, 0, 1),
            orginH="center",
            position=[0, 0],
            text_scale=(12, 12),
            width=20,
            label="Ingrese un comando",
            command=execute_console,
            parent=frame_scrolled.getCanvas(),
            size=[None, 20],
            sizeHint=[0.50, None],
            frameColor="C_WHITE"

        )



        lb = SimpleLabel(text_fg=(0, 0, 0, 1),text="Prop", position=[0,0])
        label = SimpleLabel(
            text_fg=(0, 0, 0, 1),
            orginV="bottom",
            position=[0, 0],
            text_scale=(12, 12),
            text="Prop",
            parent=frame_scrolled.getCanvas(),
            size=[None, 20],
            sizeHint=[0.50, None],
            frameColor="C_CARROT",
            align="left",
            textCenterX=False,
            padding=[15, 0, 0, 0]
            )

        frame_scrolled = SimpleScrolledFrame(

            position=[400, 400],
            canvasSize=(0, 150, -1000, 0),
            layout="BoxLayout",
            layoutDir="Y",
            gridCols=2,
            gridRows=2,
            sizeHint=[0.25, 0.25],
            frameColor="C_CARROT",
            alpha=100
        )

        label = SimpleLabel(
            text_fg=(1, 0, 0, 1),
            orginV="bottom",
            position=[0, 0],
            text_scale=(12, 12),
            text="Prop",
            parent=frame_scrolled.getCanvas(),
            size=[50, 50],
            frameColor="C_CARROT",
            align="left",
            textCenterX=False,
            padding=[15, 0, 0, 0]
        )
        """SimpleFrame(position=[0, 0],
                    size=[250, 500],
                    sizeHint=[None, 1],
                    frameColor="C_NEPHRITIS",
                    layout="BoxLayout",
                    layoutDir="Y",
                    gridCols=2,
                    gridRows=2)"""
        #myframe = DirectScrolledFrame(canvasSize=(-2, 2, -2, 2), frameSize=(-.5, .5, -.5, .5))
        #myframe.setPos(0, 0, 0)

    def toogle_show(self):
        if self.frame.is_hidden():
            self.frame["size"] = [250, 500]
            self.frame.show()
        else:
            self.frame.hide()
            self.frame["size"] = [0, 500]

        execute("regen_ui")
