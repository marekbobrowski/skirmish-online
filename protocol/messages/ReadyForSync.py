from .base import Message, MessageType, UInt8


class ReadyForSyncRequest(Message):
    ID = UInt8(150)
    SCHEMA = []
    TYPE = MessageType.request
