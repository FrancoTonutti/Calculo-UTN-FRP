from app.model.entity import Entity, register


class Material(Entity):
    def __init__(self, elastic_modulus):
        super().__init__()
        self.elastic_modulus = elastic_modulus
        register(self)

    def __str__(self):
        return "<class 'app.model.core.Material'>"