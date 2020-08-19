from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from menu import Menu


class Client(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        props = WindowProperties()
        props.set_title('Skirmish Online')
        props.set_icon_filename('artwork/icon.ico')
        base.win.request_properties(props)
        self.menu = Menu(self)
        self.menu.display_main()


if __name__ == "__main__":
    client = Client()
    client.run()
