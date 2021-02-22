from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from panda3d.core import NetDatagram
from networking.skirmish_sender import SkirmishSender
from networking.skirmish_local_updater import SkirmishLocalUpdater
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
from protocol.message import Message


class NetworkManager:
    """
    This class is responsible for managing the communication with the game server.
    """
    def __init__(self, core):
        self.core = core

        # Networking modules from panda3d.
        self.manager = QueuedConnectionManager()
        self.reader = QueuedConnectionReader(self.manager, 0)
        self.writer = ConnectionWriter(self.manager, 0)

        # Continuous communication submodules.
        self.skirmish_local_updater = None
        self.skirmish_sender = None

        # Network manager state.
        self.server_port = 5000
        self.server_address = None
        self.timeout = 4000
        self.server_connection = None
        self.connected = False

    """
    Establishes TCP connection with the game server.
    """
    def connect(self, server_address):
        self.server_address = server_address
        self.server_connection = self.manager.open_TCP_client_connection(self.server_address,
                                                                         self.server_port, self.timeout)
        if self.server_connection:
            self.reader.add_connection(self.server_connection)
            self.connected = True
            return True
        return False

    """
    Asks the server, if the client can join the game with the specified player name and class.
    Waits for the server's response and returns it.
    """
    def ask_for_pass(self, name, class_number):
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

    """
    Asks the server for initial data, so the client can load all currently active players within the world.
    The initial data consists of player names, classes, health points, positions etc. The function waits for
    the server to respond. If the server sends the initial data, then the function returns the received datagram 
    and it's iterator.
    """
    def ask_for_initial_data(self):
        # send datagram asking for initial world data (player's location, other player names, positions)
        data = PyDatagram()
        data.add_uint8(Message.ASK_FOR_INITIAL_DATA)
        self.writer.send(data, self.server_connection)
        # wait for datagram from the server
        self.manager.wait_for_readers(self.timeout/1000)
        if self.reader.data_available():
            datagram = NetDatagram()
            if self.reader.get_data(datagram):
                iterator = PyDatagramIterator(datagram)
                packet_type = iterator.get_uint8()
                if packet_type == Message.ASK_FOR_INITIAL_DATA:
                    return iterator, datagram
        return None

    """
    Sends a message to the server announcing that the client is ready for regular game updates (has loaded the world). 
    The world updates consist of all players' positions, rotations, health points etc.
    """
    def send_ready_for_updates(self):
        data = PyDatagram()
        data.add_uint8(Message.READY_FOR_UPDATES)
        self.writer.send(data, self.server_connection)

    """
    Runs 2 separate tasks to continuously communicate with the server:
    > sender thread -- sends messages from the client (for example: ability usage attempt)
    > local_updater thread -- handles the data sent by the server (positions, rotations, health point changes etc.)
    
    This communication concerns only what's happening during the actual gameplay (the skirmish scene).
    There are separate functions responsible for establishing communication and other starter actions.
    """
    def start_updating_skirmish(self, skirmish):
        self.skirmish_sender = SkirmishSender(skirmish, self.writer, self.server_connection, self)
        self.skirmish_local_updater = SkirmishLocalUpdater(skirmish, self)
        self.core.task_mgr.add(self.skirmish_local_updater.listen_for_updates, 'listen for skirmish updates')
        self.core.task_mgr.add(self.skirmish_sender.send_updates, 'send skirmish updates')

    """
    Stops continuous communication with the server.
    """
    def stop_updating_skirmish(self):
        self.core.task_mgr.remove('listen for skirmish updates')
        self.core.task_mgr.remove('send skirmish updates')

    """
    Sends a datagram with disconnection announcement.
    """
    def send_disconnect(self):
        datagram = PyDatagram()
        datagram.add_uint8(Message.DISCONNECTION)
        self.writer.send(datagram, self.server_connection)

    """
    Disconnects from the server.
    """
    def disconnect(self):
        self.send_disconnect()
        self.manager.close_connection(self.server_connection)
        self.connected = False
