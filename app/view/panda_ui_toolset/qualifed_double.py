import typing
from typing import List
from typing import Set
import numbers


class QualifedDouble:
    """

    """
    def __init__(self, value):
        super().__init__()
        self._pixel_value = 0
        self._value = 0
        self._unit = "px"
        self.auto = False

        self.set_value(value)

    def __str__(self):
        return "{} {}".format(self._value, self._unit)

    def __add__(self, other):
        if isinstance(other, QualifedDouble):
            other = other.pixel_value

        return QualifedDouble(other + self.pixel_value)

    def __radd__(self, other):
        return QualifedDouble(other + self.pixel_value)

    def __sub__(self, other):
        if isinstance(other, QualifedDouble):
            other = other.pixel_value

        return QualifedDouble(other - self.pixel_value)

    def __rsub__(self, other):
        return QualifedDouble(other - self.pixel_value)

    def __mul__(self, other):
        if isinstance(other, QualifedDouble):
            other = other.pixel_value

        return QualifedDouble(other * self.pixel_value)

    def __rmul__(self, other):
        return QualifedDouble(other * self.pixel_value)

    def __truediv__(self, other):
        if isinstance(other, QualifedDouble):
            other = other.pixel_value

        return QualifedDouble(self.pixel_value / other)

    def __rtruediv__(self, other):
        return QualifedDouble(other / self.pixel_value)

    def __floordiv__(self, other):
        if isinstance(other, QualifedDouble):
            other = other.pixel_value

        return QualifedDouble(self.pixel_value // other)

    def __rfloordiv__(self, other):
        return QualifedDouble(other // self.pixel_value)


    @property
    def pixel_value(self):
        return self._pixel_value

    def get_value(self, default="Auto", unit="px"):

        if self.auto:
            return default

        if unit == "px":
            value = self._pixel_value
        elif unit == "in":
            value = self._pixel_value / 96
        elif unit == "cm":
            value = self._pixel_value / 96*2.54
        elif unit == "pt":
            value = self._pixel_value / 96 * 72
        else:
            exeption_msj = "The str '{}' is not valid unit. " \
                           "Options allowed: px, in, cm, pt".format(unit)
            raise ValueError(exeption_msj)

        return value

    def set_value(self, value):

        if isinstance(value, QualifedDouble):
            self._value = value._value
            self._unit = value._unit
            self._pixel_value = value._pixel_value

            return None

        if not isinstance(value, str) and not isinstance(value, numbers.Real):
            exeption_msj = "QualifedDouble must be str, not '{}'".format(
                type(value))
            raise TypeError(exeption_msj)

        unit = "px"

        if isinstance(value, str):

            if value == "Auto":
                self._value = None
                self._unit = None
                self._pixel_value = None
                self.auto = True

                return None


            if " " in value:
                value, unit = value.split(" ", 1)

                if unit not in ["px", "in", "cm", "pt"]:
                    exeption_msj = "The str '{}' is not valid unit. " \
                                   "Options allowed: px, in, cm, pt".format(unit)
                    raise ValueError(exeption_msj)

            if value.isnumeric():
                value = float(value)
            else:
                exeption_msj = "QualifedString must be numeric"
                raise ValueError(exeption_msj)

        self._value = max(value, 0)

        if unit:
            self._unit = unit

            if unit == "in":
                self._pixel_value = self._value*96
            elif unit == "cm":
                self._pixel_value = self._value * 96/2.54
            elif unit == "pt":
                self._pixel_value = self._value * 96 / 72
            else:
                self._pixel_value = self._value
