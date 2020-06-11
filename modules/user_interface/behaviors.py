from kivy.properties import BooleanProperty, ObjectProperty
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.uix.widget import Widget



class HoverBehavior(Widget):
    hovered = BooleanProperty(False)
    border_point = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverBehavior, self).__init__(**kwargs)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return # do proceed if I'm not displayed <=> If have no parent
        pos = args[1]
        # Next line to_widget allow to compensate for relative layout
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            return # We have already done what was needed
        self.border_point = pos
        self.hovered = inside

        if inside:
            self.dispatch("on_enter")
        else:
            self.dispatch("on_leave")


Factory.register('HoverBehavior', HoverBehavior)

