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

        # Continuous net submodules.
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

    def get_main_section_state(self) -> WorldState:
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
