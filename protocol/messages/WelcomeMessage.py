from .base import Message, UInt8
from ..domain import WelcomeMessage


class WelcomeMessage(Message):
    ID = UInt8(3)
    SCHEMA = [WelcomeMessage]
