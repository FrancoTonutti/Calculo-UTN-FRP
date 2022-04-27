from direct.showbase import DirectObject


class EventListener(DirectObject.DirectObject):
    def __init__(self):
        print("print EventHandler")

    def __del__(self):
        print("delete EventHandler")
        self.ignoreAll()

    def add_listener(self, event, method, args=None):
        if args:
            if not isinstance(args, list):
                args = [args]
        else:
            args = []

        self.accept(event, method, args)

    def close_listener(self):
        self.ignoreAll()


class Eventsample(object):
    def __init__(self):
        self.__eventhandlersample = []

    def __iadd__(self, Ehandler):
        self.__eventhandlersample.append(Ehandler)
        return self

    def __isub__(self, Ehandler):
        self.__eventhandlersample.remove(Ehandler)
        return self

    def __call__(self, *args, **keywargs):
        for eventhandlersample in self.__eventhandlersample:
            eventhandlersample(*args, **keywargs)
