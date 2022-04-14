from app.model import Entity


class ProfileShapeFillRect(Entity):
    @staticmethod
    def create_from_object(obj):
        entity_id = obj.get("entity_id")

        return ProfileShapeFillRect(entity_id)

    def __init__(self, set_id=None):
        super(ProfileShapeFillRect, self).__init__(set_id)
        self.name = "Sección rectangular"
        self.params = ["bw", "h"]

    def __str__(self):
        return self.name

