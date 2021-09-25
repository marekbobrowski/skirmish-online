from ..local import core
from .message_sender.sender import Sender
from .message_handler.handler import Handler
from .section_state_fetcher import SectionStateFetcher
from protocol.message import Message

from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter
from panda3d.core import NetDatagram
from direct.distributed.PyDatagram import PyDatagram
from direct.task.Task import Task


class NetClient:
    def __init__(self, server_address):
        # server information
        self.server_address = server_address
        self.server_port = 15000
        self.timeout = 4000
        self.server_connection = None

        # networking modules from panda3d
        self.manager = QueuedConnectionManager()
        self.reader = QueuedConnectionReader(self.manager, 0)
        self.writer = ConnectionWriter(self.manager, 0)

        # modules that deal with messages
        self.sender = Sender(self)
        self.handler = Handler(self)
        self.section_state_fetcher = SectionStateFetcher(self)

    def connect(self):
        self.server_connection = self.manager.open_TCP_client_connection(
            self.server_address, self.server_port, self.timeout
        )
        if self.server_connection:
            self.reader.add_connection(self.server_connection)
            return True
        return False

    def send_ready_for_updates(self):
        data = PyDatagram()
        data.add_uint8(Message.READY_FOR_SYNC)
        self.writer.send(data, self.server_connection)

    def begin_sync_with_server(self):
        core.instance.task_mgr.add(self.listen_for_updates, "listen-for-updates")

    def listen_for_updates(self, task):
        if self.reader.data_available():
            datagram = NetDatagram()
            if self.reader.get_data(datagram):
                self.handler.handle_data(datagram)
        return Task.cont
