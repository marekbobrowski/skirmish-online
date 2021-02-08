from scenes.character_menu.character_menu_2d import CharacterMenu2D
from scenes.character_menu.character_menu_3d import CharacterMenu3D
from threading import Thread


class CharacterMenu:

    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.core = scene_manager.core
        self.selected_class = 0
        self.joining_skirmish = False

        self.node_2d = self.core.aspect2d.attach_new_node('Character Menu Node')
        self.node_3d = self.core.render.attach_new_node('Character Menu Node')

        self.char_menu_2d = CharacterMenu2D(self)
        self.char_menu_3d = CharacterMenu3D(self)

        self._is_loaded = False

    def enter(self):
        self.node_2d.show()
        self.node_3d.show()
        self.char_menu_2d.refresh()
        self.char_menu_3d.refresh()

    def is_loaded(self):
        return self._is_loaded

    def load(self):
        self.node_2d.hide()
        self.node_3d.hide()
        self.char_menu_2d.load()
        self.char_menu_3d.load()
        self._is_loaded = True

    def join_skirmish_attempt(self):
        if not self.joining_skirmish:
            self.joining_skirmish = True
            # running this function in new thread so that
            # client-server communication and model loading don't block the main thread
            Thread(target=self.join_skirmish).start()

    def join_skirmish(self):
        self.scene_manager.show_dialog('Asking for pass...')
        player_name = self.char_menu_2d.player_name_entry.get()
        passed = self.core.network_manager.ask_for_pass(player_name, self.selected_class)
        if passed:
            self.scene_manager.hide_dialog()
            self.scene_manager.change_scene_to(2)
            self.scene_manager.load_scene(3)
            self.scene_manager.change_scene_to(3)

        else:
            self.scene_manager.show_dialog('This nickname is already in use.\nPlease change it.')
        self.joining_skirmish = False

    def update_class(self, class_number):
        self.selected_class = class_number
        self.char_menu_2d.refresh()
        self.char_menu_3d.refresh()

    def leave(self):
        self.node_2d.hide()
        self.node_3d.hide()
