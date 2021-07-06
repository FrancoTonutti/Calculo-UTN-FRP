from app import app
import json
from app.model.entity import Entity

primitive = (int, str, bool, float)
class_register = {}


def is_primitive(thing):
    return isinstance(thing, primitive)


class ModelReg(dict):
    def __init__(self):
        super().__init__()

        self.entity_register = dict()

    def get_all_bars(self):
        return self.get("Bar", {})

    def get_bars(self):
        if "Bar" in self:
            for model_id in self["Bar"]:
                yield self["Bar"][model_id]
        else:
            yield list()

    def get_bar_count(self):
        return len(self["Bar"])

    def get_nodes(self):
        if "Node" in self:
            for model_id in self["Node"]:
                yield self["Node"][model_id]
        else:
            yield list()

    def get_node_count(self):
        return len(self["Node"])

    def clear(self):
        keys = list(self.keys())

        self.entity_register.clear()

        for key in keys:
            if key != "ViewGizmoZone":
                self.pop(key, None)

    def get_entity(self, entity_id):
        if isinstance(entity_id, str):
            return self.entity_register.get(entity_id)
        else:
            return entity_id

    def toJSON(self):
        dict_data = dict()

        exclude_attrs = ["geom", "_geom", "is_editable", "is_selectable", "is_selected", "ifc_entity"]

        for key in self.keys():
            dict_data.update({key: dict()})
            subdict_data = dict_data.get(key)

            for model_id in self[key]:
                entity = self[key][model_id]

                entity_dict = dict()

                entity_attrs = [a for a in dir(entity) if not a.startswith('_') and not callable(getattr(entity, a))]

                for attr in entity_attrs:
                    if attr in exclude_attrs:
                        continue

                    value = getattr(entity, attr)

                    value = convert_value(value)

                    entity_dict.update({attr: value})

                subdict_data.update({model_id: entity_dict})

        return json.dumps(dict_data, sort_keys=True, indent=4)


    def from_JSON(self, json_string: str):

        dict_data = json.loads(json_string)

        keys_priority = ["View", "Node", "Section", "Material", "Bar", "Load"]

        for key in dict_data.keys():
            if key not in keys_priority:
                keys_priority.append(key)

        for key in keys_priority:
            print("start load {}".format(key))
            i=0
            for entity_id, entity_data in dict_data[key].items():
                class_obj = class_register.get(key)

                if class_obj is None:
                    raise Exception(key)
                else:
                    class_obj.create_from_object(entity_data)
                    i +=1
            print("loaded {} {}".format(i, key))


from numpy import ndarray

def convert_value(value):
    if isinstance(value, Entity):
        value = value.entity_id
    else:
        if not is_primitive(value):
            if isinstance(value, list):
                new_list = list()
                for elem in value:
                    new_list.append(convert_value(elem))
                value = new_list
            elif isinstance(value, dict):
                new_dict = dict()
                for key, elem in value.items():
                    new_dict.update({key: convert_value(elem)})
                value = new_dict
            elif isinstance(value, ndarray):
                value = value.tolist()
            else:
                value = type(value).__name__

    return value




app.model_reg = ModelReg()


