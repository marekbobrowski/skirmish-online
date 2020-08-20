from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionListener
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter
from _thread import start_new_thread
from panda3d.core import PointerToConnection
from panda3d.core import NetAddress
from panda3d.core import NetDatagram
from player import Player


class Server:
    def __init__(self):
        self.manager = QueuedConnectionManager()
        self.listener = QueuedConnectionListener(self.manager, 0)
        self.reader = QueuedConnectionReader(self.manager, 0)
        self.writer = ConnectionWriter(self.manager, 0)
        self.active_connections = []
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
                    self.active_connections.append({'connection': new_connection, 'player': Player()})
                    print(str(new_connection.get_address()) + ' connected')
                    self.reader.add_connection(new_connection)

    def listen_for_new_data(self):
        while True:
            if self.reader.data_available():
                datagram = NetDatagram()
                if self.reader.get_data(datagram):
                    self.process_data(datagram)

    def process_data(self, datagram):
        pass


if __name__ == "__main__":
    server = Server()
    server.run()
    quit_server = input('Press any key to turn off the server...\n')


