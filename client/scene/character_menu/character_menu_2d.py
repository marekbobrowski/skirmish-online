from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectEntry, DirectButton, DGG
import assets_dir_config
import core
from assets import asset_names
from scene.character_menu import join_game


class CharacterMenu2D:
    """
    The interface submodule of the character menu. Displays buttons that represent available classes,
    input field for character name, class description field etc.
    """
    def __init__(self, char_menu):
        self.char_menu = char_menu
        self.node = char_menu.node_2d
        self.warrior_btn = None
        self.mage_btn = None
        self.priest_btn = None
        self.archer_btn = None
        self.class_name_text = None
        self.player_name_entry = None
        self.join_skirmish_btn = None
        self.character_description_text = None

        # class_name, class_color, class_description
        self.class_info = [
            ['Hero 1', (1, 0, 0, 1), 'Abilities: '
                                     '\n ability 1 - lorem ipsum'
                                     '\n ability 2 - lorem ipsum'
                                     '\n ability 3 - lorem ipsum'],
            ['Hero 2', (0, 1, 0, 1), 'Abilities: '
                                     '\n ability 1 - lorem ipsum'
                                     '\n ability 2 - lorem ipsum'
                                     '\n ability 3 - lorem ipsum']
        ]

    def load(self):
        """
        Loads the character's menu interface components.
        """
        rollover_sound = core.instance.loader.loadSfx(asset_names.rollover_sound)
        click_sound = core.instance.loader.loadSfx(asset_names.click_sound)
        font = core.instance.loader.load_font(asset_names.font_1)

        self.warrior_btn = DirectButton(scale=0.34,
                                        pos=(-1.5, 0, 0.6),
                                        frameColor=(0, 0, 0, 0),
                                        image=asset_names.warrior_icon,
                                        image_scale=0.3,
                                        rolloverSound=rollover_sound,
                                        clickSound=click_sound,
                                        command=lambda: self.char_menu.update_class(0),
                                        parent=self.node)
        self.archer_btn = DirectButton(scale=0.34,
                                       pos=(-1.5, 0, -0.3),
                                       frameColor=(0, 0, 0, 0),
                                       image=asset_names.archer_icon,
                                       image_scale=0.3,
                                       rolloverSound=rollover_sound,
                                       clickSound=click_sound,
                                       command=lambda: self.char_menu.update_class(1),
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
                                              image=asset_names.button,
                                              image_scale=(1.1, 1, 0.3),
                                              rolloverSound=rollover_sound,
                                              clickSound=click_sound,
                                              command=lambda: join_game.join_skirmish_attempt(
                                                  self.player_name_entry.get(),
                                                  self.char_menu.selected_class),
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
        """
        Refreshes the character menu by updating the classes name and it's description.
        """
        self.class_name_text.setText(self.class_info[self.char_menu.selected_class][0])
        self.class_name_text.setFg(self.class_info[self.char_menu.selected_class][1])
        self.character_description_text.setText(self.class_info[self.char_menu.selected_class][2])

