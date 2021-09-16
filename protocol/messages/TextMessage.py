from .base import Message, UInt8


class TextMessage(Message):
    ID = UInt8(54)
    SCHEMA = []
