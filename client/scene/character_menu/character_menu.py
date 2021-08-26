from scene.character_menu.character_menu_2d import CharacterMenu2D
from scene.character_menu.character_menu_3d import CharacterMenu3D
from threading import Thread
import core


class CharacterMenu:
    """
    This class represents a scene in which user chooses their class and nickname.
    After choice, they can enter the game by clicking "Join skirmish" button.
    """
    def __init__(self, scene_manager):
        self.selected_class = 0
        self.joining_skirmish = False

        # The scene graph nodes. Every visible submodule is attached either to
        # the 3d node (3d models like players, terrain) or the 2d node
        # (usually 2d interface components -- buttons, input fields etc.).
        self.node_2d = core.instance.aspect2d.attach_new_node('Character Menu Node')
        self.node_3d = core.instance.render.attach_new_node('Character Menu Node')

        self.char_menu_2d = CharacterMenu2D(self)
        self.char_menu_3d = CharacterMenu3D(self)

        self.is_loaded = False

    def enter(self):
        """
        Enters to this scene -- displays it's components attached to the 2d and 3d nodes.
        """
        self.node_2d.show()
        self.node_3d.show()
        self.char_menu_2d.refresh()
        self.char_menu_3d.refresh()

    def load(self):
        """
        Loads the scene's components.
        """
        self.node_2d.hide()
        self.node_3d.hide()
        self.char_menu_2d.load()
        self.char_menu_3d.load()
        self.is_loaded = True

    def update_class(self, class_number):
        """
        Updates the scene according to the chosen class.
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
