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
    print("angle: {}, {}, {}".format(p1, p2, p3))
    v1 = [p2[0] - p1[0], p2[1] - p1[1]]
    v2 = [p2[0] - p3[0], p2[1] - p3[1]]

    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if norm1 == 0 or norm2 == 0:
        raise Exception("divide by 0")

    dot_product = np.dot(v1, v2)
    angle = np.arccos(dot_product / (norm1 * norm2))

    return angle




def is_clockwise(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    det = (x2 - x1) * (x3 - x1) - (x3 - x1) * (y2 - y1)

    return det < 0


def clamp_index(x, a, b):

    if a <= x <= b:
        return x
    elif x > b:
        return a
    else:
        return b


def triangulate(points):
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

    poly_clockwise = is_clockwise(p1, p2, p3)

    angles = [0]*n

    for i in range(n):
        p1 = points[i]
        p2 = points[(i+1) % n]
        p3 = points[(i+2) % n]
        print([i, (i+1) % n, (i+2) % n])
        theta = angle(p1, p2, p3)
        triangle_clockwise = is_clockwise(p1, p2, p3)

        if triangle_clockwise != poly_clockwise:
            theta = 2*np.pi - theta

        angles[(i+1) % n] = theta

    triangles = []

    for i in range(m-2):
        min_ang = min(angles)
        min_ang_index = angles.index(min_ang)

        i0 = clamp_index(min_ang_index-1, 0, n-1)
        i2 = clamp_index(min_ang_index+1, 0, n - 1)

        p1 = points[i0]
        p2 = points[min_ang_index]
        p3 = points[i2]

        triangles.append([p1, p2, p3])

        xs, ys = zip(*[p1, p2, p3, p1])


        plt.plot(xs, ys)
        plt.pause(2)

        #plt.show()


        if p2 == p3:
            raise Exception(str([i0, min_ang_index, i2]))

        p1 = points[clamp_index(i0-1, 0, n-1)]
        p2 = points[min_ang_index]
        p3 = points[i2]

        theta = angle(p1, p2, p3)
        triangle_clockwise = is_clockwise(p1, p2, p3)

        if triangle_clockwise != poly_clockwise:
            theta = 2*np.pi - theta

        angles[i0] = theta

        p1 = points[i0]
        p2 = points[i2]
        p3 = points[clamp_index(i2+1, 0, n-1)]

        triangle_clockwise = is_clockwise(p1, p2, p3)

        if triangle_clockwise != poly_clockwise:
            theta = 2 * np.pi - theta

        angles[i2] = theta

        pop_x, pop_y = points.pop(min_ang_index)
        angles.pop(min_ang_index)

        circle1 = plt.Circle((pop_x, pop_y), 0.01, color='r')
        plt.gca().add_patch(circle1)
        plt.pause(2)



        n -= 1

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
coord_traing = coord_traing[::-1]


#coord = [[1,1], [2,1], [2,2], [1,2], [0.5,1.5]]
coord.append(coord[0]) #repeat the first point to create a 'closed loop'

xs, ys = zip(*coord) #create lists of x and y values

plt.figure()
plt.axes().set_aspect('equal')
plt.plot(xs,ys)
plt.pause(2)

traingles = triangulate(coord_traing)

'''for triangle in traingles:
    triangle.append(triangle[0])
    xs, ys = zip(*triangle)
    plt.plot(xs, ys)
    plt.pause(2)'''


plt.show() # if you need...

