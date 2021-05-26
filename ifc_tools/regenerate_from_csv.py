import csv
import ifcopenshell
import os
import re
import xml
from ifcopenshell import validate
#import ifc_tools

import pprint

# print(ifcopenshell.__file__)

# print(os.path.dirname(ifcopenshell.__file__))

IFC_PATH = os.path.dirname(ifcopenshell.__file__)

CSV_PATH = os.path.join(IFC_PATH, 'express')

IFC_TOOLS_PATH = os.path.dirname(__file__)
# print(IFC_TOOLS_PATH)
SCHEMA_FILE = "IFC4x1.exp"

snake_case_pattern = re.compile(r'(?<!^)(?=[A-Z])')
cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

INDEN_1 = " " * 4
INDEN_2 = " " * 8

PEP8_MAX_LENGTH = 79

attr_dict = dict()
entity_dict = dict()
entity_identifier_dict = dict()
types_dict = dict()


def to_snake_case(camel: str) -> str:
    snake_case = snake_case_pattern.sub('_', camel).lower()
    snake_case = snake_case.replace("2_d", "_2d")
    snake_case = snake_case.replace("3_d", "_3d")
    return snake_case


def clean_description(desc: str, indentation="") -> str:
    desc_clean = re.sub(cleanr, '', desc)

    desc_clean = desc_clean.replace("\n\n", "\n", -1)
    desc_clean = desc_clean.replace("  ", " ", -1)
    desc_clean = desc_clean.replace("\n", "\n        ", -1)
    # Replace all tabulations
    desc_clean = desc_clean.replace("\t", "", -1)
    desc_clean = desc_clean.replace("NOTE ", "NOTE: ", -1)
    desc_clean = desc_clean.replace("HISTORY ", "HISTORY: ", -1)
    desc_clean = desc_clean.replace("SELF\\", "self.", -1)
    desc_clean = desc_clean.replace("\\", ".", -1)

    while desc_clean.startswith((" ", "\n")):
        desc_clean = desc_clean[1:]

    desc_clean = " " * 8 + desc_clean

    while desc_clean.endswith((" ", "\n")):
        desc_clean = desc_clean[:-1]

    desc_clean = fix_pep8_max_lenght(desc_clean)

    desc_clean = re.sub(cleanr, '', desc_clean)






    '''desc_lines = desc_clean.split("\n")

    new_lines = list()

    for line in desc_lines:

        if len(line) > PEP8_MAX_LENGTH:
            # print("split line")
            words = line.split(" ")
            line_len = 0
            new_words = list()
            for word in words:
                if line_len + 1 + len(word) > PEP8_MAX_LENGTH:
                    word = "\n" + INDEN_2 + word
                    line_len = len(word)
                else:
                    line_len += len(word)

                new_words.append(word)
                # print("line_len %s " % line_len)

            new_lines.append(" ".join(new_words))
        else:
            new_lines.append(line)

    desc_clean = "\n".join(new_lines)'''

    return desc_clean


def fix_pep8_max_lenght(string, identation=8, max_lenght=PEP8_MAX_LENGTH, min_identation=12, is_function=False):
    lines = string.split("\n")
    new_lines = list()
    break_char = " "

    for line in lines:

        if len(line) > max_lenght:
            # print("split line")
            words = line.split(" ")
            line_len = 0
            new_words = list()
            this_line = ""
            i = 0
            while i < len(words):
                word = words[i]
                #if line_len + 1 + len(word) > PEP8_MAX_LENGTH and break_char not in word:
                if len(this_line) + 1 + len(word) > PEP8_MAX_LENGTH and break_char not in word:
                    #if is_function -> "(" not in word or not is_function

                    # print("Line:{}:{}: {}".format(len(this_line), "\n" in this_line, this_line ))
                    this_line = " "

                    word = "\n" + " " * identation + word
                    line_len = len(word)
                    if (len(word) > PEP8_MAX_LENGTH and identation > min_identation) or (is_function and "(" in word):
                        # Restart the while loop
                        line_len = 0
                        new_words = list()
                        i = 0
                        identation = min_identation
                        if is_function:
                            break_char = "("
                        continue

                elif break_char in word:
                    break_pos = word.find(break_char)
                    word_a = word[0:break_pos+1]
                    if len(word)-1 > break_pos:
                        word_b = word[break_pos+1:len(word)]
                    else:
                        word_b = ""
                    line_len += len(word_a)
                    new_words.append(word_a)
                    # print("Line:{}:{}: {}".format(len(this_line), "\n" in this_line, this_line ))
                    this_line = " "
                    word = "\n" + " " * identation + word_b
                    line_len = len(word)
                else:
                    line_len += len(word)

                new_words.append(word)
                this_line += word.replace("\n", "") + " "
                i += 1
                # print("line_len %s " % line_len)

            new_lines.append(" ".join(new_words))
        else:
            new_lines.append(line)

    return "\n".join(new_lines)


