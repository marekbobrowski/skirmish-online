from scenes.character_menu.character_menu_2d import CharacterMenu2D
from scenes.character_menu.character_menu_3d import CharacterMenu3D


class CharacterMenu:

    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.core = scene_manager.core
        self.selected_class = 0

        self.node_2d = self.core.render2d.attach_new_node('Character Menu Node')
        self.node_3d = self.core.render.attach_new_node('Character Menu Node')

        self.char_menu_2d = CharacterMenu2D(self)
        self.char_menu_3d = CharacterMenu3D(self)

        self._is_loaded = False

    def enter(self):
        self.char_menu_2d.refresh()
        self.char_menu_3d.refresh()

    def is_loaded(self):
        return self.is_loaded

    def load(self):
        self.char_menu_2d.load()
        self.char_menu_3d.load()

    def join_game(self):
        self.hide()
        self.core.parent.display_notification('Logging in...')
        if self.core.network_manager.ask_for_pass(self.player_name_entry.get(), self.selected_class):
            self.core.parent.display_notification('Successfully logged in!\nLoading world...')
            if self.core.network_manager.ask_for_initial_data():
                self.core.network_manager.send_ready_for_updates()
                self.core.network_manager.start_listening_for_updates()
                self.core.network_manager.start_sending_updates()
                self.core.parent.hide()
                self.core.world.show()
                self.core.world.enable_character_control()
            else:
                self.core.parent.display_notification('Failed to load world.')
                self.core.parent.return_btn.show()
        else:
            self.core.parent.display_notification('Failed to log in.')
            self.core.parent.return_btn.show()

    def set_selected_class(self, class_number):
        self.selected_class = class_number
