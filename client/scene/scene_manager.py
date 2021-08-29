from scene.character_menu.character_menu import CharacterMenu
from scene.menu.menu import Menu
from scene.skirmish.skirmish import Skirmish
from scene.common_modules.dialog import Dialog
from scene.loading_screen.loading_screen import LoadingScreen
import core
from scene.scene import Scene


class SceneManager:

    def __init__(self):
        self.dialog = None
        self.scene_mapping = {
            Scene.MENU: Menu(),
            Scene.CHARACTER_MENU: CharacterMenu(),
            Scene.LOADING_SCREEN: LoadingScreen(),
            Scene.SKIRMISH: Skirmish()
        }
        self.current_scene = None
        self.joining_skirmish = False

    def load_scene(self, scene):
        scene_to_load = self.scene_mapping.get(scene)
        if not scene_to_load.is_loaded:
            scene_to_load.load()

    def change_scene_to(self, scene):
        if self.current_scene is not None:
            self.current_scene.leave()
        self.current_scene = self.scene_mapping.get(scene)
        if not self.current_scene.is_loaded:
            self.current_scene.load()
        self.current_scene.enter()

    def show_dialog(self, text, button_text=None, button_command=None):
        if self.dialog is None:
            self.dialog = Dialog(core=core.instance,
                                 parent=core.instance.aspect2d,
                                 frame_size=(-0.75, 0.75, -0.25, 0.25))
        if button_text is not None:
            self.dialog.label.setText(button_text)
        if button_command is not None:
            self.dialog.button.commandFunc(button_command)
        self.dialog.set_label(text)
        self.dialog.set_button(button_text, button_command)
        self.dialog.show()

    def hide_dialog(self):
        self.dialog.hide()


instance = SceneManager()
