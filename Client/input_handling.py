from direct.task.Task import Task
from panda3d.core import WindowProperties
from camera_control import CameraControl


class InputHandling:

    def __init__(self, client, char_ctrl, cam_ctrl):
        self.client = client
        self.char_ctrl = char_ctrl
        self.cam_ctrl = cam_ctrl

        self.mouse_clicked = False

        self.client.accept('w', self.w_handler)
        self.client.accept('w-up', self.w_up_handler)
        self.client.accept('s', self.s_handler)
        self.client.accept('s-up', self.s_up_handler)
        self.client.accept('a', self.a_handler)
        self.client.accept('a-up', self.a_up_handler)
        self.client.accept('d', self.d_handler)
        self.client.accept('d-up', self.d_up_handler)
        self.client.accept('mouse3', self.mouse_3_handler)
        self.client.accept('mouse3-up', self.mouse_3_up_handler)
        self.client.accept('wheel_up', self.wheel_up_handler)
        self.client.accept('wheel_down', self.wheel_down_handler)
        self.client.accept('q', self.q_handler)
        self.client.accept('q-up', self.q_up_handler)
        self.client.accept('e', self.e_handler)
        self.client.accept('e-up', self.e_up_handler)
        self.client.accept('r', self.r_handler)
        self.client.accept('f', self.f_handler)
        self.client.accept('escape', self.esc_handler)
        self.client.taskMgr.add(self.handle_rotating, "RotatePlayer")
        self.last_mouse_x = 0
        self.last_mouse_y = 0

    def w_handler(self):
        self.client.taskMgr.remove("MoveBackward")
        self.client.taskMgr.add(self.char_ctrl.move_forward, "MoveForward")

    def w_up_handler(self):
        self.client.taskMgr.remove("MoveForward")

    def s_handler(self):
        self.client.taskMgr.remove("MoveForward")
        self.client.taskMgr.add(self.char_ctrl.move_backward, "MoveBackward")

    def s_up_handler(self):
        self.client.taskMgr.remove("MoveBackward")

    def a_handler(self):
        self.client.taskMgr.remove("MoveRight")
        self.client.taskMgr.add(self.char_ctrl.move_left, "MoveLeft")

    def a_up_handler(self):
        self.client.taskMgr.remove("MoveLeft")

    def d_handler(self):
        self.client.taskMgr.add(self.char_ctrl.move_right, "MoveRight")
        self.client.taskMgr.remove("MoveLeft")

    def d_up_handler(self):
        self.client.taskMgr.remove("MoveRight")

    def mouse_3_handler(self):
        self.mouse_clicked = True
        self.set_cursor_hidden(True)

        md = self.client.win.get_pointer(0)
        self.last_mouse_x = md.get_x()
        self.last_mouse_y = md.get_y()
        self.client.win.move_pointer(0, 200, 200)

    def mouse_3_up_handler(self):
        self.mouse_clicked = False
        self.set_cursor_hidden(False)
        self.client.win.move_pointer(0, int(self.last_mouse_x), int(self.last_mouse_y))

    def wheel_up_handler(self):
        self.client.taskMgr.add(self.cam_ctrl.zoom_in_camera, "ZoomInCamera")

    def wheel_down_handler(self):
        self.client.taskMgr.add(self.cam_ctrl.zoom_out_camera, "ZoomOutCamera")

    def q_handler(self):
        pass

    def q_up_handler(self):
        pass

    def e_handler(self):
        pass

    def e_up_handler(self):
        pass

    def r_handler(self):
        pass

    def f_handler(self):
        pass

    def esc_handler(self):
        self.client.taskMgr.add(self.client.menu.go_to_menu, "ShowMenu")

    def handle_rotating(self, task):
        props = WindowProperties()
        props.setCursorHidden(True)
        if self.client.mouseWatcherNode.hasMouse() and self.mouse_clicked:
            md = self.client.win.getPointer(0)
            delta_x = md.get_x() - 200
            self.client.win.movePointer(0, 200, 200)
            self.client.world.main_player.set_h(self.client.world.main_player.get_h() - 0.3 * delta_x)
        return Task.cont

    def set_cursor_hidden(self, value):
        props = WindowProperties()
        props.setCursorHidden(value)
        self.client.win.requestProperties(props)
