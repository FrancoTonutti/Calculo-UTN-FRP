import csv
import ifcopenshell
import os
import re
import xml
from ifcopenshell import validate
#import ifc_tools
import xmlschema
import json

from xmlschema.validators.schema import XsdComplexType, XsdAttribute, XsdAtomicRestriction
from xmlschema.validators.simple_types import XsdAtomicBuiltin



import utils
import pprint

# print(ifcopenshell.__file__)

# print(os.path.dirname(ifcopenshell.__file__))

IFC_PATH = os.path.dirname(ifcopenshell.__file__)

CSV_PATH = os.path.join(IFC_PATH, 'express')

IFC_TOOLS_PATH = os.path.dirname(__file__)
# print(IFC_TOOLS_PATH)
SCHEMA_FILE = "IFC4x1.exp"
SCHEMA_FILE_exp = "IFC4x1.exp"

snake_case_pattern = re.compile(r'(?<!^)(?=[A-Z])')
cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

INDEN_1 = " " * 4
INDEN_2 = " " * 8

PEP8_MAX_LENGTH = 79

attr_dict = dict()
entity_dict = dict()
entity_identifier_dict = dict()
types_dict = dict()

defined_types = utils.read_definitions("defined_types.txt")
defined_types_data = dict()

defined_types_file = utils.FileData()

exp_schema = utils.parse_exp(SCHEMA_FILE_exp)

print(json.dumps(exp_schema, indent=2))

my_schema = xmlschema.XMLSchema('IFC4x1.xsd')
print(my_schema)

"""for elem in my_schema.iter_globals():
    print(elem)"""

default_attrs = ['href', 'ref', 'id', 'path', 'pos', 'express', 'configuration']

for schema_type_name in my_schema.types:
    schema_type = my_schema.types[schema_type_name]


    if schema_type_name in defined_types:


        #print(schema_type_name)
        #print(schema_type.base_type)

        base_type = schema_type.base_type
        python_type = None

        if isinstance(base_type, XsdAtomicBuiltin):
            python_type = str(base_type.python_type)
            python_type = python_type.replace("<class '", "")
            python_type = python_type.replace("'>", "")
            #print(python_type)

        new_class = utils.ClassFileData(schema_type_name)
        if python_type:
            new_class.subclass_of = python_type

        defined_types_file.add_class(new_class)
        #print("add_class")



    if isinstance(schema_type, XsdAtomicRestriction):
        #print("{} - {}".format(schema_type_name, schema_type.base_type))
        #print("@ {}".format(schema_type.is_simple()))

        for tt in schema_type.iter_components():
            pass
            #print("----{}".format(tt))

    elif isinstance(schema_type, XsdComplexType):
        
        #print(schema_type)

        for attr_name in schema_type.attributes:
            #if attr_name not in default_attrs:

            xsd_attr: XsdAttribute = schema_type.attributes[attr_name]

            if xsd_attr.get_parent_type() is schema_type:
                pass
                #print("-{} - {}".format(attr_name, xsd_attr.type))
    else:
        print(schema_type)

print("------------")
#defined_types_file.print_file()
