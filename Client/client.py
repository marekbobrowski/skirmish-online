from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from menu import Menu
from network_manager import NetworkManager
from map import Map
from world import World


class Client(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        props = WindowProperties()
        props.set_title('Skirmish Online')
        props.set_icon_filename('artwork/icon.ico')
        props.set_cursor_filename('artwork/cursor.ico')
        base.win.request_properties(props)
        self.network_manager = NetworkManager(self)
        self.menu = Menu(self)
        self.menu.display_main()
        self.world = World(self)


if __name__ == "__main__":
    client = Client()
    client.run()
