from direct.showbase.ShowBaseGlobal import globalClock
from direct.task import Task


class CharacterControl:

    def __init__(self, actor, parent_node):
        self.actor = actor
        self.control_node = parent_node.attach_new_node("actor control node")
        self.control_node.set_pos(actor.get_pos(parent_node))
        self.control_node.set_hpr(actor.get_hpr(parent_node))
        self.actor.reparent_to(self.control_node)
        self.actor.set_pos(0, 0, 0)
        self.actor.set_hpr(0, 0, 0)
        self.movement_speed = 2.8

    def move_forward(self, task):
        self.control_node.set_y(self.control_node, -self.movement_speed * globalClock.getDt())
        self.actor.set_h(0)
        return Task.cont

    def move_backward(self, task):
        self.control_node.set_y(self.control_node, self.movement_speed * globalClock.getDt())
        self.actor.set_h(180)
        return Task.cont

    def move_left(self, task):
        self.control_node.set_x(self.control_node, self.movement_speed * 0.7 * globalClock.getDt())
        self.actor.set_h(90)
        return Task.cont

    def move_right(self, task):
        self.control_node.set_x(self.control_node, -self.movement_speed * 0.7 * globalClock.getDt())
        self.actor.set_h(-90)
        return Task.cont

    def rotate_left(self, task):
        self.control_node.set_h(self.control_node, self.movement_speed * 80 * globalClock.getDt())
        return Task.cont

    def rotate_right(self, task):
        self.control_node.set_h(self.control_node, -self.movement_speed * 80 * globalClock.getDt())
        return Task.cont

    def rotate_by_angle(self, angle):
        self.control_node.set_h(self.control_node.get_h() + angle)

    def adjust_rotation_to_camera(self, cam_ctrl):
        rel_hook_hpr = cam_ctrl.hook.get_hpr(self.control_node.get_parent())
        self.control_node.set_h(rel_hook_hpr.get_x())
        cam_ctrl.hook.set_hpr(self.control_node.get_parent(), rel_hook_hpr)