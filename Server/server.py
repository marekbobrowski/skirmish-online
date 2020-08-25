from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionListener
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter
from _thread import start_new_thread
from panda3d.core import PointerToConnection
from panda3d.core import NetAddress
from panda3d.core import NetDatagram
from player import Player
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
import random

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


class Server:
    def __init__(self):
        self.manager = QueuedConnectionManager()
        self.listener = QueuedConnectionListener(self.manager, 0)
        self.reader = QueuedConnectionReader(self.manager, 0)
        self.writer = ConnectionWriter(self.manager, 0)
        self.connected_players = []
        self.last_id = 0
        self.port = 5000
        self.backlog = 1000
        self.tcp_socket = self.manager.open_TCP_server_rendezvous(self.port, self.backlog)
        self.listener.add_connection(self.tcp_socket)

    def run(self):
        start_new_thread(self.listen_for_new_connections, ())
        start_new_thread(self.listen_for_new_data, ())

    def listen_for_new_connections(self):
        while True:
            if self.listener.new_connection_available():
                rendezvous = PointerToConnection()
                net_address = NetAddress()
                new_connection = PointerToConnection()

                if self.listener.get_new_connection(rendezvous, net_address, new_connection):
                    new_connection = new_connection.p()
                    self.connected_players.append(Player(new_connection))
                    print(str(new_connection.get_address()) + ' connected')
                    self.reader.add_connection(new_connection)

    def listen_for_new_data(self):
        while True:
            if self.reader.data_available():
                datagram = NetDatagram()
                if self.reader.get_data(datagram):
                    self.process_data(datagram)

    def process_data(self, datagram):
        iterator = PyDatagramIterator(datagram)
        packet_type = iterator.get_uint8()
        if packet_type == ASK_FOR_PASS:
            self.handle_ask_for_pass(datagram, iterator)
        if packet_type == ASK_FOR_INITIAL_DATA:
            self.handle_ask_for_initial_data(datagram, iterator)

    def handle_ask_for_pass(self, datagram, iterator):
        name = iterator.get_string()
        class_number = iterator.get_uint8()
        connection = datagram.get_connection()
        allow_player = 0
        player = self.find_player_by_connection(connection)
        if player is not None:
            player.joined_game = True
            player.set_name(name)
            player.set_player_class(class_number)
            player.set_id(self.last_id)
            self.last_id += 1
            allow_player = 1
        else:
            allow_player = 0
        response = PyDatagram()
        response.add_uint8(ASK_FOR_PASS)
        response.add_uint8(allow_player)  # 0 - don't allow player to join, 1 - allow player to join
        self.writer.send(response, connection)

    def find_player_by_connection(self, connection):
        for player in self.connected_players:
            if connection == player.connection:
                return player
        return None

    def handle_ask_for_initial_data(self, datagram, iterator):
        connection = datagram.get_connection()
        player = self.find_player_by_connection(connection)

        if player is not None and player.get_joined_game():
            x, y, z, h, p, r = -3, -5, 1, 120, 0, 0
            player.set_pos_hpr(x, y, z, h, p, r)

            response = PyDatagram()
            response.add_uint8(ASK_FOR_INITIAL_DATA)

            # send player his own id, nickname and class
            response.add_uint8(player.get_id())
            response.add_string(player.get_name())
            response.add_uint8(player.get_player_class())

            # send player his own position and rotation
            response.add_float64(player.get_x())
            response.add_float64(player.get_y())
            response.add_float64(player.get_z())
            response.add_float64(player.get_h())
            response.add_float64(player.get_p())
            response.add_float64(player.get_r())

            # send players' id's, names and positions & rotations
            for other_player in self.connected_players:
                if other_player is not player and other_player.get_joined_game():
                    # order: id, name, class, x, y, z, h, p, r
                    response.add_uint8(other_player.get_id())
                    response.add_string(other_player.get_name())
                    response.add_uint8(other_player.get_player_class())
                    response.add_float64(other_player.get_x())
                    response.add_float64(other_player.get_y())
                    response.add_float64(other_player.get_z())
                    response.add_float64(other_player.get_h())
                    response.add_float64(other_player.get_p())
                    response.add_float64(other_player.get_r())
        self.writer.send(response, connection)


if __name__ == "__main__":
    server = Server()
    server.run()
    quit_server = input('Press any key to turn off the server...\n')


