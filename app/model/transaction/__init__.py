class TransactionManager:
    def __init__(self):
        self.root_transaction = None
        self.history = list()
        self.history_position = -1

    def get_root_transaction(self):
        return self.root_transaction

    def get_active_transaction(self):
        if self.root_transaction:
            tr = self.root_transaction
            while (tr._childs):
                tr = tr._childs[-1]
            return tr
        else:
            return None

    def history_undo(self):
        transaction = self.history[self.history_position]

        tr = Transaction(register=False)
        tr.start()

        transaction.undo()

        tr.commit()


TM = TransactionManager()


class Action:
    def __init__(self):
        pass

    def undo(self):
        pass

    def redo(self):
        pass

class EntityCreationAction(Action):
    def __init__(self, obj, args=None):
        super().__init__()
        self.obj = obj
        self.args = args

    def undo(self):
        print("EntityCreationAction undo")
        print(self)
        self.obj.delete()

    def redo(self):
        pass

class SetAttrAction(Action):
    def __init__(self, obj, attr, old_value, new_value):
        super().__init__()
        self.obj = obj
        self.attr = attr
        self.old_value = old_value
        self.new_value = new_value

    def undo(self):
        setattr(self.obj, self.attr, self.old_value)

    def redo(self):
        setattr(self.obj, self.attr, self.new_value)


class TransactionAction(Action):
    def __init__(self, transaction):
        super().__init__()
        self.transaction = transaction

    def undo(self):
        for action in self.transaction.get_actions():
            action.undo()

    def redo(self):
        for action in self.transaction.get_actions():
            action.redo()


class Transaction:
    global TM

    def __init__(self, register=True, name=None):
        self.name = name
        self.parent = None
        self._childs = list()
        self._commited = False
        self._actions = list()

    def is_commited(self):
        return self._commited

    def start(self, name=None):
        root = TM.root_transaction
        self.name = name
        if root:
            parent = root
            while (parent._childs):
                tr = parent._childs[-1]
                if not tr.is_commited():
                    parent = tr
                else:
                    break

            self.parent = parent
            self.parent._childs.append(self)
            action = TransactionAction(self)
            self.parent.register_action(action)

        else:
            TM.root_transaction = self

    def commit(self):
        if not self._childs or self._childs[-1].is_commited():
            self._commited = True
            if not self.parent:
                TM.root_transaction = None
                TM.history.append(self)

        else:
            raise Exception(
                "Las transacciones hijas no se finalizaron correctamente")

    def rollback(self):
        for action in self.get_actions():
            action.undo()
        self._commited = True

    def register_action(self, action):
        self._actions.append(action)

    def get_actions(self):
        return self._actions[::-1]

    def undo(self):
        if self.is_commited():
            for action in self.get_actions():
                action.undo()
        else:
            raise Exception("Can't undo uncommited transaction")


class DataManager:
    global TM

    def __init__(self):
        tr = Transaction()
        tr.start()
        self.var1 = 1
        self.var2 = 1
        self.history = list()
        tr.commit()

    def register_transaction(self):
        pass

    def __setattr__(self, attr, value):
        active_transaction = TM.get_active_transaction()

        if active_transaction:
            if hasattr(self, attr):
                old = getattr(self, attr)
            else:
                old = None
            super().__setattr__(attr, value)

            action = SetAttrAction(self, attr, old, value)
            active_transaction.register_action(action)
        else:
            raise Exception("No existe una transacción activa")


'''dm = DataManager()
print("start")
global_tr = Transaction()

global_tr.start()
dm.var1 = "set1"
tr = Transaction()
tr.start()

dm.var1 = 125
dm.var2 = "testing"

tr.commit()
global_tr.commit()

print(dm.var1)
print(dm.var2)

print("Undo")
TM.history_undo()

print(dm.var1)
print(dm.var2)'''
