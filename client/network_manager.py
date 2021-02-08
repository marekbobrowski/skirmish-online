from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from panda3d.core import NetDatagram
from direct.task.Task import Task
from protocol.message import Message


class NetworkManager:
    def __init__(self, core):
        self.core = core

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

    def start_listening_for_updates(self):
        self.core.taskMgr.add(self.listen_for_updates, "ListenForUpdates")

    def start_sending_updates(self):
        self.core.taskMgr.add(self.send_updates, "SendUpdates")

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
            self.send_pos_hpr()
            return Task.cont
        else:
            return Task.done

    def process_updates(self, datagram, iterator):
        packet_type = iterator.get_uint8()
        if packet_type == Message.POS_HPR:
            self.handle_pos_hpr_from_server(datagram, iterator)
        elif packet_type == Message.NEW_PLAYER:
            self.handle_new_player(datagram, iterator)
        elif packet_type == Message.DISCONNECTION:
            self.handle_disconnection(datagram, iterator)

    def send_pos_hpr(self):
        datagram = PyDatagram()
        datagram.add_uint8(Message.POS_HPR)
        datagram.add_float64(self.core.world.player.get_x())
        datagram.add_float64(self.core.world.player.get_y())
        datagram.add_float64(self.core.world.player.get_z())
        datagram.add_float64(self.core.world.player.get_h())
        datagram.add_float64(self.core.world.player.get_p())
        datagram.add_float64(self.core.world.player.get_r())
        self.writer.send(datagram, self.server_connection)

    def handle_pos_hpr_from_server(self, datagram, iterator):
        while iterator.get_remaining_size() > 0:
            id = iterator.get_uint8()
            x = iterator.get_float64()
            y = iterator.get_float64()
            z = iterator.get_float64()
            h = iterator.get_float64()
            p = iterator.get_float64()
            r = iterator.get_float64()
            self.core.world.update_player_pos_hpr(id, x, y, z, h, p, r)

    def handle_new_player(self, datagram, iterator):
        id = iterator.get_uint8()
        name = iterator.get_string()
        class_number = iterator.get_uint8()
        x = iterator.get_float64()
        y = iterator.get_float64()
        z = iterator.get_float64()
        h = iterator.get_float64()
        p = iterator.get_float64()
        r = iterator.get_float64()
        new_player = self.core.world.create_other_player(class_number, id, name, x, y, z, h, p, r)
        new_player.enter()

    def handle_disconnection(self, datagram, iterator):
        id = iterator.get_uint8()
        player = self.core.world.get_player_by_id(id)
        if player is not None:
            self.core.world.destroy_character(player)

    def disconnect(self):
        datagram = PyDatagram()
        datagram.add_uint8(Message.DISCONNECTION)
        self.writer.send(datagram, self.server_connection)
        while self.writer.get_current_queue_size() != 0:
            print(self.writer.get_current_queue_size())
        self.connected = False







