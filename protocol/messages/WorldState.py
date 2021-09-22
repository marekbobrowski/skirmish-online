from .base import Message, MessageType, UInt8
from ..domain import Player, ListOf


class WorldStateRequest(Message):
    ID = UInt8(1)
    SCHEMA = []
    TYPE = MessageType.request


class WorldStateResponse(Message):
    ID = UInt8(1)
    SCHEMA = [Player, ListOf(Player)]
    TYPE = MessageType.response
