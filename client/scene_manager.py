from scenes.character_menu.character_menu import CharacterMenu
from scenes.menu.menu import Menu
from scenes.skirmish.skirmish import Skirmish
from scenes.common_modules.dialog import Dialog



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

    def load_scene(self, scene):
        scene_to_load = self.scene_mapping.get(scene)
        if not scene_to_load.is_loaded():
            scene_to_load.load()
        self.core.messenger.send('load success')

    def change_scene_to(self, scene):
        if self.current_scene is not None:
            self.current_scene.leave()
        self.current_scene = self.scene_mapping.get(scene)
        if not self.current_scene.is_loaded():
            self.current_scene.load()
        self.current_scene.enter()

    def show_dialog(self, text):
        if self.dialog is None:
            self.dialog = Dialog(parent=self.core.aspect2d,
                                 frame_size=(-0.75, 0.75, -0.25, 0.25),
                                 label=text,
                                 button_label='OK',
                                 function=None)
        self.dialog.set_label(text)

    def hide_dialog(self):
        self.dialog.hide()



