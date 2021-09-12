from local import core, actor_config, weapon_config
from local import asset_names as assets
from event import Event
from local.subpart import Subpart
from local.animation import Animation
from local.floating_bars import FloatingBars

from panda3d.core import PointLight, AmbientLight
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import *


class World(DirectObject):
    def __init__(self):
        DirectObject.__init__(self)
        self.node = core.instance.render.attach_new_node("scene node")
        self.main_player_id = None
        self.units = {}

        # scene has to handle the event first, before the floating bars
        self.accept(Event.PLAYER_JOINED, self.handle_player_joined)
        self.accept(Event.PLAYER_CHANGED_POS_HPR, self.handle_player_changed_pos_hpr)
        self.accept(Event.PLAYER_CHANGED_ANIMATION, self.handle_player_changed_animation)

        self.floating_bars = FloatingBars(self.units)

        # those will be parented to the scene graph so need to keep the references
        skybox = core.instance.loader.loadModel(assets.skybox)
        skybox.set_scale(100)
        skybox.reparent_to(core.instance.camera)
        skybox.set_compass(core.instance.render)

        terrain = core.instance.loader.loadModel(assets.arena)
        terrain.reparent_to(self.node)
        terrain.set_scale(10)
        terrain.set_z(0.82)

        plight = PointLight('plight')
        plight.setColor((5, 5, 5, 0))
        plight_node_path = self.node.attachNewNode(plight)
        plight_node_path.setPos(20, 0, 0)
        core.instance.render.setLight(plight_node_path)

        alight = AmbientLight('alight')
        alight.setColor((1, 1, 1, 0))
        alight_node_path = self.node.attachNewNode(alight)
        alight_node_path.setPos(20, 0, 0)
        core.instance.render.setLight(alight_node_path)

    def handle_player_joined(self, args):
        self.spawn_unit(args.unit)

    def handle_player_changed_pos_hpr(self, args):
        unit = self.units.get(args.id_, None)
        if unit is not None:
            self.move_rotate_character(unit,
                                       args.x,
                                       args.y,
                                       args.z,
                                       args.h,
                                       args.p,
                                       args.r)

    def handle_player_changed_animation(self, args):
        unit = self.units.get(args.id_, None)
        self.change_animation(unit, args.animation, args.loop)

    def spawn_unit(self, unit):
        unit.actor = actor_config.load(unit.model)
        weapon = weapon_config.load(unit.weapon)
        self.equip_weapon(unit, weapon)
        self.change_animation(unit, unit.animation, 1)
        unit.actor.set_pos_hpr(unit.x,
                               unit.y,
                               unit.z,
                               unit.h,
                               unit.p,
                               unit.r)
        unit.actor.reparent_to(self.node)
        unit.actor.set_blend(frameBlend=True)
        unit.actor.set_light_off(1)
        self.units[unit.id] = unit

    def move_rotate_character(self, unit, x, y, z, h, p, r):
        unit.actor.set_pos_hpr(x, y, z, h, p, r)

    def change_animation(self, unit, animation, loop):
        animation = actor_config.get_anim_name(unit.model, animation)
        if loop:
            unit.actor.loop(animation)
        else:
            unit.actor.play(animation)
        #
        # return
        # play_only_torso = False
        # if unit.actor.get_current_anim(partName=Subpart.LEGS) == Animation.RUN:
        #     play_only_torso = True
        # if loop:
        #     play_func = self.test_loop
        # else:
        #     play_func = self.test_play
        # if play_only_torso:
        #     Sequence(
        #         Func(play_func, unit.actor, animation, 1, Subpart.TORSO),
        #         Func(self.resume_stand_run, [unit.actor])
        #     ).start()
        # else:
        #     Sequence(
        #         Func(play_func, unit.actor, animation, 1, Subpart.TORSO),
        #         Func(play_func, unit.actor, animation, 1, Subpart.LEGS),
        #         Func(self.resume_stand_run, [unit.actor])
        #     ).start()

    def equip_weapon(self, unit, weapon):
        hand = unit.actor.expose_joint(None, "modelRoot", "Weapon_R_Bone")
        weapon.reparent_to(hand)

    def resume_stand_run(self, char):
        pass

    def test_play(self, char, animation, xd, part):
        char.play(animation, xd, part)

    def test_loop(self, char, animation, xd, part):
        char.loop(animation, xd, part)

