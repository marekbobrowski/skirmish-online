from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from network_manager import NetworkManager
from scene_manager import SceneManager


class Core(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.assets_dir = '../assets/'

        # set up the window icon and cursor appearance
        props = WindowProperties()
        props.set_title('Skirmish Online')
        props.set_icon_filename(self.assets_dir + 'artwork/icon.ico')
        props.set_cursor_filename(self.assets_dir + 'artwork/cursor.ico')
        self.win.request_properties(props)

        self.disable_mouse()  # disable the default Panda3D mouse controlling system

        self.scene_manager = SceneManager(self)
        self.network_manager = NetworkManager(self)
        self.scene_manager.change_scene_to(0)
