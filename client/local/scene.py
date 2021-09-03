from local import core
from local import asset_names as assets


class Scene:
    def __init__(self, world):
        self.world = world
        self.node = core.instance.render.attach_new_node("scene node")

        self.skybox = core.instance.loader.loadModel(assets.skybox)
        self.skybox.set_scale(100)
        self.skybox.reparent_to(core.instance.camera)
        self.skybox.set_compass(core.instance.render)
        self.terrain = None
        core.instance.accept('player-base-updated', self.update_players_view)

    def update_players_view(self):
        all_players = self.world.other_players.copy()
        all_players.append(self.world.player)
        for player in all_players:
            if player.character.parent is None:
                player.character.reparent_to(core.instance.render)
                player.character.loop('stand')
                player.character.set_blend(frameBlend=True)
                player.character.show()

    def set_up_camera(self):
        core.instance.camera.reparent_to(self.world.player.character)


