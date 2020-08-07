from app import app
from app.view.widgets.button import new_button
from app.view.widgets.frame import Frame


class WidProperties:
    def __init__(self, panda_app):
        super(WidProperties, self).__init__()
        self.panda3d = app
        self.entity_data = dict()
        self.entity = None

        self.fields = []

    def add_property(self, prop, name, value=0):
        """lb = Label(text=name)
        self.add_widget(lb)
        ti = PropInput(prop=prop, text=str(value))
        self.add_widget(ti)
        self.fields.append([lb, ti])"""
        pass

    def entity_read(self, entity=None):
        if len(self.fields):
            if self.panda3d.kyvi_focused_ti:
                self.panda3d.kyvi_focused_ti.on_text_validate()

        if self.entity and self.entity.geom:
            self.entity.geom.setTextureOff(0)
            self.entity.geom.clearColorScale()

        if entity:
            self.entity = entity
            if self.entity.geom:
                self.entity.geom.setTextureOff(1)
                self.entity.geom.setColorScale(1, 0, 0, 0.7)

        for wid in self.fields:
            pass
            # self.remove_widget(wid[0])
            # self.remove_widget(wid[1])

        # print("read")
        # print(dir(self.entity))
        for prop in self.entity.get_properties():
            # for prop in dir(self.entity):
            # if self.entity.is_public(prop):
            # self.add_property(prop, self.entity.prop_name(prop), inspect.getattr_static(self.entity, prop))
            self.add_property(prop, self.entity.prop_name(prop), getattr(self.entity, prop))

    def entity_set_prop(self, name, value):
        last_value = getattr(self.entity, name, None)
        val = value
        if isinstance(last_value, float):
            val = float(val)
        if type(last_value) is type(val):
            setattr(self.entity, name, val)
        else:
            print("El tipo de asignación no corresponde: {},{}->{}".format(name, type(self.entity.__dict__[name]),
                                                                           type(val)))
