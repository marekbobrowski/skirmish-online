from .base import Message, UInt8


class Disconnection(Message):
    ID = UInt8(53)
