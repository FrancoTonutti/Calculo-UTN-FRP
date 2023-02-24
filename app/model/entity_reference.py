import ctypes


class EntityReferenceRegister:
    def __init__(self):
        self.references_list = list()
        self.garbage = list()

    def add_reference(self, ref):
        if ref not in self.references_list:
            self.references_list.append(ref)

        self.update()

    def update(self):
        for ref in self.references_list:
            if not ref.__updated__:
                ref.__update__()

            if ctypes.c_long.from_address(id(ref)).value == 1:
                self.garbage.append(ref)

        self.clear_garbage()

    def clear_garbage(self):
        for ref in self.garbage:
            self.references_list.remove(ref)

        self.garbage.clear()


register = EntityReferenceRegister()


class EntityReference:
    def __init__(self, entity):
        if isinstance(entity, EntityReference):
            raise Exception("EntityReference to EntityReference is not allowed")

        self.__reference__ = entity
        self.__entity_id__ = None
        self.__updated__ = False
        self.__update__()
        register.add_reference(self)

    def __update__(self):
        if self.__reference__:
            check = 0
            if hasattr(self.__reference__, "_entity_id"):
                self.__entity_id__ = self.__reference__.entity_id
                check += 1

            if hasattr(self.__reference__, "__references__"):
                self.__reference__.add_refence(self)
                check += 1

            if check == 2:
                self.__updated__ = True



    def __dispose__(self):
        if self.__reference__:
            self.__reference__.remove_reference(self)
            self.__reference__ = None

    def __del__(self):
        self.__dispose__()

    def __getattr__(self, attr):
        if self.__reference__:
            if not self.__reference__.__is_deleted__:
                return getattr(self.__reference__, attr)
            else:
                self.__reference__ = None
                return None
        else:
            return None

    def __setattr__(self, name, value):
        if name == "__reference__" or name == "__entity_id__" or name == "__updated__":
            super(EntityReference, self).__setattr__(name, value)
        else:
            if self.__reference__ and not self.__reference__.__is_deleted__:
                setattr(self.__reference__, name, value)
            else:
                self.__reference__ = None

    def __str__(self):
        if self.__reference__:
            if not self.__reference__.__is_deleted__:
                pass
                return self.__reference__.__str__()
            else:
                pass
                self.__dispose__()
                return super(EntityReference, self).__str__()
        else:
            return super(EntityReference, self).__str__()

        return ""

    def __eq__(self, other):
        if isinstance(other, EntityReference):
            return self.__reference__ == other.__reference__
        else:
            return self.__reference__ == other


def create_entity_reference(value):
    return value
