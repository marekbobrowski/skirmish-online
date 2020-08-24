from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter
from time import sleep
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from panda3d.core import NetDatagram
from other_player import OtherPlayer
from player import Player

# === PACKET TYPES ==== #

# INITIAL TYPES #
ASK_FOR_PASS = 1
ASK_FOR_INITIAL_DATA = 2

# SENT BY CLIENT AND SERVER #
TYPE_POS_HPR = 3
TYPE_IS_MOVING = 4
TYPE_SKILL = 5

# SENT ONLY BY SERVER
TYPE_CHARACTER_REACTION = 6  # reaction to hit, or spell-casting animation'
TYPE_TELEPORT = 7

# ===================== #


class NetworkManager:
    def __init__(self, client):
        self.client = client

        self.manager = QueuedConnectionManager()
        self.reader = QueuedConnectionReader(self.manager, 0)
        self.writer = ConnectionWriter(self.manager, 0)

        self.server_port = 5000
        self.server_address = None
        self.timeout = 4000
        self.server_connection = None
        self.connected = False

    def connect(self, server_address):
        self.server_address = server_address
        self.server_connection = self.manager.open_TCP_client_connection(self.server_address,
                                                                         self.server_port, self.timeout)
        if self.server_connection:
            self.reader.add_connection(self.server_connection)
            self.connected = True
            return True
        return False

    def ask_for_pass(self, name, class_number):
        # send datagram asking if player can join the world
        data = PyDatagram()
        data.add_uint8(ASK_FOR_PASS)
        data.add_string(name)  # player's name
        data.add_uint8(class_number)  # class number
        self.writer.send(data, self.server_connection)

        # wait for response from the server
        self.manager.wait_for_readers(self.timeout/1000)
        if self.reader.data_available():
            datagram = NetDatagram()
            if self.reader.get_data(datagram):
                iterator = PyDatagramIterator(datagram)
                packet_type = iterator.get_uint8()
                if packet_type == ASK_FOR_PASS:
                    allow_join = iterator.get_uint8()
                    if allow_join == 1:
                        return True
        return False

    def ask_for_initial_data(self):
        # send datagram asking for initial world data (player's location, other player names, positions)
        data = PyDatagram()
        data.add_uint8(ASK_FOR_INITIAL_DATA)
        self.writer.send(data, self.server_connection)
        # wait for response from the server
        self.manager.wait_for_readers(self.timeout/1000)
        if self.reader.data_available():
            datagram = NetDatagram()
            if self.reader.get_data(datagram):
                iterator = PyDatagramIterator(datagram)
                packet_type = iterator.get_uint8()
                if packet_type == ASK_FOR_INITIAL_DATA:
                    id = iterator.get_uint8()
                    name = iterator.get_string()
                    class_number = iterator.get_uint8()
                    self.client.world.main_player = Player(self.client, class_number)
                    self.client.world.main_player.reparent_to(self.client.render)
                    self.client.world.main_player.hide()
                    return True

        return False





