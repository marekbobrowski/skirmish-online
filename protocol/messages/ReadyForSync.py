from .base import Message, UInt8


class ReadyForSync(Message):
    ID = UInt8(150)
    SCHEMA = []
