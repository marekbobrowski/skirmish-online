from .base import Message, UInt8


class CombatData(Message):
    ID = UInt8(55)
