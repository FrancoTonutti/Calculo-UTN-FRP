from direct.showbase import DirectObject


class EventListener(DirectObject.DirectObject):
    def __init__(self):
        print("print EventHandler")

    def __del__(self):
        print("delete EventHandler")
        self.ignoreAll()

    def add_listener(self, event, method, args=None):
        if args and not isinstance(args, list):
            args = [args]
        else:
            args = []
        self.accept(event, method, args)

    def close_listener(self):
        self.ignoreAll()
