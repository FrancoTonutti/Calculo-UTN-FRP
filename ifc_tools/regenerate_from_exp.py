import ifc_tools
import os
import re
from ifcopenshell import validate

import utils

IFC_PATH = os.path.dirname(ifc_tools.__file__)

IDEN_1 = " " * 4
IDEN_2 = " " * 8

SCHEMA_FILE = "IFC4x1.exp"
snake_case_pattern = re.compile(r'(?<!^)(?=[A-Z])')

ifc_types = dict()

exp_schema = utils.parse_exp(os.path.join(IFC_PATH, SCHEMA_FILE))


def to_snake_case(string):
    return snake_case_pattern.sub('_', string).lower()


def convert_to_python_type(string):
    if string.lower() in validate.simple_type_python_mapping:
        string = validate.simple_type_python_mapping.get(string.lower()).__name__
    elif "list" in string.lower():
        string = "list"
    elif "ENUM" in string:
        string = "Enum"

    if string == "bool":
        string = ""

    return string

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
    file_string = "from enum import Enum\n\n"
    types_file_data = utils.FileData()
    types_file_data.add_import("Enum", "enum")


    ifc_types = exp_schema.get("types")

    for key, ifc_type in ifc_types.items():
        t_name = ifc_type.get("name")
        file_string += "class {}".format(t_name)
        python_type = convert_to_python_type(ifc_type.get("type"))
        if python_type is not "":
            file_string += "({})".format(python_type)
        file_string += ":\n"
        file_string += IDEN_1 + "pass\n"
        file_string += "\n\n"

        new_class = utils.ClassFileData(t_name)
        if python_type is not "":
            new_class.subclass_of = python_type

        types_file_data.add_class(new_class)

    #print(file_string)
    f = open("ifc_types.py", "w", encoding='utf8')
    f.write(file_string)
    f.close()


if __name__ == "__main__":
    load_exp_data()
    generate_ifc_types()
