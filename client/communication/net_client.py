from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter
from panda3d.core import NetDatagram
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from ..local import core
from .send_requests import SendRequests
from .fetch_events import FetchEvents
from protocol.message import Message
from protocol.parser import MessageParser, MessageType
from protocol.domain.WorldState import WorldState
from protocol.messages.WorldState import WorldStateRequest, WorldStateResponse


class NetClient:
    def __init__(self, server_address):
        # Networking modules from panda3d.
        self.manager = QueuedConnectionManager()
        self.reader = QueuedConnectionReader(self.manager, 0)
        self.writer = ConnectionWriter(self.manager, 0)

        self.console = None

        # Continuous communication submodules.
        self.local_sync = None
        self.server_sync = None

        # Network manager state.
        self.server_port = 15000
        self.server_address = server_address
        self.timeout = 4000
        self.server_connection = None

        self.is_connecting = False

        self.message_parser = MessageParser()

    def connect(self):
        self.server_connection = self.manager.open_TCP_client_connection(
            self.server_address, self.server_port, self.timeout
        )
        if self.server_connection:
            self.reader.add_connection(self.server_connection)
            return True
        return False

    def get_world_state(self) -> WorldState:
        """
        Fetch current world state from the server.
        """

        # send datagram asking for current world data (player's location, other player names, positions etc.)
        data = PyDatagram()
        data.add_uint8(WorldStateRequest.ID)
        self.writer.send(data, self.server_connection)

        # wait for datagram from the server
        self.manager.wait_for_readers(self.timeout / 1000)

        if not self.reader.data_available():
            raise Exception("No response to world state request.")

        datagram = NetDatagram()

        if not self.reader.get_data(datagram):
            raise Exception("World state response error.")

        iterator = PyDatagramIterator(datagram)
        world_state_message = self.message_parser(iterator, MessageType.response)
        return world_state_message.data

    def send_ready_for_updates(self):
        data = PyDatagram()
        data.add_uint8(Message.READY_FOR_SYNC)
        self.writer.send(data, self.server_connection)

    def begin_sync(self):
        self.server_sync = SendRequests(self)
        self.local_sync = FetchEvents(self)
        core.instance.task_mgr.add(
            self.local_sync.listen_for_updates, "listen for updates"
        )

    # def load_world_state(self, world):
    #     # send datagram asking for initial world data (player's location, other player names, positions)
    #     data = PyDatagram()
    #     data.add_uint8(Message.WORLD_STATE)
    #     self.writer.send(data, self.server_connection)
    #     # wait for datagram from the server
    #     self.manager.wait_for_readers(self.timeout / 1000)
    #     if self.reader.data_available():
    #         datagram = NetDatagram()
    #         if self.reader.get_data(datagram):
    #             iterator = PyDatagramIterator(datagram)
    #             packet_type = iterator.get_uint8()
    #             if packet_type == Message.WORLD_STATE:
    #                 main_player = Unit()
    #                 main_player.id = iterator.get_uint8()
    #                 main_player.name = iterator.get_string()
    #                 main_player.health = iterator.get_uint8()
    #                 main_player.model = iterator.get_uint8()
    #                 main_player.animation = iterator.get_string()
    #                 main_player.weapon = iterator.get_uint8()
    #                 main_player.x = iterator.get_float64()
    #                 main_player.y = iterator.get_float64()
    #                 main_player.z = iterator.get_float64()
    #                 main_player.h = iterator.get_float64()
    #                 main_player.p = iterator.get_float64()
    #                 main_player.r = iterator.get_float64()
    #                 world.spawn_unit(main_player)
    #                 world.floating_bars.create_bar(main_player)
    #                 world.main_player_id = main_player.id
    #                 while iterator.get_remaining_size() > 0:
    #                     player = Unit()
    #                     player.id = iterator.get_uint8()
    #                     player.name = iterator.get_string()
    #                     player.health = iterator.get_uint8()
    #                     player.model = iterator.get_uint8()
    #                     player.animation = iterator.get_string()
    #                     player.weapon = iterator.get_uint8()
    #                     player.x = iterator.get_float64()
    #                     player.y = iterator.get_float64()
    #                     player.z = iterator.get_float64()
    #                     player.h = iterator.get_float64()
    #                     player.p = iterator.get_float64()
    #                     player.r = iterator.get_float64()
    #                     world.spawn_unit(player)
    #                     world.floating_bars.create_bar(player)
