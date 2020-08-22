from direct.gui.OnscreenImage import OnscreenImage


class CharacterPreparation:
    def __init__(self, client):
        self.client = client
        self.client.disable_mouse()
        self.client.camera.set_pos(-3.3, -5.3, 1)
        self.client.camera.set_h(-50)
        self.client.map.terrain = self.client.loader.load_model('models/terrain.egg')
        self.client.map.terrain.reparent_to(self.client.render)
        self.client.map.tower = self.client.loader.load_model('models/tower.egg')
        self.client.map.tower.reparent_to(self.client.render)
        self.client.map.tower.set_scale(0.5)
        self.client.map.tower.set_pos(5, 5, 0.4)
        self.client.map.tower2 = self.client.loader.load_model('models/tower2.egg')
        self.client.map.tower2.reparent_to(self.client.render)
        self.client.map.tower2.set_scale(0.15)
        self.client.map.tower2.set_pos(-1, -3.5, 0.7)
        self.client.map.tower2.set_h(30)
        self.client.map.background_image = OnscreenImage(parent=render2d, image="artwork/map_background.jpg")
        self.client.map.background_image.set_scale(1)
        base.cam.node().getDisplayRegion(0).setSort(20)
        self.client.main_menu.hide()

