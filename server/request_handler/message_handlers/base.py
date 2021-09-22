from abc import abstractmethod
from protocol.messages.base import Message
from typing import Optional, Any
from .bank import MetaClass


class MessageHandler(metaclass=MetaClass):
    handled_message: Message = None
    response_message: Optional[Message] = None

    def __init__(self, session, message: Message):
        self.session = session
        self.message = message

    def __call__(self) -> Optional[Any]:
        self.handle_message()
        return self.build_response()

    @abstractmethod
    def handle_message(self):
        """
        Main method, handles message
        and updates application state
        """
        pass

    def build_response(self) -> Optional[Message]:
        """
        Response builder
        """
        return None
