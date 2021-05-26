def read_definitions(filename):
    f = open(filename, "r")
    definitions = f.read()
    definitions = definitions.split("\n")

    return definitions


class ClassFileData:
    def __init__(self, name, subclass_of=None, superclass_of=None):
        if subclass_of and not isinstance(subclass_of, list):
            subclass_of = [subclass_of]

        if superclass_of and not isinstance(superclass_of, list):
            superclass_of = [superclass_of]

        if subclass_of is None:
            subclass_of = []

        if superclass_of is None:
            superclass_of = []

        self.name = name
        self.subclass_of = subclass_of
        self.superclass_of = superclass_of

class FileData:
    iden_1 = " " * 4
    iden_2 = " " * 8
    iden_3 = " " * 12

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.classes = dict()
        self.imports = list()

    def add_class(self, class_data: ClassFileData):
        self.classes.update({class_data.name: class_data})

    def get_class(self, class_name: str):
        return self.classes.get(class_name)

    def add_import(self, import_module, import_from=None, import_as=None):
        self.imports.append({"import": import_module,
                             "from": import_from,
                             "as": import_as})



    def reorder_class_by_inheritance(self):

        _class: ClassFileData
        for _class in self.classes:

            subclass_of = _class.subclass_of

            for superclass_name in subclass_of:
                superclass: ClassFileData = self.get_class(superclass_name)


    def print_file(self):
        str_file = ""

        _class: ClassFileData
        for _class in self.classes.values():
            # Class Definition
            str_file += "class {}".format(_class.name)

            if _class.subclass_of:
                if isinstance(_class.subclass_of, list):
                    str_inheritance = ", ".join(_class.subclass_of)
                else:
                    str_inheritance = _class.subclass_of
                str_file += "({})".format(str_inheritance)

            str_file += ":\n"
            # Class Content
            str_file += self.iden_1 + "pass\n\n"

        print(str_file)




def generate_python_file(file_data):
    pass


def safe_list_get(l, idx, default=None):
    try:
        return l[idx]
    except IndexError:
        return default


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


def removesuffix(self: str, suffix: str) -> str:
    if self.endswith(suffix):
        return self[:-len(suffix)]
    else:
        return self[:]


def removeprefix(self: str, prefix: str) -> str:
    if self.startswith(prefix):
        return self[len(prefix):]
    else:
        return self[:]


def split_line(line: str):
    pass


