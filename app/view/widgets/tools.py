from panda3d.core import Point3


def pos2d(x, y):
    return Point3(x, 0, -y)


def rec2d(width, height):
    return -width, 0, 0, height


def reset_pivot(frame):
    size = frame['frameSize']
    frame.setPos(-size[0], 0, -size[3])
    frame.flattenLight()
