from client.local import core
from client.local.assets import asset_names as assets


class Terrain:
    def __init__(self, node):
        self.node = node
        terrain = core.instance.loader.loadModel(assets.arena)
        terrain.reparent_to(self.node)
        terrain.set_scale(10)
        terrain.set_z(0.82)
