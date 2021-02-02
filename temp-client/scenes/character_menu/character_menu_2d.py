from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectEntry, DirectButton, DGG


class CharacterMenu2D:

    def __init__(self, char_menu):
        self.char_menu = char_menu
        self.node = char_menu.node_2d
        self.warrior_btn = None
        self.mage_btn = None
        self.priest_btn = None
        self.archer_btn = None
        self.class_name_text = None
        self.player_name_entry = None
        self.join_world_btn = None
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
        self.warrior_btn = DirectButton(scale=0.34, pos=(-1.5, 0, 0.6), frameColor=(0, 0, 0, 0),
                                        image=self.char_menu.core.assets_dir+'artwork/warrior-class.png',
                                        image_scale=0.3,
                                        rolloverSound=self.char_menu.core.parent.rollover_sound,
                                        clickSound=self.char_menu.core.parent.click_sound,
                                        command=self.char_menu.set_selected_class(0))
        self.archer_btn = DirectButton(scale=0.34, pos=(-1.5, 0, -0.3), frameColor=(0, 0, 0, 0),
                                       image=self.char_menu.core.assets_dir+'artwork/archer-class.png',
                                       image_scale=0.3,
                                       rolloverSound=self.char_menu.core.parent.rollover_sound,
                                       clickSound=self.char_menu.core.parent.click_sound,
                                       command=self.char_menu.set_selected_class(1))
        self.mage_btn = DirectButton(scale=0.34, pos=(-1.5, 0, 0.3), frameColor=(0, 0, 0, 0),
                                     image=self.char_menu.core.assets_dir+'artwork/mage-class.png',
                                     image_scale=0.3,
                                     rolloverSound=self.char_menu.core.parent.rollover_sound,
                                     clickSound=self.char_menu.core.parent.click_sound,
                                     command=self.char_menu.set_selected_class(2))
        self.priest_btn = DirectButton(scale=0.34, pos=(-1.5, 0, 0), frameColor=(0, 0, 0, 0),
                                       image=self.char_menu.core.assets_dir+'artwork/priest-class.png',
                                       image_scale=0.3,
                                       rolloverSound=self.char_menu.core.parent.rollover_sound,
                                       clickSound=self.char_menu.core.parent.click_sound,
                                       command=self.char_menu.set_selected_class(3))

        self.class_name_text = OnscreenText(text='', font=self.char_menu.core.parent.font,
                                            pos=(1, 0.6), scale=0.1, mayChange=True)

        self.player_name_entry = DirectEntry(scale=0.1, pos=(-0.4, 0, -0.9), frameColor=(1, 1, 1, 0.1),
                                             entryFont=self.char_menu.core.parent.font,
                                             width=7, relief=DGG.RIDGE)
        self.join_world_btn = DirectButton(scale=0.34, pos=(1, 0, -0.85), frameColor=(0, 0, 0, 0),
                                           text_font=self.char_menu.core.parent.font,
                                           text_fg=(1, 1, 1, 0.8), text_pos=(0, -0.05), text_scale=0.18,
                                           text='Join world', image=self.char_menu.core.assets_dir+'artwork/button.png',
                                           image_scale=(1.1, 1, 0.3),
                                           rolloverSound=self.char_menu.core.parent.rollover_sound,
                                           clickSound=self.char_menu.core.parent.click_sound,
                                           command=self.char_menu.join_game)
        self.join_world_btn.set_transparency(1)
        self.character_description_text = OnscreenText(text='',
                                                       font=self.core.parent.font,
                                                       fg=(1, 1, 1, 0.8),
                                                       pos=(1, 0.15), scale=0.07, mayChange=True,
                                                       frame=(0, 0, 0, 0.8),
                                                       bg=(0, 0, 0, 0.8))

    def refresh(self):
        self.class_name_text.setText(self.class_info[self.char_menu.selected_class][0])
        self.class_name_text.setFg(self.class_info[self.char_menu.selected_class][1])
        self.character_description_text.setText(self.class_info[self.char_menu.selected_class][2])

