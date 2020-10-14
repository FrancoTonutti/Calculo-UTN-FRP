from app.model.entity import Entity,register


class Section(Entity):
    def __init__(self, width, height):
        super().__init__()
        self.size = [width, height]
        register(self)

    def __str__(self):
        return "<class 'app.model.core.Section'>"
