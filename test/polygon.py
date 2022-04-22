import matplotlib.pyplot as plt
import numpy as np

from app.model import Section
from app.model.profile_shapes import ProfileShapeI
from app.model.section_type import SectionType
from app.model.transaction import Transaction

import app.model.section
""""""
############

def angle(p1, p2, p3):
    print("angle points: {}, {}, {}".format(p1, p2, p3))
    v1 = [p2[0] - p1[0], p2[1] - p1[1]]
    v2 = [p2[0] - p3[0], p2[1] - p3[1]]

    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if norm1 == 0 or norm2 == 0:
        raise Exception("divide by 0")

    dot_product = np.dot(v1, v2)
    angle = np.arccos(dot_product / (norm1 * norm2))

    return angle


def merge_colinear_edges(points):
    n = len(points)
    i = 0
    while i < n and n >= 3:
        i0 = clamp_index(i - 1, 0, n - 1)
        i2 = clamp_index(i + 1, 0, n - 1)

        p0 = points[i0]
        p1 = points[i]
        p2 = points[i2]

        if angle(p0, p1, p2) == 0:
            pop_x, pop_y = points.pop(i)
            circle1 = plt.Circle((pop_x, pop_y), 0.005, color='b')
            plt.gca().add_patch(circle1)
            print("MERGE VERTEX {}".format(i))
            n = len(points)
        else:
            i += 1

    return points


def get_internal_angles(points, poly_clockwise):
    n = len(points)
    angles = [0] * n
    if n >= 3:
        for i in range(n):
            p1 = points[i]
            p2 = points[(i + 1) % n]
            p3 = points[(i + 2) % n]
            print([i, (i + 1) % n, (i + 2) % n])
            theta = angle(p1, p2, p3)
            triangle_clockwise = is_clockwise(p1, p2, p3)

            if triangle_clockwise != poly_clockwise:
                theta = 2 * np.pi - theta

            angles[(i + 1) % n] = theta

    return angles

def is_clockwise(p0, p, p2):

    vec_to_p0 = [p0[0] - p[0], p0[1] - p[1]]
    vec_to_p2 = [p2[0] - p[0], p2[1] - p[1]]

    det = vec_to_p0[0]*vec_to_p2[1] - vec_to_p0[1]*vec_to_p2[0]

    return det > 0

def cross_product(vec_to_p0, vec_to_p2):
    return vec_to_p0[0]*vec_to_p2[1] - vec_to_p0[1]*vec_to_p2[0]


def clamp_index(x, a, b):

    if a <= x <= b:
        return x
    elif x > b:
        return a
    else:
        return b


def point_in_triangle(p, p0, p1, p2):
    # From https://stackoverflow.com/a/20861130
    s = (p0[0] - p2[0]) * (p[1] - p2[1]) - (p0[1] - p2[1]) * (p[0] - p2[0])
    t = (p1[0] - p0[0]) * (p[1] - p0[1]) - (p1[1] - p0[1]) * (p[0] - p0[0])

    if (s < 0) != (t < 0) and s != 0 and t != 0:
        return False

    d = (p2[0] - p1[0]) * (p[1] - p1[1]) - (p2[1] - p1[1]) * (p[0] - p1[0])

    return d == 0 or (d < 0) == (s + t <= 0)


def get_first_valid_triangle(points, angles):
    n = len(points)
    indexs = list(range(n))

    indexs_sorted = sorted(indexs, key=lambda i: angles[i])

    for i in indexs_sorted:
        i0 = clamp_index(i - 1, 0, n - 1)
        i2 = clamp_index(i + 1, 0, n - 1)

        p0 = points[i0]
        p1 = points[i]
        p2 = points[i2]

        if is_valid_triangle(points, p0, p1, p2):
            return i0, i, i2

    else:
        print("All triangles are invalid")
        i = indexs_sorted[0]
        i0 = clamp_index(i - 1, 0, n - 1)
        i2 = clamp_index(i + 1, 0, n - 1)

        return i0, i, i2


def is_valid_triangle(points, p0, p1, p2):
    triangle = [p0, p1, p2]
    for point in points:
        if point not in triangle:
            if point_in_triangle(point, p0, p1, p2):
                return False

    return True


def triangulate(points, poly_clockwise):
    points = merge_colinear_edges(points)
    n = len(points)
    a=0
    for x,y in points:
        print("{}: {};{}".format(a, x, y))
        a += 1

    print("n: {}".format(n))

    m = n

    max_x = points[0][0]
    j = 0

    for i in range(n):
        if points[i][0] > max_x:
            max_x = points[i][0]
            j = i

    i0 = clamp_index(j-1, 0, n-1)
    i2 = clamp_index(j+1, 0, n-1)

    p1 = points[i0]
    p2 = points[j]
    p3 = points[i2]

    angles = get_internal_angles(points, poly_clockwise)

    triangles = []

    for i in range(m-2):

        i0, min_ang_index, i2 = get_first_valid_triangle(points, angles)

        p1 = points[i0]
        p2 = points[min_ang_index]
        p3 = points[i2]

        triangles.append([p1, p2, p3])

        xs, ys = zip(*[p1, p2, p3, p1])

        plt.plot(xs, ys)
        plt.pause(2)

        pop_x, pop_y = points.pop(min_ang_index)
        angles.pop(min_ang_index)

        circle1 = plt.Circle((pop_x, pop_y), 0.005, color='r')
        plt.gca().add_patch(circle1)
        plt.pause(2)

        points = merge_colinear_edges(points)
        angles = get_internal_angles(points, poly_clockwise)

        n = len(points)

        if n < 3:
            break

    return triangles

""""""

tr = Transaction()
tr.start()

sec_type = SectionType("IPN")
shapes = sec_type.valid_values_shape()
for shape in shapes:
    if isinstance(shape, ProfileShapeI):
        sec_type.shape = shape

sec = Section("IPN 300", sec_type, {"d": "300 mm",
                              "bf": "125 mm",
                              "tf": "16.2 mm",
                              "hw": "241 mm",
                              "tw": "10.8 mm",
                              "r1": "10.8 mm",
                              "r2": "6.5 mm"})

tr.commit()

coord = sec.get_contour_points()
coord_traing = coord.copy()
#coord_traing = coord_traing[::-1]


#coord = [[1,1], [2,1], [2,2], [1,2], [0.5,1.5]]
coord.append(coord[0]) #repeat the first point to create a 'closed loop'

xs, ys = zip(*coord) #create lists of x and y values

plt.figure()
plt.axes().set_aspect('equal')
plt.plot(xs,ys)
plt.pause(2)

traingles = triangulate(coord_traing, sec.section_type.shape.is_clockwise)

'''for triangle in traingles:
    triangle.append(triangle[0])
    xs, ys = zip(*triangle)
    plt.plot(xs, ys)
    plt.pause(2)'''


plt.show() # if you need...

