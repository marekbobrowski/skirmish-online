from client.local import core
from client.local.assets import asset_names as assets


class Skybox:
    def __init__(self, node):
        self.node = node
        skybox = core.instance.loader.loadModel(assets.skybox)
        skybox.set_scale(100)
        skybox.reparent_to(core.instance.camera)
        skybox.set_compass(core.instance.render)
