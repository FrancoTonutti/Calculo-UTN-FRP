from app.model import Entity, unit_manager


class ProfileShapeFillRect(Entity):
    @staticmethod
    def create_from_object(obj):
        entity_id = obj.get("entity_id")

        return ProfileShapeFillRect(entity_id)

    def __init__(self, set_id=None):
        super(ProfileShapeFillRect, self).__init__(set_id)
        self.name = "Sección rectangular"
        self.params = ["bw", "h"]

    def __str__(self):
        return self.name

    @staticmethod
    def get_contour_points(bw, h):
        bw = unit_manager.convert_to_m(bw)
        h = unit_manager.convert_to_m(h)

        x0 = -bw/2
        y0 = -h/2
        points = [[x0, y0],
                  [x0+bw, y0],
                  [x0+bw, y0+h],
                  #[x0 + bw/2, y0 + h/2],
                  [x0, y0+h],
                  #[x0, y0]
                  ]

        return points
