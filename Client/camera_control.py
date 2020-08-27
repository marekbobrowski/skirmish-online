from direct.task import Task


class CameraControl:

    def __init__(self, camera):
        self.camera = camera
        self.scrolling_sensitivity = 10

    def zoom_in_camera(self, task):
        if self.camera.get_y() > 40:
            self.camera.set_y(self.camera, self.scrolling_sensitivity)
        return Task.done

    def zoom_out_camera(self, task):
        if self.camera.get_y() < 160:
            self.camera.set_y(self.camera, -self.scrolling_sensitivity)
        return Task.done
