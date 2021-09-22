from .base import Message, MessageType, UInt8
from ..domain import LongMessage


class WelcomeMessageRequest(Message):
    ID = UInt8(3)
    TYPE = MessageType.request


class WelcomeMessageResponse(Message):
    ID = UInt8(3)
    SCHEMA = LongMessage
    TYPE = MessageType.response
