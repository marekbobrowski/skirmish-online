from .base import Message, UInt8


class NewPlayer(Message):
    ID = UInt8(102)
    SCHEMA = []
