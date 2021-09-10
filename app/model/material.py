from app.model.entity import Entity


class Material(Entity):

    @staticmethod
    def create_from_object(obj):
        entity_id = obj.get("entity_id")
        elastic_modulus = obj.get("elastic_modulus")

        Material(elastic_modulus, entity_id)

    def __init__(self, elastic_modulus, set_id=None):
        super().__init__(set_id)
        self.elastic_modulus = elastic_modulus

    def __str__(self):
        return "<class 'app.model.core.Material'>"