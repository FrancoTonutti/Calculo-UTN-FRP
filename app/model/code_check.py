from app.model.entity import Entity
from typing import TYPE_CHECKING
from typing import List
from app import app

if TYPE_CHECKING:
    # Imports only for IDE type hints
    from app.model import *


class CodeCheck(Entity):

    @staticmethod
    def create_from_object(obj):
        pass

    def __init__(self, set_id=None):
        super().__init__(set_id)
        self.name = None

    def verify_beam(self, element):
        pass
