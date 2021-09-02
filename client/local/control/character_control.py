from direct.showbase.ShowBaseGlobal import globalClock
from direct.task import Task
from direct.interval.IntervalGlobal import *


class CharacterControl:

    def __init__(self, character, core):
        self.core = core
        self.character = character
        self.movement_speed = 10

    def move_forward(self, task):
        self.character.set_y(self.character, -self.movement_speed * globalClock.getDt())
        return Task.cont

    def move_backward(self, task):
        self.character.set_y(self.character, self.movement_speed * globalClock.getDt())
        return Task.cont

    def move_left(self, task):
        self.character.set_x(self.character, self.movement_speed * 0.7 * globalClock.getDt())
        return Task.cont

    def move_right(self, task):
        self.character.set_x(self.character, -self.movement_speed * 0.7 * globalClock.getDt())
        return Task.cont

    def rotate_left(self, task):
        self.character.set_h(self.character, self.movement_speed * 10 * globalClock.getDt())
        return Task.cont

    def rotate_right(self, task):
        self.character.set_h(self.character, -self.movement_speed * 10 * globalClock.getDt())
        return Task.cont

    def rotate_by_angle(self, angle):
        self.character.set_h(self.character.get_h() + angle)

    def adjust_rotation_to_camera(self, cam_ctrl):
        rel_hook_hpr = cam_ctrl.hook.get_hpr(self.character.get_parent())
        self.character.set_h(rel_hook_hpr.get_x())
        cam_ctrl.hook.set_hpr(self.character.get_parent(), rel_hook_hpr)