from app.model.entity import Entity, register


class Section(Entity):

    @staticmethod
    def create_from_object(obj):
        entity_id = obj.get("entity_id")
        width, height = obj.get("size")

        return Section(width, height, entity_id)

    def __init__(self, width, height, set_id=None):
        super().__init__(set_id)
        self.size = [width, height]
        register(self)

    def inertia_x(self):
        b = self.size[0]
        h = self.size[1]
        return (b * pow(h, 3)) / 12

    def inertia_y(self):
        b = self.size[0]
        h = self.size[1]
        return (h * pow(b, 3)) / 12

    def area(self):
        return self.size[0] * self.size[1]

    def __str__(self):
        return "<class 'app.model.core.Section'>"
