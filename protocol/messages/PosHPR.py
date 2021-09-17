from .base import Message, MessageType, UInt8
from ..domain import PlayerPosHPR


class PosHPRRequest(Message):
    ID = UInt8(50)
    SCHEMA = [PlayerPosHPR]
    TYPE = MessageType.request
