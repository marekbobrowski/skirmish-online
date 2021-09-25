from .base import BaseSender, Event
from protocol.messages import TextMessageRequest


class TextMessageSender(BaseSender):
    """
    Sends text messages
    """

    MANAGED_EVENT = Event.TXT_MSG_TO_SERVER_TYPED
    MESSAGE_CLS = TextMessageRequest

    def handle(self, message: str) -> None:
        """
        Sends the text message
        """
        self.send(TextMessageRequest.build(message))
