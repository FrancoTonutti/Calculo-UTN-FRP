from app.model import Entity


class ProfileShapeI(Entity):
    @staticmethod
    def create_from_object(obj):
        entity_id = obj.get("entity_id")

        return ProfileShapeI(entity_id)

    def __init__(self, set_id=None):
        super(ProfileShapeI, self).__init__(set_id)
        self.name = "Sección doble T"
        self.params = ["d", "bf", "tf", "hw", "tw", "r1", "r2"]

    def __str__(self):
        return self.name

