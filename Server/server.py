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
from time import sleep

# === PACKET TYPES ==== #

# INITIAL TYPES #
ASK_FOR_PASS = 1
ASK_FOR_INITIAL_DATA = 2

# SENT BY CLIENT AND SERVER #
TYPE_POS_HPR = 3
TYPE_IS_MOVING = 4
TYPE_SKILL = 5
TYPE_DISCONNECTION = 6

# SENT ONLY BY SERVER
TYPE_CHARACTER_REACTION = 7  # reaction to hit, or spell-casting animation'
TYPE_TELEPORT = 8
TYPE_NEW_PLAYER = 9

# ===================== #


class Server:
    def __init__(self):
        self.manager = QueuedConnectionManager()
        self.listener = QueuedConnectionListener(self.manager, 0)
        self.reader = QueuedConnectionReader(self.manager, 0)
        self.writer = ConnectionWriter(self.manager, 0)
        self.active_connections = []
        self.last_id = 0
        self.port = 5000
        self.backlog = 1000
        self.tcp_socket = self.manager.open_TCP_server_rendezvous(self.port, self.backlog)
        self.listener.add_connection(self.tcp_socket)

    def run(self):
        start_new_thread(self.listen_for_new_connections, ())
        start_new_thread(self.listen_for_new_data, ())
        start_new_thread(self.send_updates_to_active_players, ())

    def listen_for_new_connections(self):
        while True:
            if self.listener.new_connection_available():
                rendezvous = PointerToConnection()
                net_address = NetAddress()
                new_connection = PointerToConnection()

                if self.listener.get_new_connection(rendezvous, net_address, new_connection):
                    new_connection = new_connection.p()
                    self.active_connections.append(Player(new_connection))
                    print(str(new_connection.get_address()) + ' connected')
                    self.reader.add_connection(new_connection)

    def listen_for_new_data(self):
        while True:
            if self.reader.data_available():
                datagram = NetDatagram()
                if self.reader.get_data(datagram):
                    self.process_data(datagram)

    def send_updates_to_active_players(self):
        while True:
            for player in self.active_connections:
                if player.get_joined_game():
                    self.send_pos_hpr(player.get_connection())
            sleep(0.05)

    def process_data(self, datagram):
        iterator = PyDatagramIterator(datagram)
        packet_type = iterator.get_uint8()
        if packet_type == ASK_FOR_PASS:
            self.handle_ask_for_pass(datagram, iterator)
        elif packet_type == ASK_FOR_INITIAL_DATA:
            self.handle_ask_for_initial_data(datagram, iterator)
        elif packet_type == TYPE_POS_HPR:
            self.handle_pos_hpr(datagram, iterator)
        elif packet_type == TYPE_DISCONNECTION:
            self.handle_disconnection(datagram, iterator)

    def handle_ask_for_pass(self, datagram, iterator):
        name = iterator.get_string()
        class_number = iterator.get_uint8()
        connection = datagram.get_connection()
        allow_player = 1
        # the client had to connect to the server, before he asked for pass
        # so now the server searches for the player object in his connection list
        player = self.find_player_by_connection(connection)
        if player is not None:
            player.set_name(name)
            player.set_class_number(class_number)
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
        for player in self.active_connections:
            if connection == player.connection:
                return player
        return None

    def handle_ask_for_initial_data(self, datagram, iterator):
        connection = datagram.get_connection()
        player = self.find_player_by_connection(connection)
        if player is None:
            return
        else:
            x, y, z, h, p, r = -3, -5, 1, 120, 0, 0
            player.set_pos_hpr(x, y, z, h, p, r)

            response = PyDatagram()
            response.add_uint8(ASK_FOR_INITIAL_DATA)

            # send player his own id, nickname and class
            response.add_uint8(player.get_id())
            response.add_string(player.get_name())
            response.add_uint8(player.get_class_number())

            # send player his own position and rotation
            response.add_float64(player.get_x())
            response.add_float64(player.get_y())
            response.add_float64(player.get_z())
            response.add_float64(player.get_h())
            response.add_float64(player.get_p())
            response.add_float64(player.get_r())

            # send number of other players that are already participating in game
            active_players = self.get_number_of_players_in_world()
            response.add_uint8(active_players)

            # send players' id's, names and positions & rotations
            for i, other_player in enumerate(self.active_connections):
                if other_player is not player and other_player.get_joined_game() and i < active_players:
                    # order: id, name, class, x, y, z, h, p, r
                    response.add_uint8(other_player.get_id())
                    response.add_string(other_player.get_name())
                    response.add_uint8(other_player.get_class_number())
                    response.add_float64(other_player.get_x())
                    response.add_float64(other_player.get_y())
                    response.add_float64(other_player.get_z())
                    response.add_float64(other_player.get_h())
                    response.add_float64(other_player.get_p())
                    response.add_float64(other_player.get_r())
            self.writer.send(response, connection)

            # send info about new player to everyone else
            datagram = PyDatagram()
            datagram.add_uint8(TYPE_NEW_PLAYER)
            datagram.add_uint8(player.get_id())
            datagram.add_string(player.get_name())
            datagram.add_uint8(player.get_class_number())
            datagram.add_float64(player.get_x())
            datagram.add_float64(player.get_y())
            datagram.add_float64(player.get_z())
            datagram.add_float64(player.get_h())
            datagram.add_float64(player.get_p())
            datagram.add_float64(player.get_r())

            for player in self.active_connections:
                if player.get_joined_game():
                    self.writer.send(datagram, player.get_connection())

            player.set_joined_game(True)

    def handle_pos_hpr(self, datagram, iterator):
        player = self.find_player_by_connection(datagram.get_connection())
        if player is not None:
            x = iterator.get_float64()
            y = iterator.get_float64()
            z = iterator.get_float64()
            h = iterator.get_float64()
            p = iterator.get_float64()
            r = iterator.get_float64()
            player.set_pos_hpr(x, y, z, h, p, r)

    def get_number_of_players_in_world(self):
        count = 0
        for other_player in self.active_connections:
            if other_player.get_joined_game():
                count += 1
        return count

    def send_pos_hpr(self, connection):
        datagram = PyDatagram()
        active_players = self.get_number_of_players_in_world()
        datagram.add_uint8(TYPE_POS_HPR)
        datagram.add_uint8(active_players)
        for i, player in enumerate(self.active_connections):
            if player.get_joined_game() and i < active_players:
                datagram.add_uint8(player.get_id())
                datagram.add_float64(player.get_x())
                datagram.add_float64(player.get_y())
                datagram.add_float64(player.get_z())
                datagram.add_float64(player.get_h())
                datagram.add_float64(player.get_p())
                datagram.add_float64(player.get_r())
        self.writer.send(datagram, connection)

    def handle_disconnection(self, datagram, iterator):
        connection = datagram.get_connection()
        player = self.find_player_by_connection(connection)
        if player is not None:
            self.active_connections.remove(player)
            print(str(connection.get_address()) + ' disconnected.')
            self.manager.close_connection(connection)
            id = player.get_id()
            del player
            for other_player in self.active_connections:
                if other_player.get_joined_game():
                    datagram = PyDatagram()
                    datagram.add_uint8(TYPE_DISCONNECTION)
                    datagram.add_uint8(id)
                    self.writer.send(datagram, other_player.get_connection())


if __name__ == "__main__":
    server = Server()
    server.run()
    quit_server = input('Press any key to turn off the server...\n')


