from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter
from time import sleep


class NetworkManager:
    def __init__(self, client):
        self.client = client

        self.manager = QueuedConnectionManager()
        self.reader = QueuedConnectionReader(self.manager, 0)
        self.writer = ConnectionWriter(self.manager, 0)

        self.server_port = 5000
        self.server_address = None
        self.timeout = 10000
        self.server_connection = None
        self.connected = False

    def connect(self, server_address):
        self.server_address = server_address
        self.client.main_menu.display_notification("Connecting...")
        self.server_connection = self.manager.open_TCP_client_connection(self.server_address,
                                                                         self.server_port, self.timeout)
        if self.server_connection:
            self.reader.add_connection(self.server_connection)
            self.connected = True
            self.client.main_menu.display_notification("Connected!\nLoading models...")
            self.client.main_menu.load_character_preparation()



