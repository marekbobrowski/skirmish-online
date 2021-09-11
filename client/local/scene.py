from local import core, model
from local import asset_names as assets
from event import Event
from local.subpart import Subpart
from local.animation import Animation
from local.floating_bars import FloatingBars

from panda3d.core import PointLight, AmbientLight
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import *


class Scene(DirectObject):
    def __init__(self):
        DirectObject.__init__(self)
        self.node = core.instance.render.attach_new_node("scene node")
        self.characters = {}
        # scene has to handle the event first, before the floating bars
        self.accept(Event.PLAYER_JOINED, self.spawn_player_character)
        self.accept(Event.PLAYER_CHANGED_POS_HPR, self.move_rotate_character)
        self.accept(Event.PLAYER_CHANGED_ANIMATION, self.change_animation)
        self.floating_bars = FloatingBars(self.characters)

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

    def spawn_player_character(self, player):
        character = model.load_model_config(player.model)
        # character.loop(player.animation, Subpart.LEGS)
        # character.loop(player.animation, Subpart.TORSO)
        wep = core.instance.loader.loadModel(assets.weapon_1)
        hand = character.expose_joint(None, "modelRoot", "Weapon_R_Bone")
        wep.reparent_to(hand)
        character.set_pos_hpr(player.x,
                              player.y,
                              player.z,
                              player.h,
                              player.p,
                              player.r)
        character.reparent_to(self.node)
        character.set_blend(frameBlend=True)
        character.set_light_off(1)
        self.characters[player.id] = character

    def move_rotate_character(self, id_, x, y, z, h, p, r):
        char = self.characters.get(id_, None)
        if char is not None:
            char.set_pos_hpr(x, y, z, h, p, r)

    def change_animation(self, char, id_, animation, loop):
        animation = model.get_anim_name(0, animation)
        if char is None:
            char = self.characters.get(id_, None)
        if char is not None:
            play_only_torso = False
            if char.get_current_anim(partName=Subpart.LEGS) == Animation.RUN:
                play_only_torso = True
            if loop:
                play_func = self.test_loop
            else:
                play_func = self.test_play
            if play_only_torso:
                Sequence(
                    Func(play_func, char, animation, 1, Subpart.TORSO),
                    Func(self.resume_stand_run, [char])
                ).start()
            else:
                Sequence(
                    Func(play_func, char, animation, 1, Subpart.TORSO),
                    Func(play_func, char, animation, 1, Subpart.LEGS),
                    Func(self.resume_stand_run, [char])
                ).start()

    def resume_stand_run(self, char):
        pass

    def test_play(self, char, animation, xd, part):
        char.play(animation, xd, part)

    def test_loop(self, char, animation, xd, part):
        char.loop(animation, xd, part)

