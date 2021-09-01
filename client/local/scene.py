from local import core
from local import asset_names as assets


class Scene:
    def __init__(self):
        self.skybox = core.instance.loader.loadModel(assets.skybox)
        self.skybox.set_scale(100)
        self.skybox.reparent_to(core.instance.camera)
        self.skybox.set_compass(core.instance.render)
        self.terrain = None
