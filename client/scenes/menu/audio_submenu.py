from direct.gui.DirectGui import DirectButton, DirectScrollBar, DGG


class AudioSubmenu:
    def __init__(self, menu):
        self.menu = menu
        self.audio_submenu_node = menu.menu_node.attach_new_node("Audio Submenu Node")
        self.audio_submenu_node.hide()
        self.master_audio_scroll = None
        self.sfx_audio_scroll = None
        self.music_audio_scroll = None
        self.ambiance_audio_scroll = None
        self.return_btn = None

    def load(self):
        assets_dir = self.menu.core.assets_dir
        self.master_audio_scroll = DirectScrollBar(range=(0, 100),
                                                   value=50,
                                                   pageSize=3,
                                                   orientation=DGG.HORIZONTAL,
                                                   parent=self.audio_submenu_node)
        self.master_audio_scroll.set_pos(0, 0, 0.2)

        self.sfx_audio_scroll = DirectScrollBar(range=(0, 100),
                                                value=50,
                                                pageSize=3,
                                                orientation=DGG.HORIZONTAL,
                                                parent=self.audio_submenu_node)
        self.sfx_audio_scroll.set_pos(0, 0, 0)

        self.music_audio_scroll = DirectScrollBar(range=(0, 100),
                                                  value=50,
                                                  pageSize=3,
                                                  orientation=DGG.HORIZONTAL,
                                                  parent=self.audio_submenu_node)
        self.music_audio_scroll.set_pos(0, 0, -0.2)

        self.ambiance_audio_scroll = DirectScrollBar(range=(0, 100),
                                                     value=50,
                                                     pageSize=3,
                                                     orientation=DGG.HORIZONTAL,
                                                     parent=self.audio_submenu_node)
        self.ambiance_audio_scroll.set_pos(0, 0, -0.4)

        self.return_btn = DirectButton(scale=0.34,
                                       pos=(0, 0, -0.7),
                                       frameColor=(0, 0, 0, 0),
                                       text_font=self.menu.font,
                                       text_fg=(1, 1, 1, 0.8),
                                       text_pos=(0, -0.05),
                                       text_scale=0.18,
                                       text='Return',
                                       image=assets_dir + 'artwork/button.png',
                                       image_scale=(1.1, 1, 0.3),
                                       rolloverSound=self.menu.rollover_sound,
                                       clickSound=self.menu.click_sound,
                                       parent=self.audio_submenu_node,
                                       command=lambda: self.menu.change_subscene_to(0))
        self.return_btn.set_transparency(1)

    def enter(self):
        self.audio_submenu_node.show()
        print('DEBUG: entered audio submenu')

    def leave(self):
        self.audio_submenu_node.hide()
        print('DEBUG: left audio submenu')
