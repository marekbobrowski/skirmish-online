from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
import assets_dir_config
import core


class LoadingScreen:

    def __init__(self):
        self._is_loaded = False
        self.node = core.instance.aspect2d.attach_new_node("loading screen node")

        self.game_label = None
        self.font = None
        self.background = None
        self.loading_label = None
        self.is_loaded = False

    def load(self):
        assets_dir = assets_dir_config.assets_dir
        self.background = OnscreenImage(parent=core.instance.render2d,
                                        image=assets_dir + 'artwork/menu_background.jpg')
        self.font = core.instance.loader.load_font(assets_dir + 'fonts/GODOFWAR.TTF')
        self.game_label = OnscreenText(text='Skirmish Online',
                                       font=self.font,
                                       pos=(0, 0.7),
                                       scale=0.2,
                                       parent=self.node)
        self.loading_label = OnscreenText(text='Loading world...',
                                          font=self.font,
                                          pos=(0, 0),
                                          scale=0.2,
                                          parent=self.node)

    def enter(self):
        self.node.show()
        self.background.show()

    def leave(self):
        self.node.hide()
        self.background.hide()
