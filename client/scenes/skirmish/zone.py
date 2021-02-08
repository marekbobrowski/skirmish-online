from direct.gui.OnscreenImage import OnscreenImage


class Zone:
    def __init__(self, core, parent_3d, parent_2d):
        self.core = core

        self.node_3d = parent_3d.attach_new_node("zone 3d node")
        self.node_2d = parent_2d.attach_new_node("zone 2d node")
        # self.terrain = None
        # self.tower = None
        # self.tower2 = None
        # self.background_image = None

    def load(self):
        assets_dir = self.core.assets_dir
        # self.terrain = self.core.loader.load_model(assets_dir + 'models/terrain.egg')
        # self.terrain.reparent_to(self.node_3d)

        # self.tower = self.core.loader.load_model(assets_dir + 'models/tower.egg')
        # self.tower.reparent_to(self.node_3d)
        # self.tower.set_scale(0.5)
        # self.tower.set_pos(5, 5, 0.4)

        # self.tower2 = self.core.loader.load_model(assets_dir + 'models/tower2.egg')
        # self.tower2.reparent_to(self.node_3d)
        # self.tower2.set_scale(0.15)
        # self.tower2.set_pos(-1, -3.5, 0.7)
        # self.tower2.set_h(30)

        # self.background_image = OnscreenImage(parent=self.node_2d, image=assets_dir + 'artwork/map_background.jpg')


