from .base import Message, MessageType, UInt8
from ..domain import Disconnect


class DisconnectRequest(Message):
    ID = UInt8(53)
    SCHEMA = Disconnect
    TYPE = MessageType.request


class DisconnectResponse(Message):
    ID = UInt8(58)
    TYPE = MessageType.response
