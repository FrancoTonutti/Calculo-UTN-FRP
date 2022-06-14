class EntityReferenceMeta(type):
    def A__instancecheck__(self, other):
        check = super(EntityReferenceMeta, self).__instancecheck__(other)
        print('hi EntityReferenceMeta {}'.format(check))
        print('self {}'.format(self))
        print('other {}'.format(other))
        return check

    def __instancecheck__(cls, inst):
        """Implement isinstance(inst, cls)."""
        check = any(cls.__subclasscheck__(c) for c in {type(inst), inst.__class__})
        print('hi __instancecheck__ {}'.format(check))
        print('self {}'.format(cls))
        print('other {}'.format(inst))


        return check

    def __subclasscheck__(cls, sub):
        """Implement issubclass(sub, cls)."""
        candidates = cls.__dict__.get("__subclass__", set()) | {cls}
        check = any(c in candidates for c in sub.mro())
        print('hi __subclasscheck__ {}'.format(check))
        print('self {}'.format(cls))
        print('other {}'.format(sub))

        return check

    def __class__(self):
        print("__class__")
        return super(EntityReferenceMeta, self).__class__()


class EntityReference(metaclass=EntityReferenceMeta):
    pass


class Test:

    def __eq__(self, other):
        print("__eq__")
        super(Test, self).__eq__(other)



a = Test()
b = Test()
if a == b:
    pass