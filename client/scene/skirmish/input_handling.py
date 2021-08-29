from direct.task.Task import Task
from direct.interval.IntervalGlobal import *
from direct.interval.ActorInterval import ActorInterval
from panda3d.core import WindowProperties
from networking import networking_manager
import core


import datetime


class InputHandling:

    def __init__(self, skirmish):
        self.skirmish = skirmish

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
        self.mouse_1_click_time = 0

        # Assignment of handling functions.
        self.event_handler_mapping = {
            'w': self.w_handler,
            'w-up': self.w_up_handler,
            's': self.s_handler,
            's-up': self.s_up_handler,
            'a': self.a_handler,
            'a-up': self.a_up_handler,
            'd': self.d_handler,
            'd-up': self.d_up_handler,
            'mouse1': self.mouse_1_handler,
            'mouse1-up': self.mouse_1_up_handler,
            'mouse3': self.mouse_3_handler,
            'mouse3-up': self.mouse_3_up_handler,
            'wheel_up': self.wheel_up_handler,
            'wheel_down': self.wheel_down_handler,
            'q': self.q_handler,
            'q-up': self.q_up_handler,
            'e': self.e_handler,
            'e-up': self.e_up_handler,
            'r': self.r_handler,
            'f': self.f_handler,
            'escape': self.esc_handler,
            'enter': self.enter_handler
        }
        self.enable()

    def enable(self):
        for event, handler in self.event_handler_mapping.items():
            core.instance.accept(event, handler)

    def disable(self):
        for event, handler in self.event_handler_mapping.items():
            core.instance.ignore(event)

    def w_handler(self):
        self.w_pressed = True
        core.instance.taskMgr.remove("MoveBackward")
        # Start moving if the character is not moving yet (mouse buttons allow to move, so we have to check).
        if not core.instance.taskMgr.hasTaskNamed("MoveForward"):
            core.instance.taskMgr.add(self.char_ctrl.move_forward, "MoveForward")
        self.update_animation()

    def w_up_handler(self):
        self.w_pressed = False
        # Stop moving if not both mouse buttons are clicked.
        if not (self.mouse_1_clicked and self.mouse_3_clicked):
            core.instance.taskMgr.remove("MoveForward")
        self.update_animation()

    def s_handler(self):
        # Stop moving forward.
        core.instance.taskMgr.remove("MoveForward")
        # Start moving backward.
        core.instance.taskMgr.add(self.char_ctrl.move_backward, "MoveBackward")
        self.update_animation()

    def s_up_handler(self):
        # Stop moving backward.
        core.instance.taskMgr.remove("MoveBackward")
        self.update_animation()

    def a_handler(self):
        self.a_pressed = True
        # Stop rotating to the right.
        core.instance.taskMgr.remove("RotateRight")
        core.instance.taskMgr.remove("MoveRight")

        # If the mouse3 button is clicked, start moving(!) to the left.
        if self.mouse_3_clicked:
            core.instance.taskMgr.add(self.char_ctrl.move_left, "MoveLeft")
        # Else, start rotating(!) to the left.
        else:
            core.instance.taskMgr.add(self.char_ctrl.rotate_left, "RotateLeft")

        self.update_animation()

    def a_up_handler(self):
        self.a_pressed = False

        # Stop moving/rotating to the left.
        core.instance.taskMgr.remove("RotateLeft")
        core.instance.taskMgr.remove("MoveLeft")
        self.update_animation()

    def d_handler(self):
        self.d_pressed = True

        # Stop moving/rotating to the right.
        core.instance.taskMgr.remove("RotateLeft")
        core.instance.taskMgr.remove("MoveLeft")

        # If the mouse3 button is clicked, start moving(!) to the right.
        if self.mouse_3_clicked:
            core.instance.taskMgr.add(self.char_ctrl.move_right, "MoveRight")
        # Else, start rotating(!) to the right.
        else:
            core.instance.taskMgr.add(self.char_ctrl.rotate_right, "RotateRight")
        self.update_animation()

    def d_up_handler(self):
        self.d_pressed = False

        # Stop moving/rotating to the right.
        core.instance.taskMgr.remove("RotateRight")
        core.instance.taskMgr.remove("MoveRight")
        self.update_animation()

    def mouse_1_handler(self):
        self.mouse_1_clicked = True
        self.mouse_1_click_time = datetime.datetime.now()
        self.skirmish.object_picking.find_pickable()

        # Run the dragging handler.
        core.instance.taskMgr.add(self.handle_m1_dragging_task, "M1Drag")

        # Start moving forward if both mouse buttons are clicked and 'w' wasn't already pressed.
        if self.mouse_3_clicked and not self.w_pressed:
            core.instance.taskMgr.add(self.char_ctrl.move_forward, "MoveForward")

        # Hide the cursor.
        self.set_cursor_hidden(True)

        # Remember the position of mouse click.
        md = core.instance.win.get_pointer(0)
        self.last_mouse_x = md.get_x()
        self.last_mouse_y = md.get_y()
        self.update_animation()

    def mouse_1_up_handler(self):
        self.mouse_1_clicked = False
        if (datetime.datetime.now() - self.mouse_1_click_time).microseconds < 100000:
            self.skirmish.object_picking.pick()

        core.instance.win.move_pointer(0, int(self.last_mouse_x), int(self.last_mouse_y))

        # Show the cursor if neither of mouse buttons are clicked.
        if not self.mouse_3_clicked:
            self.set_cursor_hidden(False)

        # Stop moving forward in case both mouse buttons were clicked, but 'w' is still being pressed.
        if not self.w_pressed:
            core.instance.taskMgr.remove("MoveForward")
        self.update_animation()

    def mouse_3_handler(self):
        self.mouse_3_clicked = True
        core.instance.taskMgr.add(self.handle_m3_dragging_task, "M3Drag")

        # Adjust the controlled character's rotation to the camera.
        self.char_ctrl.adjust_rotation_to_camera(self.cam_ctrl)

        # Move forward if both mouse buttons are clicked.
        if self.mouse_1_clicked:
            if not core.instance.taskMgr.hasTaskNamed("MoveForward"):
                core.instance.taskMgr.add(self.char_ctrl.move_forward, "MoveForward")

        # Switch to moving from rotating.
        if self.d_pressed:
            core.instance.taskMgr.remove("RotateRight")
            core.instance.taskMgr.add(self.char_ctrl.move_right, "MoveRight")
        if self.a_pressed:
            core.instance.taskMgr.remove("RotateLeft")
            core.instance.taskMgr.add(self.char_ctrl.move_left, "MoveLeft")

        # Hide the mouse.
        self.set_cursor_hidden(True)

        # Remember the position of mouse click.
        md = core.instance.win.get_pointer(0)
        self.last_mouse_x = md.get_x()
        self.last_mouse_y = md.get_y()
        self.update_animation()

    def mouse_3_up_handler(self):
        self.mouse_3_clicked = False

        # Switch from moving to rotating.
        if self.d_pressed:
            core.instance.taskMgr.remove("MoveRight")
            core.instance.taskMgr.add(self.char_ctrl.rotate_right, "RotateRight")
        if self.a_pressed:
            core.instance.taskMgr.remove("MoveLeft")
            core.instance.taskMgr.add(self.char_ctrl.rotate_left, "RotateLeft")

        core.instance.win.move_pointer(0, int(self.last_mouse_x), int(self.last_mouse_y))
        # Show the cursor if neither of mouse buttons are clicked.
        if not self.mouse_1_clicked:
            self.set_cursor_hidden(False)

        # Stop moving forward in case both mouse buttons were clicked, but 'w' is still being pressed.
        if not self.w_pressed:
            core.instance.taskMgr.remove("MoveForward")
        self.update_animation()

    def wheel_up_handler(self):
        self.cam_ctrl.zoom_in(1)

    def wheel_down_handler(self):
        self.cam_ctrl.zoom_out(1)

    def q_handler(self):
        if self.skirmish.player.target is not None:
            self.skirmish.abilities.trigger_cooldown(0)
            networking_manager.instance.skirmish_sender.send_ability_attempt(0, self.skirmish.player.target.id)

    def q_up_handler(self):
        pass

    def e_handler(self):
        if self.skirmish.player.target is not None:
            self.skirmish.abilities.trigger_cooldown(1)
            networking_manager.instance.skirmish_sender.send_ability_attempt(1, self.skirmish.player.target.id)

    def e_up_handler(self):
        pass

    def r_handler(self):
        if self.skirmish.player.target is not None:
            self.skirmish.abilities.trigger_cooldown(2)
            networking_manager.instance.skirmish_sender.send_ability_attempt(2, self.skirmish.player.target.id)

    def f_handler(self):
        if self.skirmish.player.target is not None:
            self.skirmish.abilities.trigger_cooldown(3)
            networking_manager.instance.skirmish_sender.send_ability_attempt(3, self.skirmish.player.target.id)

    def esc_handler(self):
        self.skirmish.interface.submodules[0].toggle()

    def enter_handler(self):
        chat_frame = self.skirmish.interface.submodules[3]
        if chat_frame.focused:
            message = chat_frame.entry.get()
            if message == '':
                return
            networking_manager.instance.skirmish_sender.send_chat_message(message)
            chat_frame.remove_focus()
        else:
            chat_frame.focus()

    def handle_m1_dragging_task(self, task):
        # Move the camera on the character's "orbit" only if the first button of the mouse is clicked.
        if core.instance.mouseWatcherNode.hasMouse() and self.mouse_1_clicked and not self.mouse_3_clicked:
            self.cam_ctrl.rotate_with_character = False
            md = core.instance.win.getPointer(0)
            delta_x = md.get_x() - self.last_mouse_x
            delta_y = md.get_y() - self.last_mouse_y
            core.instance.win.movePointer(0, int(self.last_mouse_x), int(self.last_mouse_y))
            self.cam_ctrl.move_on_horizontal_orbit(- delta_x * 0.3 * self.mouse_sensitivity)
            self.cam_ctrl.move_on_vertical_orbit(delta_y * 0.3 * self.mouse_sensitivity)
        elif not self.mouse_1_clicked:
            self.cam_ctrl.rotate_with_character = True
            return Task.done
        return Task.cont

    def handle_m3_dragging_task(self, task):
        # Rotate the player if the third mouse button is clicked.
        if core.instance.mouseWatcherNode.hasMouse() and self.mouse_3_clicked:
            md = core.instance.win.getPointer(0)
            delta_x = md.get_x() - self.last_mouse_x
            core.instance.win.movePointer(0, int(self.last_mouse_x), int(self.last_mouse_y))
            self.char_ctrl.rotate_by_angle(-0.3 * self.mouse_sensitivity * delta_x)
        elif not self.mouse_3_clicked:
            return Task.done
        return Task.cont

    def set_cursor_hidden(self, value):
        props = WindowProperties()
        props.setCursorHidden(value)
        core.instance.win.requestProperties(props)

    def update_animation(self):
        f = core.instance.task_mgr.hasTaskNamed
        if f("MoveRight"):
            if self.char_ctrl.character.get_current_anim() != 'strafe_right':
                networking_manager.instance.skirmish_sender.send_animation('strafe_right', 1)
                self.char_ctrl.character.loop('strafe_right')
        elif f("MoveLeft"):
            if self.char_ctrl.character.get_current_anim() != 'strafe_left':
                networking_manager.instance.skirmish_sender.send_animation('strafe_left', 1)
                self.char_ctrl.character.loop('strafe_left')
        elif f("MoveForward") or f("MoveBackward"):
            if self.char_ctrl.character.get_current_anim() != 'run':
                self.char_ctrl.character.loop('run')
                networking_manager.instance.skirmish_sender.send_animation('run', 1)
        else:
            if self.char_ctrl.character.get_current_anim() != 'idle':
                self.char_ctrl.character.loop('idle')
                networking_manager.instance.skirmish_sender.send_animation('idle', 1)
