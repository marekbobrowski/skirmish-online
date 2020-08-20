from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from main_menu import MainMenu
from network_manager import NetworkManager
from map import Map


class Client(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        props = WindowProperties()
        props.set_title('Skirmish Online')
        props.set_icon_filename('artwork/icon.ico')
        base.win.request_properties(props)
        self.network_manager = NetworkManager(self)
        self.main_menu = MainMenu(self)
        self.map = Map(self)
        self.main_menu.display_main()


if __name__ == "__main__":
    client = Client()
    client.run()
