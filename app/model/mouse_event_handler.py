from app import app


class MouseEventHandler:
    def __init__(self):
        panda3d = app.get_show_base()
        self.mouse_watcher = panda3d.mouseWatcherNode
        self.mouse_1_status = 0
        self.camera_control = panda3d.camera_control

    def mouse1_btn_released(self):
        # if self.mouse_watcher.hasMouse():
        if self.camera_control.mouse_is_over_workspace():
            if self.mouse_watcher.isButtonDown("mouse1"):
                self.mouse_1_status = 1
            else:
                if self.mouse_1_status is 1:
                    self.mouse_1_status = 0
                    return True

        return False