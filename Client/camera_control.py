from direct.task import Task


class CameraControl:

    def __init__(self, client):
        self.client = client
        self.scrolling_sensitivity = 10

    def zoom_in_camera(self, task):
        if self.client.camera.get_y() > 40:
            self.client.camera.set_y(self.client.camera, self.scrolling_sensitivity)
        return Task.done

    def zoom_out_camera(self, task):
        if self.client.camera.get_y() < 160:
            self.client.camera.set_y(self.client.camera, -self.scrolling_sensitivity)
        return Task.done
