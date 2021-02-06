from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectEntry, DirectButton, DGG


class CharacterMenu2D:

    def __init__(self, char_menu):
        self.char_menu = char_menu
        self.core = char_menu.core
        self.node = char_menu.node_2d
        self.warrior_btn = None
        self.mage_btn = None
        self.priest_btn = None
        self.archer_btn = None
        self.class_name_text = None
        self.player_name_entry = None
        self.join_skirmish_btn = None
        self.character_description_text = None
        self.class_info = [
            ['Warrior', (1, 0, 0, 1), 'Abilities: '
                                      '\n ability 1 - lorem ipsum'
                                      '\n ability 2 - lorem ipsum'
                                      '\n ability 3 - lorem ipsum'],
            ['Archer', (0, 1, 0, 1), 'Abilities: '
                                     '\n ability 1 - lorem ipsum'
                                     '\n ability 2 - lorem ipsum'
                                     '\n ability 3 - lorem ipsum'],
            ['Mage', (0, 0, 1, 1), 'Abilities: '
                                   '\n ability 1 - lorem ipsum'
                                   '\n ability 2 - lorem ipsum'
                                   '\n ability 3 - lorem ipsum'],
            ['Priest', (1, 1, 1, 1), 'Abilities: '
                                     '\n ability 1 - lorem ipsum'
                                     '\n ability 2 - lorem ipsum'
                                     '\n ability 3 - lorem ipsum']
        ]

    def load(self):
        assets_dir = self.core.assets_dir
        rollover_sound = self.core.loader.loadSfx(assets_dir + 'sounds/mouse_rollover.wav')
        click_sound = self.core.loader.loadSfx(assets_dir + 'sounds/mouse_click.wav')
        font = self.core.loader.load_font(assets_dir + 'fonts/GODOFWAR.TTF')

        self.warrior_btn = DirectButton(scale=0.34,
                                        pos=(-1.5, 0, 0.6),
                                        frameColor=(0, 0, 0, 0),
                                        image=assets_dir+'artwork/warrior-class.png',
                                        image_scale=0.3,
                                        rolloverSound=rollover_sound,
                                        clickSound=click_sound,
                                        command=lambda: self.char_menu.update_class(0),
                                        parent=self.node)
        self.archer_btn = DirectButton(scale=0.34,
                                       pos=(-1.5, 0, -0.3),
                                       frameColor=(0, 0, 0, 0),
                                       image=assets_dir+'artwork/archer-class.png',
                                       image_scale=0.3,
                                       rolloverSound=rollover_sound,
                                       clickSound=click_sound,
                                       command=lambda: self.char_menu.update_class(1),
                                       parent=self.node)
        self.mage_btn = DirectButton(scale=0.34,
                                     pos=(-1.5, 0, 0.3),
                                     frameColor=(0, 0, 0, 0),
                                     image=assets_dir+'artwork/mage-class.png',
                                     image_scale=0.3,
                                     rolloverSound=rollover_sound,
                                     clickSound=click_sound,
                                     command=lambda: self.char_menu.update_class(2),
                                     parent=self.node)
        self.priest_btn = DirectButton(scale=0.34,
                                       pos=(-1.5, 0, 0),
                                       frameColor=(0, 0, 0, 0),
                                       image=assets_dir+'artwork/priest-class.png',
                                       image_scale=0.3,
                                       rolloverSound=rollover_sound,
                                       clickSound=click_sound,
                                       command=lambda: self.char_menu.update_class(3),
                                       parent=self.node)

        self.class_name_text = OnscreenText(text='',
                                            font=font,
                                            pos=(1, 0.6),
                                            scale=0.1,
                                            mayChange=True,
                                            parent=self.node)

        self.player_name_entry = DirectEntry(scale=0.1,
                                             pos=(-0.4, 0, -0.9),
                                             frameColor=(1, 1, 1, 0.1),
                                             entryFont=font,
                                             width=7,
                                             relief=DGG.RIDGE,
                                             parent=self.node)
        self.join_skirmish_btn = DirectButton(scale=0.34,
                                              pos=(1, 0, -0.85),
                                              frameColor=(0, 0, 0, 0),
                                              text_font=font,
                                              text_fg=(1, 1, 1, 0.8),
                                              text_pos=(0, -0.05),
                                              text_scale=0.18,
                                              text='Join skirmish',
                                              image=assets_dir+'artwork/button.png',
                                              image_scale=(1.1, 1, 0.3),
                                              rolloverSound=rollover_sound,
                                              clickSound=click_sound,
                                              command=self.char_menu.join_skirmish_attempt,
                                              parent=self.node)
        self.join_skirmish_btn.set_transparency(1)
        self.character_description_text = OnscreenText(text='',
                                                       font=font,
                                                       fg=(1, 1, 1, 0.8),
                                                       pos=(1, 0.15),
                                                       scale=0.07,
                                                       mayChange=True,
                                                       frame=(0, 0, 0, 0.8),
                                                       bg=(0, 0, 0, 0.8),
                                                       parent=self.node)

    def refresh(self):
        self.class_name_text.setText(self.class_info[self.char_menu.selected_class][0])
        self.class_name_text.setFg(self.class_info[self.char_menu.selected_class][1])
        self.character_description_text.setText(self.class_info[self.char_menu.selected_class][2])

