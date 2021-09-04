from local import core
from local import asset_names as assets
from panda3d.core import PointLight, AmbientLight
from panda3d.core import BitMask32

class Scene:
    def __init__(self, world):
        self.world = world
        self.node = core.instance.render.attach_new_node("scene node")

        self.skybox = core.instance.loader.loadModel(assets.skybox)
        self.skybox.set_scale(100)
        self.skybox.reparent_to(core.instance.camera)
        self.skybox.set_compass(core.instance.render)

        self.terrain = core.instance.loader.loadModel(assets.terrain)
        self.terrain.reparent_to(self.node)
        self.terrain.set_scale(100)
        self.terrain.set_z(4)

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

        core.instance.accept('player-base-updated', self.update_players_view)

    def update_players_view(self):
        all_players = self.world.other_players.copy()
        all_players.append(self.world.player)
        for player in all_players:
            if player.character.parent is None:
                player.character.reparent_to(core.instance.render)
                player.character.loop('stand')
                player.character.set_blend(frameBlend=True)
                player.character.set_light_off(1)
                player.character.show()

    def set_up_camera(self):
        core.instance.camera.reparent_to(self.world.player.character)


