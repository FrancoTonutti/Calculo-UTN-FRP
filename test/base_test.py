from direct.gui.DirectButton import DirectButton
from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectOptionMenu import DirectOptionMenu
from direct.showbase.ShowBase import ShowBase

from app.view.simpleui import SimpleEntry


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        menu = DirectEntry(initialText="options", scale=15, parent=pixel2d, pos=(300,0,-400))
        menu = DirectButton(text="options2", scale=15,parent=pixel2d, pos=(300,0,-410))

        SimpleEntry()

app = MyApp()
app.run()
