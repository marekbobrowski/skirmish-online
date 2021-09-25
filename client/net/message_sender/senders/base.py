from direct.showbase.DirectObject import DirectObject
from direct.distributed.PyDatagram import PyDatagram
from client.event import Event
from protocol.messages.base import Message
from abc import abstractmethod


class BaseSender(DirectObject):
    """
    Base sender implementation
    """
    MANAGED_EVENT: Event
    MESSAGE_CLS: Message

    def __init__(self, manager):
        """
        Stores manager for request
        sending
        """
        super().__init__()
        self.manager = manager

        self.accept(self.MANAGED_EVENT, self.handle)

    @abstractmethod
    def handle(self, *args, **kwargs) -> None:
        """
        Overwrite this method for handling
        events. This method should:
            - build message from given params
            - send the message using self.send(message)
        Optionally return self._continue
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
