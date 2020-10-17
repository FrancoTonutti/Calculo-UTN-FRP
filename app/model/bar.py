from app.model.entity import Entity, register


class Bar(Entity):

    def __init__(self, start, end, section, material=None):
        super().__init__()
        self.name = ""
        self.start = start
        self.end = end
        self.section = section
        self.material = material
        self._width = 0.2
        self._height = 0.3

        self.show_properties("name", "width", "height")

        self.show_properties("start_x", "start_y", "start_z")
        self.set_prop_name(start_x="Incio x", start_y="Incio y", start_z="Incio z")
        self.show_properties("end_x", "end_y", "end_z")
        self.set_prop_name(end_x="Fin x", end_y="Fin y", end_z="Fin z")
        register(self)

    def __str__(self):
        if self.name is "":
            name_start = self.start.name
            name_end = self.end.name

            if name_start is not "" and name_end is not "":
                name = "Barra {}-{}".format(name_start, name_end)
            else:
                name = None
        else:
            name = "Barra {}".format(self.name)

        if name is None:
            return super().__str__()
        else:
            return name



    @property
    def width(self):
        return self.section.size[0]

    @width.setter
    def width(self, value):
        print("setter width")
        self.section.size[0] = value

    @property
    def height(self):
        return self.section.size[1]

    @height.setter
    def height(self, value):
        print("setter height")
        self.section.size[1] = value

    @property
    def start_x(self):
        return self.start.x

    @start_x.setter
    def start_x(self, value: str):
        self.start.x = value

    @property
    def start_y(self):
        return self.start.y

    @start_y.setter
    def start_y(self, value: str):
        self.start.y = value

    @property
    def start_z(self):
        return self.start.z

    @start_z.setter
    def start_z(self, value: str):
        self.start.z = value

    @property
    def end_x(self):
        return self.end.x

    @end_x.setter
    def end_x(self, value: str):
        self.end.x = value

    @property
    def end_y(self):
        return self.end.y

    @end_y.setter
    def end_y(self, value: str):
        self.end.y = value

    @property
    def end_z(self):
        return self.end.z

    @end_z.setter
    def end_z(self, value: str):
        self.end.z = value