from client.local.model_config.actor_config import actor_config
from client.local.model_config.weapon_config import weapon_config
from direct.task.Task import Task
from client.local.section.main.scene.actor_manipulation.unit_interpolator import (
    UnitInterpolator,
)
from client.local.model_config.actor_config.animation import Animation
from client.local import core
from client.event import Event
from direct.showbase.DirectObject import DirectObject


class ActorManipulator(DirectObject):
    def __init__(self, model, node):
        DirectObject.__init__(self)
        self.model = model
        self.node = node

        self.accept(Event.NEW_UNIT_CREATED, self.handle_new_unit_created)
        self.accept(Event.UNIT_ANIMATION_UPDATED, self.handle_unit_animation_updated)
        self.accept(Event.UNIT_MODEL_UPDATED, self.handle_unit_model_updated)
        self.accept(Event.UNIT_WEAPON_UPDATED, self.handle_weapon_changed)

    def handle_new_unit_created(self, *args):
        unit = args[0]
        self.spawn_unit(unit)

    def handle_unit_animation_updated(self, *args):
        unit, loop = args
        self.change_animation(unit, unit.animation, loop)

    def handle_unit_model_updated(self, *args):
        unit = args[0]
        unit.actor.removePart("modelRoot")
        unit.actor = actor_config.load(unit.model)
        unit.actor.reparent_to(unit.base_node)
        self.change_animation(unit, Animation.STAND, 1)
        weapon = weapon_config.load(unit.weapon)
        self.equip_weapon(unit, weapon)

    def handle_weapon_changed(self, *args):
        unit, = args
        self.change_weapon(unit, unit.weapon)

    def spawn_unit(self, unit):
        unit.actor = actor_config.load(unit.model)
        weapon = weapon_config.load(unit.weapon)
        self.equip_weapon(unit, weapon)
        self.change_animation(unit, unit.animation, 1)
        unit.base_node = self.node.attach_new_node("actor base node")
        unit.base_node.set_pos_hpr(unit.x, unit.y, unit.z, unit.h, unit.p, unit.r)
        unit.actor.reparent_to(unit.base_node)
        unit.actor.set_blend(frameBlend=True)
        if unit != self.model.player_unit:
            unit.interpolator = UnitInterpolator(unit)
            unit.interpolator.update()
            task = Task(self.update_position_task)
            core.instance.task_mgr.add(
                task, f"interpolate{unit}", extraArgs=[unit, task]
            )

    def move_rotate_character(self, unit, x, y, z, h, p, r):
        unit.base_node.set_pos_hpr(x, y, z, h, p, r)

    def change_animation(self, unit, animation, loop):
        animation = actor_config.get_anim_name(unit.model, animation)
        if loop:
            unit.actor.loop(animation)
        else:
            unit.actor.play(animation)

    def equip_weapon(self, unit, weapon):
        unit.hand_node = unit.actor.expose_joint(None, "modelRoot", "Weapon_R_Bone")
        weapon.reparent_to(unit.hand_node)
        unit.weapon_node = weapon

    def change_weapon(self, unit, weapon):
        unit.weapon_node.detach_node()
        unit.weapon_node = weapon_config.load(unit.weapon)
        unit.weapon_node.reparent_to(unit.hand_node)

    def update_position_task(self, unit, task):
        unit.interpolator.interpolate()
        return Task.cont
