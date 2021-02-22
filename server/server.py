from time import sleep
from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionListener
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter
from threading import Thread
from panda3d.core import PointerToConnection
from panda3d.core import NetAddress
from panda3d.core import NetDatagram
from player.player import Player
from direct.distributed.PyDatagram import PyDatagram
from handler import Handler
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
from protocol.message import Message


# noinspection PyArgumentList
class Server:
    def __init__(self):
        # Support objects
        self.manager = QueuedConnectionManager()
        self.listener = QueuedConnectionListener(self.manager, 0)
        self.reader = QueuedConnectionReader(self.manager, 0)
        self.writer = ConnectionWriter(self.manager, 0)
        self.handler = Handler(self)

        # Server state
        self.active_connections = []
        self.last_player_id = 0

        # Socket
        self.tcp_socket = self.manager.open_TCP_server_rendezvous(5000, 1000)
        self.listener.add_connection(self.tcp_socket)

    def run(self):
        Thread(target=self.listen_for_new_connections, daemon=True).start()
        Thread(target=self.listen_for_new_data, daemon=True).start()
        Thread(target=self.send_updates_to_active_players, daemon=True).start()

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
                    self.handler.handle_data(datagram)

    def send_updates_to_active_players(self):
        while True:
            for player in self.active_connections:
                if player.get_joined_game():
                    self.send_pos_hpr(player.get_connection())
            sleep(0.005)

    def get_number_of_active_players(self):
        count = 0
        for other_player in self.active_connections:
            if other_player.get_joined_game():
                count += 1
        return count

    def find_player_by_connection(self, connection):
        for player in self.active_connections:
            if connection == player.connection:
                return player
        return None

    def find_player_by_id(self, id_):
        for player in self.active_connections:
            if player.id == id_:
                return player

    def send_pos_hpr(self, connection):
        datagram = PyDatagram()
        active_players = self.get_number_of_active_players()
        datagram.add_uint8(Message.POS_HPR)
        for i, player in enumerate(self.active_connections):
            if player.get_joined_game():
                datagram.add_uint8(player.get_id())
                datagram.add_float64(player.get_x())
                datagram.add_float64(player.get_y())
                datagram.add_float64(player.get_z())
                datagram.add_float64(player.get_h())
                datagram.add_float64(player.get_p())
                datagram.add_float64(player.get_r())
        self.writer.send(datagram, connection)


if __name__ == "__main__":
    server = Server()
    server.run()
    quit_server = input('Press any key to turn off the server...\n')


