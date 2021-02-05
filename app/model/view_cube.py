from app.model.entity import Entity, register
from app import app


class ViewCube(Entity):
    def __init__(self):
        super().__init__()
        self.is_editable = False
        register(self)

    def set_geom(self, node):
        self.geom = [None, None]
        self.geom[0] = node
        node.setTag('entity_type', self.__class__.__name__)
        node.setTag('entity_id', self.entity_id)
