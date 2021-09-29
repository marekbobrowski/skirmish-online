from .base import BaseSender
from client.local.client_event import ClientEvent
from protocol.messages import TextMessageRequest


class TextMessageSender(BaseSender):
    """
    Sends text messages
    """

    MANAGED_EVENT = ClientEvent.COMMAND_TO_SERVER
    MESSAGE_CLS = TextMessageRequest

    def handle(self, message: str) -> None:
        """
        Sends the text message
        """
        self.send(TextMessageRequest.build(message))
