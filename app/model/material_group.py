from app.model.entity import Entity
from app import app

class MaterialGroup(Entity):

    @staticmethod
    def create_from_object(obj):
        entity_id = obj.get("entity_id")
        name = obj.get("name")

        MaterialGroup(name, entity_id)

    def __init__(self, name, set_id=None):
        super().__init__(set_id)

        self._name = "None"
        self.name = name

    def __str__(self):
        return "<class 'app.model.core.MaterialGroup'> :%s" % (self.name,)


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):

        panda3d = app.get_show_base()
        # Obtenemos el registro del modelo
        model_reg = app.model_reg
        entities = model_reg.find_entities("MaterialGroup")

        iterate = False

        i = 2

        for entity in entities:
            if entity is not self:
                if entity.name == value:
                    iterate = True

                    if not value[:-1].endswith("_copy"):
                        value += "_copy1"
                        i = 2
                    else:
                        i = int(value[-1])+1

        while iterate:
            iterate = False

            for entity in entities:
                if entity is not self:
                    if entity.name == value:
                        iterate = True
                        value = value[:-len(str(i-1))] + str(i)
                        i += 1
                        break

        self._name = value
