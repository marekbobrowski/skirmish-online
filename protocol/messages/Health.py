from .base import Message, UInt8


class Health(Message):
    ID = UInt8(103)
    SCHEMA = []
