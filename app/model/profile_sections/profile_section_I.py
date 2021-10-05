from app.model.entity import Entity, register
from .profile_section import ProfileSection
import numpy

class ProfleSectionI(ProfileSection):

    @staticmethod
    def create_from_object(obj):
        entity_id = obj.get("entity_id")
        width, height = obj.get("size")

        Section(width, height, entity_id)

    def __init__(self, d, bf, tf, tw, r, set_id=None):
        super().__init__(set_id)

        self.d = d
        self.bf = bf
        self.tf = tf
        self.tw = tw
        self.r = r

        self._cache_data = dict()

    def inertia_x(self):
        if "Ix" not in self._cache_data:

            d = self.d/10
            bf = self.bf/10
            tf = self.tf/10
            tw = self.tw/10
            r = self.r/10

            ix1 = bf*tf**3/12 + bf*tf*((d-tf)/2)**2

            ix2 = (tw*((d-2*tf)**3))/12

            ix3 = 2*r*(r**3)/12 + 2*r*r*((d-r)/2-tf)**2

            ix4 = numpy.pi*r**4/8 + 0.5*numpy.pi*r**2*(d/2-r-tf)**2

            ix = 2*ix1 + ix2 + 2*ix3 - 2*ix4

            print("tw", tw)
            print("d-2*tf", d-2*tf)
            print("(d-2*tf)**3", (d-2*tf)**3)
            print("(tw*((d-2*tf)**3))", tw*((d-2*tf)**3))

            self._cache_data.update({"Ix": ix})
        else:
            ix = self._cache_data.get("Ix")


        return ix

    def inertia_y(self):
        b = self.size[0]
        h = self.size[1]
        return (h * pow(b, 3)) / 12

    def area(self):
        if "Ag" not in self._cache_data:
            area1 = 2 * (self.bf * self.tf)
            area2 = (self.d - 2 * self.tf) * self.tw
            r2 = self.r * self.r
            area3 = 4 * r2 - numpy.pi * r2

            area = area1 + area2 + area3

            self._cache_data.update({"Ag": area})
        else:
            area = self._cache_data.get("Ag")

        return area

    def __str__(self):
        return "<class 'app.model.core.Section'>"
