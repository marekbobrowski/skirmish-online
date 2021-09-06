from local import core
from local import asset_names as assets
from event import Event
from local.model_config import model
from local.scene.floating_bars import FloatingBars

from panda3d.core import PointLight, AmbientLight
from panda3d.core import BitMask32
from direct.showbase.DirectObject import DirectObject


class Scene(DirectObject):
    def __init__(self):
        DirectObject.__init__(self)
        self.node = core.instance.render.attach_new_node("scene node")
        self.characters = {}
        # scene has to handle the event first, before the floating bars
        self.accept(Event.PLAYER_JOINED, self.spawn_player_character)
        self.accept(Event.PLAYER_CHANGED_POS_HPR, self.move_rotate_character)
        self.floating_bars = FloatingBars(self.characters)

        # those will be parented to the scene graph so need to keep the references
        skybox = core.instance.loader.loadModel(assets.skybox)
        skybox.set_scale(100)
        skybox.reparent_to(core.instance.camera)
        skybox.set_compass(core.instance.render)

        terrain = core.instance.loader.loadModel(assets.terrain)
        terrain.reparent_to(self.node)
        terrain.set_scale(100)
        terrain.set_z(4)

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
        character.loop(player.animation)
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
        char = self.characters[id_]
        char.set_pos_hpr(x, y, z, h, p, r)
