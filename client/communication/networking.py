from event import Event
from local.player import Player
from local import core

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


class Networking:
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
        self.server_address = server_address
        self.server_connection = self.manager.open_TCP_client_connection(self.server_address,
                                                                         self.server_port, self.timeout)
        if self.server_connection:
            self.reader.add_connection(self.server_connection)
            return True
        return False

    def load_world_state(self, world, scene):
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
                    main_player = Player()
                    main_player.id = iterator.get_uint8()
                    main_player.name = iterator.get_string()
                    main_player.health = iterator.get_uint8()
                    main_player.model = iterator.get_uint8()
                    main_player.animation = iterator.get_string()
                    main_player.x = iterator.get_float64()
                    main_player.y = iterator.get_float64()
                    main_player.z = iterator.get_float64()
                    main_player.h = iterator.get_float64()
                    main_player.p = iterator.get_float64()
                    main_player.r = iterator.get_float64()
                    world.set_main_player(main_player)
                    scene.spawn_player_character(main_player)
                    scene.floating_bars.create_bar(main_player)
                    while iterator.get_remaining_size() > 0:
                        player = Player()
                        player.id = iterator.get_uint8()
                        player.name = iterator.get_string()
                        player.health = iterator.get_uint8()
                        player.model = iterator.get_uint8()
                        player.animation = iterator.get_string()
                        player.x = iterator.get_float64()
                        player.y = iterator.get_float64()
                        player.z = iterator.get_float64()
                        player.h = iterator.get_float64()
                        player.p = iterator.get_float64()
                        player.r = iterator.get_float64()
                        world.add_other_player(player)
                        scene.spawn_player_character(player)
                        scene.floating_bars.create_bar(player)

    def send_ready_for_updates(self):
        data = PyDatagram()
        data.add_uint8(Message.READY_FOR_SYNC)
        self.writer.send(data, self.server_connection)

    def begin_sync(self):
        from local import core
        from communication.server_sync import ServerSync
        from communication.local_sync import LocalSync
        self.server_sync = ServerSync(self)
        self.local_sync = LocalSync(self)
        core.instance.task_mgr.add(self.local_sync.listen_for_updates, 'listen for skirmish updates')

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
        from local import core
        core.instance.task_mgr.remove('listen for skirmish updates')
        core.instance.task_mgr.remove('send skirmish updates')

    def send_disconnect(self):
        datagram = PyDatagram()
        datagram.add_uint8(Message.DISCONNECTION)
        self.writer.send(datagram, self.server_connection)

    def disconnect(self):
        self.send_disconnect()
        self.manager.close_connection(self.server_connection)
