from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from panda3d.core import NetDatagram
from direct.task.Task import Task
from networking.skirmish_sender import SkirmishSender
from networking.skirmish_local_updater import SkirmishLocalUpdater
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
from protocol.message import Message


class NetworkManager:
    def __init__(self, core):
        self.core = core

        self.manager = QueuedConnectionManager()
        self.reader = QueuedConnectionReader(self.manager, 0)
        self.writer = ConnectionWriter(self.manager, 0)

        self.skirmish_local_updater = None
        self.skirmish_sender = None

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

    def send_ready_for_updates(self):
        data = PyDatagram()
        data.add_uint8(Message.READY_FOR_UPDATES)
        self.writer.send(data, self.server_connection)

    def start_updating_skirmish(self, skirmish):
        self.skirmish_sender = SkirmishSender(skirmish, self.writer, self.server_connection)
        self.skirmish_local_updater = SkirmishLocalUpdater(skirmish)
        self.core.task_mgr.add(self.listen_for_updates, "Listen For Skirmish Updates")
        self.core.task_mgr.add(self.send_updates, "Send Skirmish Updates")

    def listen_for_updates(self, task):
        if self.connected:
            if self.reader.data_available():
                datagram = NetDatagram()
                iterator = PyDatagramIterator(datagram)
                if self.reader.get_data(datagram):
                    self.process_updates(datagram, iterator)
            return Task.cont
        else:
            return Task.done

    def send_updates(self, task):
        if self.connected:
            self.skirmish_sender.send_pos_hpr()
            return Task.cont
        else:
            return Task.done

    def process_updates(self, datagram, iterator):
        packet_type = iterator.get_uint8()
        if packet_type == Message.POS_HPR:
            self.skirmish_local_updater.update_pos_hpr(datagram, iterator)
        elif packet_type == Message.NEW_PLAYER:
            self.skirmish_local_updater.update_new_player(datagram, iterator)
        elif packet_type == Message.DISCONNECTION:
            self.skirmish_local_updater.update_disconnection(datagram, iterator)
        elif packet_type == Message.HEALTH:
            self.skirmish_local_updater.update_health(datagram, iterator)

    def disconnect(self):
        self.skirmish_sender.send_disconnect()
        self.reader.remove_connection(self.server_connection)
        self.connected = False








