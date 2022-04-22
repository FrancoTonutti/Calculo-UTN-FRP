from app.model import Entity, unit_manager


class ProfileShapeI(Entity):
    @staticmethod
    def create_from_object(obj):
        entity_id = obj.get("entity_id")

        return ProfileShapeI(entity_id)

    def __init__(self, set_id=None):
        super(ProfileShapeI, self).__init__(set_id)
        self.name = "Sección doble T"
        self.params = ["d", "bf", "tf", "hw", "tw", "r1", "r2"]
        self.is_clockwise = False

    def __str__(self):
        return self.name

    @staticmethod
    def get_contour_points(d, bf, tf, hw, tw, r1, r2):
        d = unit_manager.convert_to_m(d)
        bf = unit_manager.convert_to_m(bf)
        tf = unit_manager.convert_to_m(tf)
        hw = unit_manager.convert_to_m(hw)
        tw = unit_manager.convert_to_m(tw)

        x0 = -bf / 2
        y0 = -d / 2
        # En sentido anti horario
        points = [[x0, y0],
                  [x0 + bf, y0],
                  [x0 + bf, y0+tf],
                  [x0 + (bf + tw)/2, y0 + tf],
                  [x0 + (bf + tw) / 2, y0 + d - tf],
                  [x0 + bf, y0 + d - tf],
                  [x0 + bf, y0 + d],
                  [x0, y0 + d],
                  [x0, y0 + d - tf],
                  [x0 + (bf - tw) / 2, y0 + d - tf],
                  [x0 + (bf - tw) / 2, y0 + tf],
                  [x0, y0 + tf]
                  ]

        print("get_contour_points len {}".format(len(points)))

        return points

