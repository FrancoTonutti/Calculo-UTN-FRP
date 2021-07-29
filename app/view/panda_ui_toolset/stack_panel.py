from .panel import Panel
from .controls import Orientation
import typing


class StackPanel(Panel):
    def __init__(self, orientation: typing.Union[int, str] = Orientation.VERTICAL, **kwargs):
        """
        Parameters
        ----------
        orientation
        parent: FrameworkElement
        width
        height
        margin
        min_width
        max_width
        min_height
        max_height
        """
        super().__init__(orientation=orientation, **kwargs)

    def update_layout(self):
        if len(self.childreen) is 0:
            return None

        avalible_space = 0
        is_vertical = self.logical_orientation == Orientation.VERTICAL

        if is_vertical:
            avalible_space = self.height
        else:
            avalible_space = self.width

        reserved_space = 0
        flex_elements = []

        for child in self.childreen:
            width = child.width.get_value()
            height = child.height.get_value()

            if is_vertical:
                if height == "Auto":
                    flex_elements.append(child)
                else:
                    reserved_space += height
            else:
                if width == "Auto":
                    flex_elements.append(child)
                else:
                    reserved_space += width

        if flex_elements:
            default_size = (avalible_space - reserved_space) / len(flex_elements)
        else:
            default_size = 0

        x = self._x
        y = self._y
        for child in self.childreen:
            if is_vertical:
                width = child.width.get_value(default=self.width.get_value())
                height = child.height.get_value(default=default_size)
            else:
                width = child.width.get_value(default=default_size)
                height = child.height.get_value(default=self.height.get_value())

            min_width = child.min_width.get_value(default=0)
            max_width = child.max_width.get_value(default=width)

            min_height = child.min_height.get_value(default=0)
            max_height = child.max_height.get_value(default=height)

            width = max(min_width, min(width, max_width))
            height = max(min_height, min(height, max_height))

            child.set_render_width(width)
            child.set_render_height(height)

            left = child.margin.left.get_value()
            right = child.margin.right.get_value()
            top = child.margin.top.get_value()
            bottom = child.margin.bottom.get_value()

            child.set_render_pos(x + left, y + top)

            if is_vertical:
                y += top + height + bottom
            else:
                x += left + width + right




