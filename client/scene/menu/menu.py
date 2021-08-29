from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from scene.menu.audio_submenu import AudioSubmenu
from scene.menu.main_menu import MainMenu
import assets_dir_config
import core


class Menu:
    def __init__(self):
        self.node = core.instance.aspect2d.attach_new_node("Menu Node")
        self.node.hide()

        self.subscene_mapping = {
            0: MainMenu(self),
            1: AudioSubmenu(self)
        }

        # Menu graphical/sound components
        self.background = None
        self.font = None
        self.logo_text = None
        self.rollover_sound = None
        self.click_sound = None

        self.current_subscene = None
        self.is_loaded = False

    def load(self):
        assets_dir = assets_dir_config.assets_dir
        self.background = OnscreenImage(parent=core.instance.render2d,
                                        image=assets_dir + 'artwork/menu_background.jpg')
        self.font = core.instance.loader.load_font(assets_dir + 'fonts/GODOFWAR.TTF')
        self.font.set_pixels_per_unit(100)
        self.logo_text = OnscreenText(text='Skirmish Online',
                                      font=self.font,
                                      pos=(0, 0.7),
                                      scale=0.2,
                                      parent=self.node)
        self.rollover_sound = core.instance.loader.loadSfx(assets_dir + 'sounds/mouse_rollover.wav')
        self.click_sound = core.instance.loader.loadSfx(assets_dir + 'sounds/mouse_click.wav')

        for scene in self.subscene_mapping.values():
            scene.load()
        self.is_loaded = True

    def enter(self):
        self.node.show()
        self.background.show()
        self.change_subscene_to(0)

    def leave(self):
        self.node.hide()
        self.background.hide()

    def change_subscene_to(self, scene_number):
        if self.current_subscene is not None:
            self.current_subscene.leave()
        self.current_subscene = self.subscene_mapping.get(scene_number)
        self.subscene_mapping.get(scene_number).enter()






