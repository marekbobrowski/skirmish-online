from direct.distributed.PyDatagram import PyDatagram
from direct.task.Task import Task
from protocol.messages.base import Message
from abc import abstractmethod


class BaseUpdater:
    """
    Base updater
    """
    MESSAGE_CLS: Message
    INTERVAL: float

    def __init__(self, manager):
        """
        Stores manager for request
        sending
        """
        super().__init__()
        self.manager = manager
        self.last_state = None

    @abstractmethod
    def handle(self, *args, **kwargs) -> None:
        """
        Overwrite this method for handling
        events. This method should:
            - build message from given params
            - send the message using self.send(message)
        """
        pass

    def send(self, message: Message) -> None:
        """
        This method sends message to server
        """
        connection = self.manager.server_connection
        datagram = PyDatagram()
        message.dump(datagram)

        self.manager.writer.send(
            datagram,
            connection,
        )

    @property
    def _continue(self):
        """
        Return self.continue for continuing
        task
        """
        return Task.cont
