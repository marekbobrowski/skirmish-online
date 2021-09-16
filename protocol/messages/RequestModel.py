from .base import Message, UInt8


class RequestModel(Message):
    ID = UInt8(2)
    SCHEMA = []
