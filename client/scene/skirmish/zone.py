from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import GeoMipTerrain
import assets_dir_config
import core


class Zone:
    def __init__(self, parent, parent_3d, parent_2d):
        self.parent = parent
        self.parent_3d = parent_3d
        self.skybox = None

        self.node_3d = parent_3d.attach_new_node("zone 3d node")
        self.node_2d = parent_2d.attach_new_node("zone 2d node")
        # self.terrain = GeoMipTerrain('terrain')
        # self.terrain.setHeightfield(config.models_dir + 'tex/HF.bmp')
        # self.terrain.set_color_map(config.models_dir + 'tex/TX.bmp')
        #
        # self.terrain.set_block_size(32)
        # self.terrain.set_near(10)
        # self.terrain.set_far(20)
        # self.terrain.set_focal_point(self.core.camera)

        # self.terrain.get_root().set_sx(1)
        # self.terrain.get_root().set_sy(1)
        # self.terrain.get_root().set_pos(-50, -50, 0)
        # self.terrain.getRoot().reparentTo(self.parent_3d)
        # self.terrain.get_root().set_sz(20)



        # self.terrain.generate()
        # self.terrain = None
        # self.tower = None
        # self.tower2 = None
        # self.background_image = None

    def load(self):
        self.skybox = core.instance.loader.loadModel(assets_dir_config.models_dir + 'skybox')
        self.skybox.set_scale(100)
        self.skybox.reparent_to(core.instance.camera)
        self.skybox.set_compass(self.parent_3d)
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