def load_csv_data():
    with open(os.path.join(CSV_PATH, 'DocAttribute.csv')) as File:
        reader = csv.reader(File, delimiter=";")
        for identifier, name_camel_case, description in reader:
            name_snake_case = to_snake_case(name_camel_case)

            attr_dict.update({identifier:
                              {"name_camel_case": name_camel_case,
                               "name_snake_case": name_snake_case,
                               "description": description}})

    with open(os.path.join(CSV_PATH, 'DocEntity.csv')) as File:
        reader = csv.reader(File, delimiter=";")
        for identifier, name_camel_case, description in reader:
            name_snake_case = to_snake_case(name_camel_case)

            description = clean_description(description, indentation=INDEN_2)

            entity_dict.update({identifier:
                                   {"name_camel_case": name_camel_case,
                                    "name_snake_case": name_snake_case,
                                    "description": description,
                                    "attr_camel_case": [],
                                    "attr_snake_case": []}
                               })
            entity_identifier_dict.update({name_camel_case:identifier})
            
            # print(description)
    with open(os.path.join(CSV_PATH, 'DocEntityAttributes.csv')) as File:
        reader = csv.reader(File, delimiter=";")
        for identifier, index, attr_id in reader:
            entity = entity_dict.get(identifier)
            attr = attr_dict.get(attr_id)
            entity.get("attr_camel_case").append(attr.get("name_camel_case"))
            entity.get("attr_snake_case").append(attr.get("name_snake_case"))


entity_names_list = list()


def load_exp_data():
    file = open(os.path.join(IFC_TOOLS_PATH, SCHEMA_FILE), 'r')
    data = file.read()
    file.close()
    lines = data.split("\n")
    context = ["", ""]
    for line in lines:

        if line.startswith("TYPE"):
            line = line.replace('TYPE ', '')
            line = line.replace(' = ', ' ')
            name_camel_case, python_type = line.split(" ", maxsplit=1)

            if "(" in name_camel_case:
                continue

            name_snake_case = to_snake_case(name_camel_case)
            python_type = python_type.replace(";", "").lower()

            if python_type in validate.simple_type_python_mapping:
                python_type = validate.simple_type_python_mapping.get(python_type).__name__
            elif "list" in python_type:
                python_type = "list"
            else:
                python_type = ""

            if python_type == "bool":
                python_type = ""

            # print("TYPE: %s (%s)" % (name_camel_case, python_type))
            types_dict.update({name_camel_case: {"name_camel_case": name_camel_case,
                                                 "name_snake_case": name_snake_case,
                                                 "python_type": python_type}})

        if line.startswith("ENTITY"):
            # print("ENTITY")
            context[0] = "ENTITY"
            line = line.replace("ENTITY ", "")
            line = line.replace(";", "", -1)
            context[1] = line
            entity_names_list.insert(0, context[1])

            identifier = entity_identifier_dict.get(context[1])
            entity = entity_dict.get(identifier)
            if entity is None:
                name_camel_case = context[1]
                name_snake_case = to_snake_case(name_camel_case)
                entity_dict.update({name_camel_case: {"name_camel_case": name_camel_case,
                                                      "name_snake_case": name_snake_case,
                                                      "description": "",
                                                      "attr_camel_case": [],
                                                      "attr_snake_case": []}
                                    })
                entity_identifier_dict.update({name_camel_case: name_camel_case})

        if line.startswith("END_ENTITY"):
            # print("END_ENTITY")
            context[0] = ""
            context[1] = ""


        if context[0] == "SUPERTYPE":
            identifier = entity_identifier_dict.get(context[1])
            entity = entity_dict.get(identifier)
            subclasses = entity.get("subclasses", [])

            subclass = line.replace('(', '')
            subclass = subclass.replace(',', '')
            subclass = subclass.replace(')', '', -1)
            subclass = subclass.replace(' ', '', -1)
            subclass = subclass.replace(';', '', -1)
            subclasses.append(subclass)

            entity.update({"subclasses": subclasses})



            if "))" in line:
                context[0] = "ENTITY"

        elif context[0] == "ENTITY":
            if "SUPERTYPE" in line:
                context[0] = "SUPERTYPE"
            elif line.startswith(" SUBTYPE"):
                line = line.replace(' SUBTYPE OF (', '')
                line = line.replace(');', '')

                base_class = line
                # print(base_class)

                identifier = entity_identifier_dict.get(context[1])
                entity = entity_dict.get(identifier)
                if entity is not None:
                    entity.update({"base_class": base_class})
                    # print("base_class")
                    # print(entity)
                else:
                    pass
                    # print("error")
            else:
                print(line)

entity_tree = dict()
entity_tree_list = list()

