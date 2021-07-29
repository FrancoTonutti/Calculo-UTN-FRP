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