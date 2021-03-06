from scene.character_menu.character_menu_2d import CharacterMenu2D
from scene.character_menu.character_menu_3d import CharacterMenu3D
from threading import Thread


class CharacterMenu:
    """
    This class represents a scene in which user chooses their class and nickname.
    After choice, they can enter the game by clicking "Join skirmish" button.
    """
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.core = scene_manager.core
        self.selected_class = 0
        self.joining_skirmish = False

        # The scene graph nodes. Every visible submodule is attached either to
        # the 3d node (3d models like players, terrain) or the 2d node
        # (usually 2d interface components -- buttons, input fields etc.).
        self.node_2d = self.core.aspect2d.attach_new_node('Character Menu Node')
        self.node_3d = self.core.render.attach_new_node('Character Menu Node')

        self.char_menu_2d = CharacterMenu2D(self)
        self.char_menu_3d = CharacterMenu3D(self)

        self._is_loaded = False

    def enter(self):
        """
        Enters to this scene -- displays it's components attached to the 2d and 3d nodes.
        """
        self.node_2d.show()
        self.node_3d.show()
        self.char_menu_2d.refresh()
        self.char_menu_3d.refresh()

    def is_loaded(self):
        """
        Tells if the scene has already loaded it's components.
        """
        return self._is_loaded

    def load(self):
        """
        Loads the scene's components.
        """
        self.node_2d.hide()
        self.node_3d.hide()
        self.char_menu_2d.load()
        self.char_menu_3d.load()
        self._is_loaded = True

    def join_skirmish_attempt(self):
        """
        Attempts to join the skirmish.
        """
        if not self.joining_skirmish:
            self.joining_skirmish = True
            # running this function in new thread so that
            # client-server communication and model loading don't block the main thread
            Thread(target=self.join_skirmish).start()

    def join_skirmish(self):
        """
        Joins the skirmish by asking the server for a pass (the server check's if the nickname is not taken)
        and if everything's fine, loads and enters the skirmish scene.
        """
        self.scene_manager.show_dialog('Asking for a pass...')
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
        """
        Updates the view according to the chosen class.
        """
        self.selected_class = class_number
        self.char_menu_2d.refresh()
        self.char_menu_3d.refresh()

    def leave(self):
        """
        Leave the scene by hiding the components attached to the 2d and 3d nodes.
        """
        self.node_2d.hide()
        self.node_3d.hide()
