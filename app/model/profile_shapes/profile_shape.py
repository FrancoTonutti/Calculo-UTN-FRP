from app import app
from app.model import Entity, unit_manager


class ProfileShape(Entity):
    @staticmethod
    def create_from_object(obj):
        entity_id = obj.get("entity_id")

        shape = ProfileShape(entity_id)

        return shape

    def __init__(self, set_id=None):
        super(ProfileShape, self).__init__(set_id)
        self.name = "Generic Shape"
        self.params = []
        self.is_clockwise = False

    def __str__(self):
        return self.name

    @staticmethod
    def get_contour_points(*args):
        pass

