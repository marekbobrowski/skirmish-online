from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter
from time import sleep
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from panda3d.core import NetDatagram
from character import Character
from _thread import start_new_thread
from direct.task.Task import Task

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

        # wait for datagram from the server
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
        # wait for datagram from the server
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
                    x = iterator.get_float64()
                    y = iterator.get_float64()
                    z = iterator.get_float64()
                    h = iterator.get_float64()
                    p = iterator.get_float64()
                    r = iterator.get_float64()
                    self.client.world.create_main_player(class_number, id, name, x, y, z, h, p, r)

                    number_of_active_players = iterator.get_uint8()
                    i = 0
                    while i < number_of_active_players:
                        id = iterator.get_uint8()
                        name = iterator.get_string()
                        class_number = iterator.get_uint8()
                        x = iterator.get_float64()
                        y = iterator.get_float64()
                        z = iterator.get_float64()
                        h = iterator.get_float64()
                        p = iterator.get_float64()
                        r = iterator.get_float64()
                        self.client.world.create_a_player(class_number, id, name, x, y, z, h, p, r)
                        i += 1

                    return True
        return False

    def start_listening_for_updates(self):
        self.client.taskMgr.add(self.listen_for_updates, "ListenForUpdates")

    def start_sending_updates(self):
        self.client.taskMgr.add(self.send_updates, "SendUpdates")

    def listen_for_updates(self, task):
        if self.reader.data_available():
            datagram = NetDatagram()
            iterator = PyDatagramIterator(datagram)
            if self.reader.get_data(datagram):
                self.process_updates(datagram, iterator)
        return Task.cont

    def send_updates(self, task):
        self.send_pos_hpr()
        return Task.cont

    def process_updates(self, datagram, iterator):
        packet_type = iterator.get_uint8()
        if packet_type == TYPE_POS_HPR:
            self.process_pos_hpr_from_server(datagram, iterator)

    def send_pos_hpr(self):
        datagram = PyDatagram()
        datagram.add_float64(self.client.world.main_player.get_x())
        datagram.add_float64(self.client.world.main_player.get_y())
        datagram.add_float64(self.client.world.main_player.get_z())
        datagram.add_float64(self.client.world.main_player.get_h())
        datagram.add_float64(self.client.world.main_player.get_p())
        datagram.add_float64(self.client.world.main_player.get_r())
        self.writer.send(datagram, self.server_connection)

    def process_pos_hpr_from_server(self, datagram, iterator):
        number_of_active_players = iterator.get_uint8()
        i = 0
        while i < number_of_active_players:
            id = iterator.get_uint8()
            x = iterator.get_float64()
            y = iterator.get_float64()
            z = iterator.get_float64()
            h = iterator.get_float64()
            p = iterator.get_float64()
            r = iterator.get_float64()
            self.client.world.update_player_pos_hpr(id, x, y, z, h, p, r)
            i += 1





