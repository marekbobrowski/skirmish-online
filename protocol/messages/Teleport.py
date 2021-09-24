from .base import Message, UInt8


class Teleport(Message):
    ID = UInt8(101)
