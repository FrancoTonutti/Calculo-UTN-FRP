from app.model.entity import Entity, register


class ProfileSection(Entity):
    _section_props = dict()

    @staticmethod
    def create_from_object(obj):
        pass

    def __init__(self, set_id=None):
        super().__init__(set_id)


    def inertia_x(self):
        pass

    def inertia_y(self):
        pass

    def area(self):
        pass

    def __str__(self):
        return "<class 'app.model.core.Section'>"