def read_ifc_entity_tree():
    # print("read_ifc_entity_tree")
    for entity_name in entity_names_list:

        key = entity_identifier_dict.get(entity_name)
        entity = entity_dict.get(key)

        if entity.get("base_class") is None:
            # print(entity)
            test = ifc_tree_find(entity.get("name_camel_case"), entity_tree)



    # pprint.pprint(entity_tree)
    create_entity_tree_list(entity_tree)
    # print(entity_tree_list)


def ifc_tree_find(entity_name, tree):
    tree.update({entity_name: {}})
    sub_tree = tree.get(entity_name)

    key = entity_identifier_dict.get(entity_name)
    entity = entity_dict.get(key)
    if entity:
        subclasses = entity.get("subclasses", [])

        for child in subclasses:
            sub_tree.update({child: ""})
            ifc_tree_find(child, sub_tree)

    return tree





def create_entity_tree_list(tree):

    for key in tree:
        entity_tree_list.append(key)
        create_entity_tree_list(tree[key])





                


def generate_ifc_file():
    ifc_file_string = ""
    ifc_file_string += "from ifcopenshell.file import file\n"
    ifc_file_string += "# noinspection PyUnresolvedReferences\n"
    ifc_file_string += "from ifc_entities import *\n\n\n"
    ifc_file_string += "class IfcFile(file):\n\n"
    ifc_file_string += INDEN_1 + "def __init__(self, f=None, schema=None):\n"
    ifc_file_string += INDEN_2 + "super().__init__(f, schema)\n\n"

    for key, entity in entity_dict.items():

        attrs = [attr+"=None" for attr in entity.get("attr_snake_case")]
        attr_string = ", ".join(attrs)
        function_name = INDEN_1 + "def create_{}(".format(entity.get("name_snake_case"))
        function_definition = function_name + "self, {}):\n".format(attr_string)

        ifc_file_string += fix_pep8_max_lenght(function_definition,
                                               identation=len(function_name),
                                               is_function=True,
                                               min_identation=12)

        ifc_file_string += INDEN_2 + '"""\n{}\n\n'.format(entity.get("description"))

        ifc_file_string += INDEN_2 + "Parameters\n"
        ifc_file_string += INDEN_2 + "-------\n"

        for attr in entity.get("attr_snake_case"):
            ifc_file_string += INDEN_2 + attr + "\n"

        ifc_file_string += "\n"
        ifc_file_string += INDEN_2 + "Returns\n"
        ifc_file_string += INDEN_2 + "-------\n"

        ifc_file_string += INDEN_2 + "{}\n".format(entity.get("name_camel_case"))

        ifc_file_string += INDEN_2 + '"""\n\n'


        attr_string = ", ".join(entity.get("attr_snake_case"))
        function_name = INDEN_2 + "return%self.create{}(".format(entity.get("name_camel_case"))
        function_return = function_name + "{})\n\n".format(attr_string)
        string_fixed = fix_pep8_max_lenght(function_return,
                                           identation=len(function_name),
                                           is_function=True,
                                           min_identation=12)
        string_fixed = string_fixed.replace("return%", "return ", 1)
        string_fixed = string_fixed.replace("( ", "(", 1)
        ifc_file_string += string_fixed
        #ifc_file_string += INDEN_2 + "return self.create{}({})\n\n".format(entity.get("name_camel_case"), attr_string)

    # print(ifc_file_string)
    f = open("ifc_file.py", "w", encoding='utf8')
    f.write(ifc_file_string)
    f.close()


def generate_ifc_entities():
    ifc_entities_string = ""
    ifc_entities_string += "from ifcopenshell.entity_instance import entity_instance\n"
    ifc_entities_string += "\n\n"

    for entity_name in entity_tree_list:

        key = entity_identifier_dict.get(entity_name)
        entity = entity_dict.get(key)

        """if entity is None:
            print("entity None")
            print(entity_name)
            print(key)
            print(len(entity_identifier_dict))
            print(len(entity_dict))"""

        base_class = entity.get("base_class", "entity_instance")

        ifc_entities_string += "class {}({}):\n".format(entity.get("name_camel_case"), base_class)
        ifc_entities_string += INDEN_1 + "pass\n"
        ifc_entities_string += "\n\n"

    # print(ifc_entities_string)
    f = open("ifc_entities.py", "w", encoding='utf8')
    f.write(ifc_entities_string)
    f.close()


def generate_ifc_types():
    file_string = ""

    for key, entity in types_dict.items():
        file_string += "class {}".format(entity.get("name_camel_case"))
        if entity.get("python_type") is not "":
            file_string += "({})".format(entity.get("python_type"))
        file_string += ":\n"
        file_string += INDEN_1 + "pass\n"
        file_string += "\n\n"

    # print(file_string)
    f = open("ifc_types.py", "w", encoding='utf8')
    f.write(file_string)
    f.close()


if __name__ == "__main__":
    load_csv_data()
    load_exp_data()
    read_ifc_entity_tree()
    generate_ifc_file()
    generate_ifc_entities()
    generate_ifc_types()
