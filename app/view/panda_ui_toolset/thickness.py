from .qualifed_double import QualifedDouble

class Thickness:
    def __init__(self, left, top=None, right=None, bottom=None):
        """

        Parameters
        ----------
        left
        left, top, right, bottom

        """

        self.left = QualifedDouble(0)
        self.top = QualifedDouble(0)
        self.right = QualifedDouble(0)
        self.bottom = QualifedDouble(0)

        self.set_thickness(left, top, right, bottom)

    def set_thickness(self, left, top=None, right=None, bottom=None):

        if isinstance(left, list):
            if len(left) == 1:
                left = left[0]
            elif len(left) == 2:
                left, top = left
            elif len(left) == 3:
                left, top, right = left
            elif len(left) == 4:
                left, top, right, bottom = left
            else:
                exeption_msj = "The max list size for Thickness 4"
                raise ValueError(exeption_msj)

        if right is None:
            right = left

        if top is None:
            top = left

        if bottom is None:
            bottom = top

        self.left.set_value(left)
        self.top.set_value(top)
        self.right.set_value(right)
        self.bottom.set_value(bottom)
