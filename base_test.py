from direct.gui.DirectButton import DirectButton
from direct.gui.DirectEntry import DirectEntry
from direct.showbase.ShowBase import ShowBase

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        a = DirectEntry(initialText="back1", scale=15, parent=pixel2d, pos=(300,0,-400),frameColor=(0,1,0,1))
        b = DirectEntry(initialText="back2", scale=15, parent=pixel2d, pos=(300, 0, -420),frameColor=(1,0,0,1))
        c = DirectButton(text="front", scale=2, parent=a, pos=(10,-1,-0.75), sortOrder=100)
        c.setBin("gui-popup", 50)

app = MyApp()
app.run()
