from .request_handler import Handler
from .storage.session import SessionManager
from .event_notifier.notifier import NotifierManager
from .storage.cache.player_position import PlayerPositionCache

from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionListener
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter
from panda3d.core import PointerToConnection
from panda3d.core import NetAddress
from panda3d.core import NetDatagram

from threading import Thread


class Server:
    def __init__(self):
        # Support objects
        self.manager = QueuedConnectionManager()
        self.listener = QueuedConnectionListener(self.manager, 0)
        self.reader = QueuedConnectionReader(self.manager, 0)
        self.writer = ConnectionWriter(self.manager, 0)
        self.handler = Handler(self)

        # Server state
        self.session_manager = SessionManager()
        self.notifier_manager = NotifierManager(self)
        self.player_position_cache = PlayerPositionCache()

        # Socket
        self.tcp_socket = self.manager.open_TCP_server_rendezvous(15000, 1000)
        self.listener.add_connection(self.tcp_socket)

    def run(self):
        """
        Creates threads with active targets for accepting new connections and
        receiving data from existing ones
        """
        Thread(target=self.listen_for_new_connections, daemon=True).start()
        Thread(target=self.listen_for_new_data, daemon=True).start()

    def listen_for_new_connections(self):
        """
        Listens to new connections, when avalibe, creates new session
        and event notifier
        """
        while True:
            if self.listener.new_connection_available():
                rendezvous = PointerToConnection()
                net_address = NetAddress()
                new_connection = PointerToConnection()
                if self.listener.get_new_connection(
                    rendezvous, net_address, new_connection
                ):
                    new_connection = new_connection.p()

                    self.reader.add_connection(new_connection)

                    session = self.session_manager.new_session(
                        new_connection, self.player_position_cache
                    )
                    self.notifier_manager.new_notifier(session, new_connection)

    def listen_for_new_data(self):
        """
        Listens for new data from active connections
        """
        while True:
            if self.reader.data_available():
                datagram = NetDatagram()
                if self.reader.get_data(datagram):
                    connection = datagram.getConnection()
                    self.handler.handle_data(
                        datagram,
                        connection,
                        self.session_manager.for_connection(connection),
                    )
