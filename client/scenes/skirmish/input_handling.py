from direct.task.Task import Task
from panda3d.core import WindowProperties


class InputHandling:

    def __init__(self, skirmish):
        self.skirmish = skirmish
        self.core = skirmish.core

        self.char_ctrl = skirmish.character_control
        self.cam_ctrl = skirmish.camera_control
        self.mouse_sensitivity = 0.5

        # Input states.
        self.mouse_1_clicked = False
        self.mouse_3_clicked = False
        self.w_pressed = False
        self.a_pressed = False
        self.d_pressed = False
        self.last_mouse_x = 200
        self.last_mouse_y = 200

        # Assignment of handling functions.
        self.core.accept('w', self.w_handler)
        self.core.accept('w-up', self.w_up_handler)
        self.core.accept('s', self.s_handler)
        self.core.accept('s-up', self.s_up_handler)
        self.core.accept('a', self.a_handler)
        self.core.accept('a-up', self.a_up_handler)
        self.core.accept('d', self.d_handler)
        self.core.accept('d-up', self.d_up_handler)
        self.core.accept('mouse1', self.mouse_1_handler)
        self.core.accept('mouse1-up', self.mouse_1_up_handler)
        self.core.accept('mouse3', self.mouse_3_handler)
        self.core.accept('mouse3-up', self.mouse_3_up_handler)
        self.core.accept('wheel_up', self.wheel_up_handler)
        self.core.accept('wheel_down', self.wheel_down_handler)
        self.core.accept('q', self.q_handler)
        self.core.accept('q-up', self.q_up_handler)
        self.core.accept('e', self.e_handler)
        self.core.accept('e-up', self.e_up_handler)
        self.core.accept('r', self.r_handler)
        self.core.accept('f', self.f_handler)
        self.core.accept('escape', self.esc_handler)

    def w_handler(self):
        self.w_pressed = True
        self.core.taskMgr.remove("MoveBackward")
        # Start moving if the character is not moving yet (mouse buttons allow to move, so we have to check).
        if not self.core.taskMgr.hasTaskNamed("MoveForward"):
            self.core.taskMgr.add(self.char_ctrl.move_forward, "MoveForward")

    def w_up_handler(self):
        self.w_pressed = False
        # Stop moving if not both mouse buttons are clicked.
        if not (self.mouse_1_clicked and self.mouse_3_clicked):
            self.core.taskMgr.remove("MoveForward")

    def s_handler(self):
        # Stop moving forward.
        self.core.taskMgr.remove("MoveForward")
        # Start moving backward.
        self.core.taskMgr.add(self.char_ctrl.move_backward, "MoveBackward")

    def s_up_handler(self):
        # Stop moving backward.
        self.core.taskMgr.remove("MoveBackward")

    def a_handler(self):
        self.a_pressed = True
        # Stop rotating to the right.
        self.core.taskMgr.remove("RotateRight")
        self.core.taskMgr.remove("MoveRight")

        # If the mouse3 button is clicked, start moving(!) to the left.
        if self.mouse_3_clicked:
            self.core.taskMgr.add(self.char_ctrl.move_left, "MoveLeft")
        # Else, start rotating(!) to the left.
        else:
            self.core.taskMgr.add(self.char_ctrl.rotate_left, "RotateLeft")

    def a_up_handler(self):
        self.a_pressed = False

        # Stop moving/rotating to the left.
        self.core.taskMgr.remove("RotateLeft")
        self.core.taskMgr.remove("MoveLeft")

    def d_handler(self):
        self.d_pressed = True

        # Stop moving/rotating to the right.
        self.core.taskMgr.remove("RotateLeft")
        self.core.taskMgr.remove("MoveLeft")

        # If the mouse3 button is clicked, start moving(!) to the right.
        if self.mouse_3_clicked:
            self.core.taskMgr.add(self.char_ctrl.move_right, "MoveRight")
        # Else, start rotating(!) to the right.
        else:
            self.core.taskMgr.add(self.char_ctrl.rotate_right, "RotateRight")

    def d_up_handler(self):
        self.d_pressed = False

        # Stop moving/rotating to the right.
        self.core.taskMgr.remove("RotateRight")
        self.core.taskMgr.remove("MoveRight")

    def mouse_1_handler(self):
        self.mouse_1_clicked = True

        # Run the dragging handler.
        self.core.taskMgr.add(self.handle_m1_dragging_task, "M1Drag")

        # Start moving forward if both mouse buttons are clicked and 'w' wasn't already pressed.
        if self.mouse_3_clicked and not self.w_pressed:
            self.core.taskMgr.add(self.char_ctrl.move_forward, "MoveForward")

        # Hide the cursor.
        self.set_cursor_hidden(True)

        # Remember the position of mouse click.
        md = self.core.win.get_pointer(0)
        self.last_mouse_x = md.get_x()
        self.last_mouse_y = md.get_y()

    def mouse_1_up_handler(self):
        self.mouse_1_clicked = False

        self.core.win.move_pointer(0, int(self.last_mouse_x), int(self.last_mouse_y))

        # Show the cursor if neither of mouse buttons are clicked.
        if not self.mouse_3_clicked:
            self.set_cursor_hidden(False)

        # Stop moving forward in case both mouse buttons were clicked, but 'w' is still being pressed.
        if not self.w_pressed:
            self.core.taskMgr.remove("MoveForward")

    def mouse_3_handler(self):
        self.mouse_3_clicked = True
        self.core.taskMgr.add(self.handle_m3_dragging_task, "M3Drag")

        # Adjust the controlled character's rotation to the camera.
        self.char_ctrl.adjust_rotation_to_camera(self.cam_ctrl)

        # Move forward if both mouse buttons are clicked.
        if self.mouse_1_clicked:
            if not self.core.taskMgr.hasTaskNamed("MoveForward"):
                self.core.taskMgr.add(self.char_ctrl.move_forward, "MoveForward")

        # Switch to moving from rotating.
        if self.d_pressed:
            self.core.taskMgr.remove("RotateRight")
            self.core.taskMgr.add(self.char_ctrl.move_right, "MoveRight")
        if self.a_pressed:
            self.core.taskMgr.remove("RotateLeft")
            self.core.taskMgr.add(self.char_ctrl.move_left, "MoveLeft")

        # Hide the mouse.
        self.set_cursor_hidden(True)

        # Remember the position of mouse click.
        md = self.core.win.get_pointer(0)
        self.last_mouse_x = md.get_x()
        self.last_mouse_y = md.get_y()

    def mouse_3_up_handler(self):
        self.mouse_3_clicked = False

        # Switch from moving to rotating.
        if self.d_pressed:
            self.core.taskMgr.remove("MoveRight")
            self.core.taskMgr.add(self.char_ctrl.rotate_right, "RotateRight")
        if self.a_pressed:
            self.core.taskMgr.remove("MoveLeft")
            self.core.taskMgr.add(self.char_ctrl.rotate_left, "RotateLeft")

        self.core.win.move_pointer(0, int(self.last_mouse_x), int(self.last_mouse_y))
        # Show the cursor if neither of mouse buttons are clicked.
        if not self.mouse_1_clicked:
            self.set_cursor_hidden(False)

        # Stop moving forward in case both mouse buttons were clicked, but 'w' is still being pressed.
        if not self.w_pressed:
            self.core.taskMgr.remove("MoveForward")

    def wheel_up_handler(self):
        self.cam_ctrl.zoom_in()

    def wheel_down_handler(self):
        self.cam_ctrl.zoom_out()

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
        self.skirmish.interface.submodules[0].toggle()

    def handle_m1_dragging_task(self, task):
        # Move the camera on the character's "orbit" only if the first button of the mouse is clicked.
        if self.core.mouseWatcherNode.hasMouse() and self.mouse_1_clicked and not self.mouse_3_clicked:
            self.cam_ctrl.rotate_with_character = False
            md = self.core.win.getPointer(0)
            delta_x = md.get_x() - self.last_mouse_x
            delta_y = md.get_y() - self.last_mouse_y
            self.core.win.movePointer(0, int(self.last_mouse_x), int(self.last_mouse_y))
            self.cam_ctrl.move_on_horizontal_orbit(- delta_x * 0.3 * self.mouse_sensitivity)
            self.cam_ctrl.move_on_vertical_orbit(delta_y * 0.3 * self.mouse_sensitivity)
        elif not self.mouse_1_clicked:
            self.cam_ctrl.rotate_with_character = True
            return Task.done
        return Task.cont

    def handle_m3_dragging_task(self, task):
        # Rotate the player if the third mouse button is clicked.
        if self.core.mouseWatcherNode.hasMouse() and self.mouse_3_clicked:
            md = self.core.win.getPointer(0)
            delta_x = md.get_x() - self.last_mouse_x
            self.core.win.movePointer(0, int(self.last_mouse_x), int(self.last_mouse_y))
            self.char_ctrl.rotate_by_angle(-0.3 * self.mouse_sensitivity * delta_x)
        elif not self.mouse_3_clicked:
            return Task.done
        return Task.cont

    def set_cursor_hidden(self, value):
        props = WindowProperties()
        props.setCursorHidden(value)
        self.core.win.requestProperties(props)
