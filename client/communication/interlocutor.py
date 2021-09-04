from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter
from panda3d.core import NetDatagram
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator



import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
from protocol.message import Message


class Interlocutor:
    """
    This class is responsible for communication with the game server.
    """
    def __init__(self):
        # Networking modules from panda3d.
        self.manager = QueuedConnectionManager()
        self.reader = QueuedConnectionReader(self.manager, 0)
        self.writer = ConnectionWriter(self.manager, 0)

        self.console = None

        # Continuous communication submodules.
        self.local_sync = None
        self.server_sync = None

        # Network manager state.
        self.server_port = 5000
        self.server_address = None
        self.timeout = 4000
        self.server_connection = None

        self.is_connecting = False

    def connect(self, server_address):
        """
        Establishes TCP connection with the game server.
        """
        self.server_address = server_address
        self.server_connection = self.manager.open_TCP_client_connection(self.server_address,
                                                                         self.server_port, self.timeout)
        if self.server_connection:
            self.reader.add_connection(self.server_connection)
            return True
        return False

    def ask_for_pass(self, name, class_number):
        """
        Asks the server, if the client can join the game with the specified player name and class.
        Waits for the server's response and returns it.
        """
        # send datagram asking if player can join the world
        data = PyDatagram()
        data.add_uint8(Message.ASK_FOR_PASS)
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
                if packet_type == Message.ASK_FOR_PASS:
                    allow_join = iterator.get_uint8()
                    if allow_join == 1:
                        return True
        return False

    def get_world_state(self):
        """
        Asks the server for initial data, so the client can load all currently active players within the world.
        The initial data consists of player names, classes, health points, positions etc. The function waits for
        the server to respond. If the server sends the initial data, then the function returns the received datagram
        and it's iterator.
        """
        # send datagram asking for initial world data (player's location, other player names, positions)
        data = PyDatagram()
        data.add_uint8(Message.WORLD_STATE)
        self.writer.send(data, self.server_connection)
        # wait for datagram from the server
        self.manager.wait_for_readers(self.timeout/1000)
        if self.reader.data_available():
            datagram = NetDatagram()
            if self.reader.get_data(datagram):
                iterator = PyDatagramIterator(datagram)
                packet_type = iterator.get_uint8()
                if packet_type == Message.WORLD_STATE:
                    return iterator, datagram
        return None

    def send_ready_for_updates(self):
        """
        Sends a message to the server announcing that the client is ready for regular game updates (has loaded the world).
        The world updates consist of all players' positions, rotations, health points etc.
        """
        data = PyDatagram()
        data.add_uint8(Message.READY_FOR_UPDATES)
        self.writer.send(data, self.server_connection)

    def begin_sync(self, world):
        """
        Runs 2 separate tasks to continuously communicate with the server:
        > sender thread -- sends messages from the client (for example: ability usage attempt)
        > local_updater thread -- handles the data sent by the server (positions, rotations, health point changes etc.)
        This communication concerns only what's happening during the actual gameplay (the skirmish scene).
        There are separate functions responsible for establishing communication and other starter actions.
        """
        from local import core
        from communication.server_sync import ServerSync
        from communication.local_sync import LocalSync
        self.server_sync = ServerSync(self, world)
        self.local_sync = LocalSync(self, world)
        core.instance.task_mgr.add(self.local_sync.listen_for_updates, 'listen for skirmish updates')
        core.instance.task_mgr.add(self.server_sync.send_updates, 'send skirmish updates')

    def get_welcome_message(self):
        data = PyDatagram()
        data.add_uint8(Message.WELCOME_MSG)
        self.writer.send(data, self.server_connection)
        self.manager.wait_for_readers(self.timeout / 1000)
        if self.reader.data_available():
            datagram = NetDatagram()
            if self.reader.get_data(datagram):
                iterator = PyDatagramIterator(datagram)
                packet_type = iterator.get_uint8()
                if packet_type == Message.WELCOME_MSG:
                    n_lines = iterator.get_uint8()
                    lines = []
                    for i in range(n_lines):
                        lines.append(iterator.get_string())
                    return lines
        return None

    def stop_updating_skirmish(self):
        """
        Stops continuous communication with the server.
        """
        from local import core
        core.instance.task_mgr.remove('listen for skirmish updates')
        core.instance.task_mgr.remove('send skirmish updates')

    def send_disconnect(self):
        """
        Sends a datagram with disconnection announcement.
        """
        datagram = PyDatagram()
        datagram.add_uint8(Message.DISCONNECTION)
        self.writer.send(datagram, self.server_connection)

    def disconnect(self):
        """
        Disconnects from the server.
        """
        self.send_disconnect()
        self.manager.close_connection(self.server_connection)

    def plug_console(self, console):
        self.local_sync.console = console
