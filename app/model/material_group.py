from app.model.entity import Entity


class MaterialGroup(Entity):

    @staticmethod
    def create_from_object(obj):
        entity_id = obj.get("entity_id")
        name = obj.get("name")

        MaterialGroup(name, entity_id)

    def __init__(self, name, set_id=None):
        super().__init__(set_id)

        self.name = name

    def __str__(self):
        return "<class 'app.model.core.MaterialGroup'> :%s" % (self.name,)
