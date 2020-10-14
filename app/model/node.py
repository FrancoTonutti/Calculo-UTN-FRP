from app.model.entity import Entity, register


class Node(Entity):
    def __init__(self, x, y, z=0, name=""):
        super().__init__()
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.name = name
        self.hide_properties("position")
        self.set_prop_name()
        self.show_properties("name", "x", "y", "z")

        self.fixed_ux = False
        self.fixed_uy = False
        self.fixed_uz = False

        self.fixed_rx = False
        self.fixed_ry = False
        self.fixed_rz = False

        self.show_properties("fixed_ux", "fixed_uz", "fixed_ry")

        register(self)

    def __str__(self):
        name = str(self.name)
        x = round(self.position[0], 2)
        y = round(self.position[1], 2)
        z = round(self.position[2], 2)
        return "Nodo {} ({}, {}, {})".format(name, x, y, z)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, val):
        self.__x = round(float(val), 2)

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, val):
        self.__y = round(float(val), 2)

    @property
    def z(self):
        return self.__z

    @z.setter
    def z(self, val):
        self.__z = round(float(val), 2)

    @property
    def position(self):
        return [self.x, self.y, self.z]

    @position.setter
    def position(self, value: list):
        if isinstance(value, list) and len(value) == 3:
            x, y, z = value
            self.x = x
            self.y = y
            self.z = z

    @property
    def position_str(self):
        x, y, z = self.position
        x = round(x, 2)
        y = round(y, 2)
        z = round(z, 2)

        return "{}, {}, {}".format(x, y, z)

    @position_str.setter
    def position_str(self, value: str):
        value = value.split(",", 3)
        if len(value) is 3:
            x, y, z = value
            x = float(x)
            y = float(y)
            z = float(z)
            self.position = [x, y, z]

    def get_restrictions(self):
        restrictions = [self.fixed_ux,
                        self.fixed_uy,
                        self.fixed_uz,
                        self.fixed_rx,
                        self.fixed_ry,
                        self.fixed_rz]

        return restrictions

    def get_restrictions2d(self):
        restrictions = [self.fixed_ux,
                        self.fixed_uz,
                        self.fixed_ry]

        return restrictions
