from app.model import Entity, unit_manager
from app.model.profile_shapes.profile_shape import ProfileShape


class ProfileShapeHollowRect(ProfileShape):
    @staticmethod
    def create_from_object(obj):
        entity_id = obj.get("entity_id")

        shape = ProfileShapeHollowRect(entity_id)

        return shape

    def __init__(self, set_id=None):
        super(ProfileShapeHollowRect, self).__init__(set_id)
        self.name = "Sección tubular rectangular"
        self.params = ["b", "h", "t"]

    def __str__(self):
        return self.name

    @staticmethod
    def get_contour_points(b, h, t):
        b = unit_manager.convert_to_m(b)
        h = unit_manager.convert_to_m(h)
        t = unit_manager.convert_to_m(t)
        r = 2*t
        x0 = -b/2
        y0 = -h/2
        points = [[x0, y0+r],
                  [x0+r, y0],

                  [x0+b-r, y0],
                  [x0 + b, y0+r],

                  [x0 + b, y0 + h-r],
                  [x0 + b-r, y0 + h],

                  #[x0 + bw/2, y0 + h/2],
                  [x0+r, y0 + h],
                  [x0, y0 + h-r],
                  #[x0, y0]
                  ]

        return points
