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

    def update(self):
        all_players = self.world.other_players.copy()
        all_players.append(self.world.player)
        for player in all_players:
            if player.character.get_parent() is None:
                player.character.reparent_to(core.instance.render)

    def set_up_camera(self):
        core.instance.camera.reparent_to(self.world.player.character)


