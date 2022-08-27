from ...code_checks import *


class CIRSOC_301_D(BaseChapter):
    def __init__(self):
        super(BaseChapter, self).__init__("D", "BARRAS TRACCIONADAS")


class CIRSOC_301(BaseCodeCheck):
    def __init__(self):
        super(CIRSOC_301, self).__init__("CIRSOC 301", 2005)