def parse_exp(filename):
    f = open(filename, "r")
    lines = f.read()
    comments = find_between(lines, "(*", "*)")

    lines = lines.replace("(*" + comments + "*)", "")
    lines = lines.replace("\t", " ")



    lines = lines.replace(" ,", ", ")
    lines = lines.split("\n")

    new_lines = []
    new_line = ""

    for line in lines:
        new_line += line
        if new_line.endswith(";") or new_line.endswith("WHERE") or new_line.endswith("INVERSE"):
            new_line = removeprefix(new_line, " ")

            while "  " in new_line:
                new_line = new_line.replace("  ", " ")

            new_line = new_line.replace(" , ", ", ")
            new_lines.append(new_line)
            new_line = ""




    lines = new_lines

    #print("\n".join(lines))

    def_name = None
    where_line = None

    schema = {
        "schema": "",
        "types": {},
        "entities": {}
    }
    context = list()

    for line in lines:
        if line.startswith("SCHEMA"):
            schema_version = removeprefix(line, "SCHEMA ")
            schema_version = removesuffix(schema_version,";")
            schema.update({"schema": schema_version})
            context.append("SCHEMA")
        elif safe_list_get(context, 0) == "SCHEMA":

            if line.startswith("TYPE"):
                context.append("TYPE")
                line = removeprefix(line, "TYPE ")
                line = removesuffix(line, ";")
                def_name, def_type = line.split(" = ")

                size = None
                def_iter = None

                def_type: str
                if " OF " in def_type:

                    def_type = def_type.replace("[", "")
                    def_type = def_type.replace("]", "")

                    def_type = removeprefix(def_type, " ")
                    def_type = removesuffix(def_type, ";")

                    def_iter, def_type = def_type.split(" OF ")

                    if ":" in def_iter:
                        try:
                            def_iter, size = def_iter.split(" ")
                            size = size.split(":")
                        except Exception as ex:
                            raise Exception(def_iter)


                defined_types = schema.get("types")
                defined_types.update({def_name: {
                    "name": def_name,
                    "type": def_type,
                    "size": size,
                    "iter": def_iter,
                    "where": []
                }})

            elif safe_list_get(context, 1) == "TYPE" or safe_list_get(context, 1) == "ENTITY":
                if line.startswith("END_TYPE"):
                    context = context[0:1]
                elif line.startswith("END_ENTITY"):
                    context = context[0:1]
                elif line.startswith("INVERSE"):
                    context.append("INVERSE")
                elif line.startswith("WHERE"):
                    if len(context) == 2:
                        context.append("WHERE")
                    else:
                        context[2] = "WHERE"
                elif safe_list_get(context, -1) == "ENTITY" or safe_list_get(context, -1) == "INVERSE":
                    line = removesuffix(line, ";")
                    attr_name, attr_type = line.split(" : ")
                    attr_optional = False

                    size = None

                    if "OPTIONAL" in attr_type:
                        attr_optional = True
                        attr_type = attr_type.replace("OPTIONAL ", "")

                    attr_type, c_size, c_content = get_type(attr_type)

                    schema_dict = schema.get("entities")

                    key = "attributes"
                    if safe_list_get(context, -1) == "INVERSE":
                        key = "inverse"

                    attr_list = schema_dict.get(def_name).get(key)
                    attr_list.append(
                        {"name": attr_name,
                         "type": attr_type,
                         "optional": attr_optional,
                         "collection": c_content,
                         "size": c_size,
                         })

                elif safe_list_get(context, -1) == "WHERE":

                    if line.endswith(";") and " : " in line:
                        w_name, w_condition = line.split(" : ")

                        w_condition: str
                        w_condition = w_condition.replace("{", "")
                        w_condition = w_condition.replace("}", "")
                        w_condition = w_condition.replace(";", "")

                        w_condition = w_condition.replace("SELF", "self")
                        w_condition = w_condition.replace(" IN ", " in ")
                        w_condition = w_condition.replace(" AND ", " and ")
                        w_condition = w_condition.replace(" OR ", " or ")
                        w_condition = w_condition.replace(" OR(", " or (")
                        w_condition = w_condition.replace("ABS(", "abs(")
                        w_condition = w_condition.replace("TYPEOF(", "type(")
                        w_condition = w_condition.replace("TYPEOF (", "type(")
                        w_condition = w_condition.replace("SIZEOF(", "len(")
                        w_condition = w_condition.replace("SIZEOF (", "len(")
                        w_condition = w_condition.replace(" NOT ", " not ")
                        w_condition = w_condition.replace("NOT (", "not (")
                        w_condition = w_condition.replace("NOT(", "not (")

                        if safe_list_get(context, 1) == "TYPE":
                            schema_dict = schema.get("types")
                        elif safe_list_get(context, 1) == "ENTITY":
                            schema_dict = schema.get("entities")

                        where_list = schema_dict.get(def_name).get("where")
                        where_list.append({"w_name": w_name, "w_condition": w_condition})
                    else:
                        raise Exception("where line not ends with ';' : \n{}".format(line))

            elif line.startswith("ENTITY"):
                context.append("ENTITY")
                line = removeprefix(line, "ENTITY ")
                line = removesuffix(line, ";")

                line = line.replace(" ABSTRACT ", " ")
                #def_name, def_type = line.split(" = ")
                def_name = line

                supertype_of = None
                subtype_of = None

                if " SUPERTYPE OF " in line:
                    def_name, supertype_of = line.split(" SUPERTYPE OF (ONEOF ")

                    if " SUBTYPE OF " in supertype_of:
                        supertype_of, subtype_of = supertype_of.split(" SUBTYPE OF ")

                if supertype_of is None and " SUBTYPE OF " in line:
                    def_name, subtype_of = line.split(" SUBTYPE OF ")

                if supertype_of:
                    supertype_of = removeprefix(supertype_of, "(")
                    supertype_of = removesuffix(supertype_of, "))")

                if subtype_of:
                    subtype_of = removeprefix(subtype_of, "(")
                    subtype_of = removesuffix(subtype_of, ")")

                entities = schema.get("entities")
                entities.update({def_name: {
                    "name": def_name,
                    "supertype_of": supertype_of,
                    "subtype_of": subtype_of,
                    "attributes": [],
                    "inverse": [],
                    "where": []
                }})



            if line.startswith("END_SCHEMA;"):
                context.clear()

    return schema

def get_type(collection):

    c_type = None
    c_content = None
    c_size = None

    if " OF " in collection:

        collection = collection.replace("[", "")
        collection = collection.replace("]", "")

        c_type, c_content = collection.split(" OF ", maxsplit=1)

        c_type = c_type.replace("UNIQUE LIST", "UNIQUE_LIST")

        if " OF " in c_content:
            c_content = get_type(c_content)

        if ":" in c_type:
            try:
                c_type, c_size = c_type.split(" ")
                c_size = c_size.split(":")
            except:
                raise Exception(c_type)

    return c_type, c_size, c_content