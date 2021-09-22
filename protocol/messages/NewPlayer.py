from .base import Message, UInt8, MessageType
from ..domain import Player, ListOf


class NewPlayerResponse(Message):
    ID = UInt8(102)
    SCHEMA = [ListOf(Player)]
    TYPE: MessageType.response
