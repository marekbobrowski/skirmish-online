from .base import Message, UInt8


class SetName(Message):
    ID = UInt8(4)
    SCHEMA = []
