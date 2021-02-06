from direct.gui.OnscreenImage import OnscreenImage


class Zone:
    def __init__(self, core, parent_3d, parent_2d):
        self.core = core
        assets_dir = core.assets_dir
        self.zone_3d = parent_3d.attach_new_node("zone_3d")
        self.zone_2d = parent_2d.attach_new_node("zone_3d")

        self.terrain = core.loader.load_model(assets_dir + 'models/terrain.egg')
        self.terrain.reparent_to(self.zone_3d)

        self.tower = core.loader.load_model(assets_dir + 'models/tower.egg')
        self.tower.reparent_to(self.zone_3d)
        self.tower.set_scale(0.5)
        self.tower.set_pos(5, 5, 0.4)

        self.tower2 = core.loader.load_model(assets_dir + 'models/tower2.egg')
        self.tower2.reparent_to(self.zone_3d)
        self.tower2.set_scale(0.15)
        self.tower2.set_pos(-1, -3.5, 0.7)
        self.tower2.set_h(30)

        self.background_image = OnscreenImage(parent=self.zone_2d, image=assets_dir+'artwork/map_background.jpg')

    def reparent_to(self, loader, parent_3d, parent_2d):
        self.zone_3d.reparent_to(loader, parent_3d, parent_2d)

