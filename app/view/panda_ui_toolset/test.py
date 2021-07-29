from direct.showbase.ShowBase import ShowBase
import panda3d.core as core
from panda3d.core import *
from direct.gui.OnscreenGeom import OnscreenGeom
from pandac.PandaModules import EggData, EggVertexPool, EggPolygon, EggVertex, \
    loadEggData
from panda3d.core import loadPrcFileData
import math

loadPrcFileData("", "win-size 1024 768")


def set_bounding_frame():
    data = EggData()

    vp = EggVertexPool('fan')
    data.addChild(vp)

    # real polygons:
    radius = 30  # arc radius
    linew = 15.0  # line width
    screen = (1024, 768)

    strips = {
        'upper': [
            {'x': radius, 'z': 0},  # tl
            {'x': screen[0] - radius, 'z': 0},  # tr
            {'x': screen[0] - radius, 'z': -linew},  # br
            {'x': radius, 'z': -linew}  # bl
        ],
        'lower': [
            {'x': radius, 'z': -screen[1] + linew},  # tl
            {'x': screen[0] - radius, 'z': -screen[1] + linew},  # tr
            {'x': screen[0] - radius, 'z': -screen[1]},  # br
            {'x': radius, 'z': -screen[1]}  # bl
        ],
        'left': [
            {'x': 0, 'z': -radius},  # tl
            {'x': linew, 'z': -radius},  # tr
            {'x': linew, 'z': -screen[1] + radius},  # br
            {'x': 0, 'z': -screen[1] + radius}  # bl
        ],
        'right': [
            {'x': screen[0] - linew, 'z': -radius},  # tl
            {'x': screen[0], 'z': -radius},  # tr
            {'x': screen[0], 'z': -screen[1] + radius},  # br
            {'x': screen[0] - linew, 'z': -screen[1] + radius}  # bl
        ]
    }

    for strip in strips.keys():
        poly = EggPolygon()
        data.addChild(poly)
        for vert in strips[strip]:
            v = EggVertex()
            v.setPos(Point3D(vert['x'], 0, vert['z']))
            poly.addVertex(vp.addVertex(v))

    steps = 32

    arcs = [
        {  # tl
            'arc_center': (radius, -radius),
            'start_angle': deg2Rad(270),
            'end_angle': deg2Rad(360)
        },
        {  # tr
            'arc_center': (screen[0] - radius, -radius),
            'start_angle': deg2Rad(0),
            'end_angle': deg2Rad(90)
        },
        {  # br
            'arc_center': (screen[0] - radius, -screen[1] + radius),
            'start_angle': deg2Rad(90),
            'end_angle': deg2Rad(180)
        },
        {  # bl
            'arc_center': (radius, -screen[1] + radius),
            'start_angle': deg2Rad(180),
            'end_angle': deg2Rad(270)
        }
    ]

    for arc in arcs:
        coords = []
        step = (arc['end_angle'] - arc['start_angle']) / steps
        arc_center = arc['arc_center']
        for i in range(steps + 1):
            a = arc['start_angle'] + i * step
            x = math.sin(a)
            z = math.cos(a)
            coords.append(((arc_center[0] + x * (radius - linew),
                            arc_center[1] + z * (radius - linew)),
                           (arc_center[0] + x * radius,
                            arc_center[1] + z * radius)))

        for i in range(steps):
            poly = EggPolygon()
            data.addChild(poly)
            vertices = [
                coords[i][0],
                coords[i][1],
                coords[i + 1][1],
                # 3rd and 4th are crossed, to have clockwise order
                coords[i + 1][0]
            ]
            for vert in vertices:
                v = EggVertex()
                v.setPos(Point3D(vert[0], 0, vert[1]))
                poly.addVertex(vp.addVertex(v))

    node = loadEggData(data)

    return OnscreenGeom(
        geom=NodePath(node),
        pos=(0, 0, 0),
        hpr=(0, 0, 0),
        # scale = (0.5,1,1),
        scale=(1, 1, 1),
        color=(246.0 / 256, 138.0 / 256, 72.0 / 256, 1),
        # parent = base.render2d
        parent=base.pixel2d
    )


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)
        set_bounding_frame()


app = MyApp()
app.run()