from scenes.character_menu.character_menu import CharacterMenu
from scenes.menu.menu import Menu
from scenes.skirmish.skirmish import Skirmish
from direct.gui.DirectGui import DirectDialog


class SceneManager:
    def __init__(self, core):
        self.core = core
        self.dialog = None
        self.scene_mapping = {
            0: Menu(self),
            1: CharacterMenu(self),
            2: Skirmish(self)
        }
        self.current_scene = None

    def change_scene_to(self, scene):
        if self.current_scene is not None:
            self.current_scene.leave()
        self.current_scene = self.scene_mapping.get(scene)
        if not self.current_scene.is_loaded():
            self.current_scene.load()
        self.current_scene.enter()

    def show_dialog(self, text):
        if self.dialog is None:
            self.dialog = DirectDialog(parent=self.core.aspect2d,
                                       frameSize=(-0.5, 0.25, -0.5, 0.25))
            #print(self.dialog.)
        else:
            self.dialog.setText(text)



