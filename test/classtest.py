"""
Esto es un archivo de testeo de ejemplo, no funciona actualmente

"""


class Base:
    def __init__(self):
        print("Base")


class Frame(Base):
    def __init__(self):
        print("Frame")
        Base.__init__(self)


class Button(Frame):
    def __init__(self):
        print("Button")
        Frame.__init__(self)

    def press(self):
        print("button pressed")


class Frame2(Frame):
    def __init__(self):
        print("Frame2")
        Frame.__init__(self)


class Button2(Button, Frame2):
    def __init__(self):
        print("Button")
        Button.__init__(self)
        Frame2.__init__(self)




a = Button2()

a.press()
