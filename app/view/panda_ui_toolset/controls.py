from enum import Enum


def get_args(default: dict, **kwargs):
    return default.update(kwargs)


class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1
