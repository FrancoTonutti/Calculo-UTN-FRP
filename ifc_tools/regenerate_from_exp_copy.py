import ifc_tools
import os
import re
from ifcopenshell import validate

IFC_PATH = os.path.dirname(ifc_tools.__file__)

IDEN_1 = " " * 4
IDEN_2 = " " * 8

SCHEMA_FILE = "IFC4x1.exp"
snake_case_pattern = re.compile(r'(?<!^)(?=[A-Z])')

ifc_types = dict()



def load_exp_data():
    file = open(os.path.join(IFC_PATH, SCHEMA_FILE), 'r')
    data = file.read()
    file.close()
    lines = data.split("\n")
    for line in lines:

        if line.startswith("TYPE"):
            line = line.replace('TYPE ', '')
            line = line.replace(' = ', ' ')
            name_camel_case, python_type = line.split(" ", maxsplit=1)
            name_snake_case = snake_case_pattern.sub('_', name_camel_case).lower()
            python_type = python_type.replace(";", "").lower()

            if python_type in validate.simple_type_python_mapping:
                python_type = validate.simple_type_python_mapping.get(python_type).__name__
            elif "list" in python_type:
                python_type = "list"
            else:
                python_type = ""

            if python_type == "bool":
                python_type = ""

            print("TYPE: %s (%s)" % (name_camel_case, python_type))
            ifc_types.update({name_camel_case: {"name_camel_case": name_camel_case,
                                                "name_snake_case": name_snake_case,
                                                "python_type": python_type}})


def generate_ifc_types():
    file_string = ""

    for key, entity in ifc_types.items():
        file_string += "class {}".format(entity.get("name_camel_case"))
        if entity.get("python_type") is not "":
            file_string += "({})".format(entity.get("python_type"))
        file_string += ":\n"
        file_string += IDEN_1 + "pass\n"
        file_string += "\n\n"

    #print(file_string)
    f = open("ifc_types.py", "w", encoding='utf8')
    f.write(file_string)
    f.close()


if __name__ == "__main__":
    load_exp_data()
    generate_ifc_types()
