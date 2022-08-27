from .code_check_CIRSOC_201 import CodeCheckCIRSOC201


class BaseCodeCheck:
    def __init__(self, name, version):
        self.name = name
        self.version = version
        self.chapters = []


class BaseChapter:
    def __init__(self, index, name):
        self.index = index
        self.name = name
