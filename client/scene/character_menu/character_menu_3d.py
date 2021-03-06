from direct.actor.Actor import Actor
from scene.skirmish.zone import Zone
import config


class CharacterMenu3D:
    """
    The 3d submodule of the character menu. Displays the chosen class representative and the scenery.
    """
    def __init__(self, char_menu):
        self.char_menu = char_menu
        self.core = char_menu.core
        self.node = char_menu.node_3d
        self.characters = []
        self.zone = Zone(self, self.node, self.char_menu.core.render2dp)

    def load(self):
        """
        Loads the 3d models of the scene and places everything in the proper position (including the camera).
        """
        self.core.camera.set_pos(-2.9, -4.9, 0.94)
        self.core.camera.set_h(-50)

        self.zone.load()
        self.core.cam2dp.node().getDisplayRegion(0).setSort(-20)

        hero_1 = Actor(config.heroes[0])
        hero_1.load_anims({'idle': config.animations_dir + 'idle_1'})
        hero_1.loop('idle')
        hero_1.reparent_to(self.node)
        hero_1.set_scale(0.25)
        hero_1.set_pos(-2.0, -4.1, 0.7)
        hero_1.set_h(-60)
        self.characters.append(hero_1)

        hero_2 = Actor(config.heroes[1])
        hero_2.load_anims({'idle': config.animations_dir + 'idle_2'})
        hero_2.loop('idle')
        hero_2.reparent_to(self.node)
        hero_2.set_scale(0.25)
        hero_2.set_pos(-1.96, -4.06, 0.7)
        hero_2.set_h(-60)
        self.characters.append(hero_2)

        # skybox = self.core.loader.loadModel(config.models_dir + 'skybox')
        # skybox.reparent_to(self.node)
        # skybox.set_scale(100)

    def position_camera(self):
        """
        Positions the camera for the character menu scene.
        """
        self.char_menu.core.camera.reparent_to(self.char_menu.core.render)
        self.char_menu.core.camera.set_pos(-2.9, -4.9, 0.94)
        self.char_menu.core.camera.set_hpr(-50, 0, 0)

    def refresh(self):
        """
        Refreshes the scene by showing the chosen class representative and hiding the rest.
        """
        for repr_ in self.characters:
            repr_.hide()
        self.characters[self.char_menu.selected_class].show()
        self.node.show()
        self.position_camera()


